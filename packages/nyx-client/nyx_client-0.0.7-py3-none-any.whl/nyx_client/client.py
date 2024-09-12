"""
Module for managing connection to Nyx
"""

import base64
import json
import logging
import uuid
from dataclasses import dataclass
from typing import Dict, List, Optional

import grpc
import requests
from iotics.api.common_pb2 import Headers, Scope
from iotics.api.meta_pb2 import SparqlQueryResponse, SparqlResultType
from requests_toolbelt.multipart.encoder import MultipartEncoder

from .configuration import BaseNyxConfig
from .host_client import HostClient
from .products import NyxProduct

logging.basicConfig(format="%(asctime)s %(levelname)s [%(module)s] %(message)s", level=logging.INFO)

log = logging.getLogger(__name__)

NS_IOTICS = "http://data.iotics.com/iotics#"
NS_NYX = "http://data.iotics.com/pnyx#"

NYX_PRODUCT_NAME = NS_NYX + "productName"

_SELECT = """
        PREFIX dcat: <http://www.w3.org/ns/dcat#>
        PREFIX dct: <http://purl.org/dc/terms/>

        SELECT ?access_url ?title ?org ?name ?mediaType
"""

_COMMON_FILTER = f"""
          ?s <{NYX_PRODUCT_NAME}> ?name .
          ?s dcat:accessURL ?access_url .
          ?s dct:title ?title .
          ?s dcat:mediaType ?mediaType .
"""


@dataclass
class NyxClient:
    """@public
    A client for interacting with the Nyx system.

    This client provides methods for querying and processing data from Nyx.

    Args:
        env_file (str, optional): Path to the environment file containing configuration.
        config (BaseNyxConfig, optional): Pre-configured BaseNyxConfig object.

    Attributes:
        config (BaseNyxConfig): Configuration for the Nyx client.
        host_client (HostClient): Client for interacting with the host.
    """

    config: BaseNyxConfig
    host_client: HostClient

    def __init__(
        self,
        env_file: Optional[str] = None,
        config: Optional[BaseNyxConfig] = None,
    ):
        if config:
            self.config = config
        else:
            self.config = BaseNyxConfig(env_file, validate=True)

        self._token = self.config.override_token
        self._refresh = ""
        self._subscribed_products: List[NyxProduct] = []

        self._setup()

    def _setup(self):
        self._authorise(refresh=False)

        # Set user nickname
        self.name = self._nyx_get("users/me").get("name")
        log.debug("successful login as %s", self.name)

        self.update_subscriptions(refresh=False)

        # Get host info
        qapi = self._nyx_get("auth/qapi-connection")
        self.config.community_mode = qapi.get("community_mode", False)
        self.config.org = (
            f"{qapi.get('org_name')}/{self.config.nyx_username}" if self.config.community_mode else qapi.get("org_name")
        )
        self.config.host_config.host_url = qapi.get("grpc_url")
        self.config.host_config.resolver_url = qapi.get("resolver_url")

        self.host_client = HostClient(self.config.host_config)

    def _nyx_post(self, endpoint: str, data: dict, headers: dict = None, multipart: MultipartEncoder = None) -> dict:
        if not headers:
            headers = {"X-Requested-With": "nyx-sdk", "Content-Type": "application/json"}
        if self._token:
            headers["authorization"] = "Bearer " + self._token
        resp = requests.post(
            url=self.config.nyx_url + "/api/portal/" + endpoint,
            json=data if data else None,
            data=multipart if multipart else None,
            headers=headers,
        )
        resp.raise_for_status()

        return resp.json()

    def _nyx_get(self, endpoint: str) -> dict:
        headers = {"X-Requested-With": "nyx-sdk", "Content-Type": "application/json"}
        if self._token:
            headers["authorization"] = "Bearer " + self._token
        resp = requests.get(url=self.config.nyx_url + "/api/portal/" + endpoint, headers=headers)
        resp.raise_for_status()

        return resp.json()

    def _authorise(self, refresh=True):
        """Authorise with the configured Nyx instance using basic authorisation."""
        if not refresh and self._token:
            # If it's not fresh then we'll return and use the existing token
            return
        resp = self._nyx_post("auth/login", self.config.nyx_auth)
        log.debug("Login response: %s", resp)
        self.access_token = resp["access_token"]
        self.refresh_token = resp["refresh_token"]

    def update_subscriptions(self, refresh=True):
        """Update the list of subscribed products."""
        self._authorise(refresh)
        # Get all products we're subscribed to, so the results are relevant to what the user wants
        purchases = self._nyx_get("purchases/transactions")
        if not purchases:
            self.subscribed_products = []
            return
        self.subscribed_products = [k["product_name"] for k in purchases]

    def close(self):
        """Cleanup any resources used by the client."""
        pass

    @property
    def access_token(self):
        return self._token

    @access_token.setter
    def access_token(self, token):
        self._token = token

    @property
    def refresh_token(self):
        return self._refresh

    @refresh_token.setter
    def refresh_token(self, token):
        self._refresh = token

    @property
    def subscribed_products(self):
        return self._subscribed_products

    @subscribed_products.setter
    def subscribed_products(self, products):
        self._subscribed_products = products

    def _local_sparql_query(self, query: str) -> list[Dict[str, str]]:
        """@private
        Execute a SPARQL query against the configured IOTICS host.

        Args:
            query (str): The SPARQL query string.

        Returns:
            list[Dict[str, str]]: A list of dictionaries representing the query results.
        """
        return self._sparql_query(query, Scope.LOCAL)

    def _federated_sparql_query(self, query: str) -> list[Dict[str, str]]:
        """@private
        Execute a SPARQL query against the federated network.

        Args:
            query (str): The SPARQL query string.

        Returns:
            list[Dict[str, str]]: A list of dictionaries representing the query results.
        """
        return self._sparql_query(query, Scope.GLOBAL)

    def _sparql_query(self, query: str, scope: Scope) -> list[Dict[str, str]]:
        """@private
        Execute a SPARQL query and process the results.

        Args:
            query (str): The SPARQL query string.
            scope (Scope): The scope of the query (LOCAL or GLOBAL).

        Returns:
            list[Dict[str, str]]: A list of dictionaries representing the query results.

        Raises:
            ValueError: If the response is incomplete.
            grpc.RpcError: If there's an RPC error during the query execution.
        """
        log.warn(query)
        with self.host_client as client:
            chunks: dict[int, SparqlQueryResponse] = {}
            stream = client.api.sparql_api.sparql_query(
                query,
                result_content_type=SparqlResultType.SPARQL_JSON,
                scope=scope,
                headers=Headers(transactionRef=("nyx_sdk", str(uuid.uuid4()))),
            )
            try:
                for response in stream:
                    chunks[response.payload.seqNum] = response
            except grpc.RpcError as err:
                err: grpc._channel._MultiThreadedRendezvous
                if err.code() != grpc.StatusCode.DEADLINE_EXCEEDED:
                    raise err

            sorted_chunks = sorted(chunks.values(), key=lambda r: r.payload.seqNum)
            if len(sorted_chunks) == 0:
                return []
            last_chunk = sorted_chunks[-1]

            if not last_chunk.payload.last or len(chunks) != last_chunk.payload.seqNum + 1:
                raise ValueError("Incomplete response")
            resp_json = json.loads("".join([c.payload.resultChunk.decode() for c in sorted_chunks]))
            results = []
            for binding in resp_json["results"]["bindings"]:
                inner_json = {}
                for k in binding:
                    inner_json[k] = binding[k]["value"]
                results.append(inner_json)

            log.warn(results)
            return results

    def get_all_categories(self) -> list:
        """Retrieve all categories from the federated network.

        Returns:
            list: A list of category names.
        """
        query = """
        PREFIX dcat: <http://www.w3.org/ns/dcat#>

        SELECT DISTINCT ?theme
        WHERE {
          ?s dcat:theme ?theme .
        }
        """

        return [r["theme"] for r in self._federated_sparql_query(query)]

    def get_subscribed_categories(self) -> list:
        """Retrieve subscribed categories from the federated network.

        Returns:
            list: A list of category names.
        """
        query = f"""
        PREFIX dcat: <http://www.w3.org/ns/dcat#>

        SELECT DISTINCT ?theme
        WHERE {{
          ?s dcat:theme ?theme .
          ?s <{NYX_PRODUCT_NAME}> ?name .
          FILTER({" || ".join([f'?name = "{product}"' for product in self.subscribed_products])})
        }}
        """

        return [r["theme"] for r in self._federated_sparql_query(query)]

    def get_all_genres(self) -> list[str]:
        """Retrieve all genres from the federated network.

        Returns:
            list: A list of genre names.
        """
        query = """
        PREFIX dc: <http://purl.org/dc/terms/>

        SELECT DISTINCT ?genre
        WHERE {
          ?s dc:type ?genre .
        }
        """

        return [r["genre"] for r in self._federated_sparql_query(query)]

    def get_subscribed_genres(self) -> list[str]:
        """Retrieve subscribed genres from the federated network.

        Returns:
            list: A list of genre names.
        """
        query = f"""
        PREFIX dc: <http://purl.org/dc/terms/>

        SELECT DISTINCT ?genre
        WHERE {{
          ?s dc:type ?genre .
          ?s <{NYX_PRODUCT_NAME}> ?name .
          FILTER({" || ".join([f'?name = "{product}"' for product in self.subscribed_products])})
        }}
        """

        return [r["genre"] for r in self._federated_sparql_query(query)]

    def get_subscribed_creators(self) -> list[str]:
        """Retrieve subscribed creators from the federated network.

        Returns:
            list: A list of creator names.
        """
        query = f"""
        PREFIX dct: <http://purl.org/dc/terms/>

        SELECT DISTINCT ?creator
        WHERE {{
          ?s dct:creator ?creator .
          ?s <{NYX_PRODUCT_NAME}> ?name .
          FILTER({" || ".join([f'?name = "{product}"' for product in self.subscribed_products])})
        }}
        """

        return [r["creator"] for r in self._federated_sparql_query(query)]

    def get_all_creators(self) -> list[str]:
        """Retrieve all creators from the federated network.

        Returns:
            list: A list of creator names.
        """
        query = """
        PREFIX dct: <http://purl.org/dc/terms/>

        SELECT DISTINCT ?creator
        WHERE {
          ?s dct:creator ?creator .
        }
        """

        return [r["creator"] for r in self._federated_sparql_query(query)]

    def get_subscribed_datasets(self) -> list[NyxProduct]:
        """Retrieve subscribed datasets from the federated network.

        Returns:
            list[NyxProduct]: A list of NyxProduct instances.
        """

        query = f"""
        {_SELECT}
        WHERE {{
          {_COMMON_FILTER}
          FILTER({" || ".join([f'?name = "{product}"' for product in self.subscribed_products])})
        }}
        """

        return [NyxProduct(**r, org=self.config.org) for r in self._federated_sparql_query(query)]

    def get_subscribed_datasets_for_categories(self, categories: list[str]) -> list[NyxProduct]:
        """Retrieve subscribed datasets for specific categories from the federated network.

        Args:
            categories (list[str]): A list of category names to filter by.

        Returns:
            list[NyxProduct]: A list of NyxProduct instances matching the specified categories.
        """
        query = f"""
        {_SELECT}
        WHERE {{
          {_COMMON_FILTER}
          FILTER({" || ".join([f'?name = "{product}"' for product in self.subscribed_products])})
          ?s dcat:theme ?theme .
          FILTER({" || ".join([f'?theme = "{theme.lower()}"' for theme in categories])})
        }}
        """

        return [NyxProduct(**r, org=self.config.org) for r in self._federated_sparql_query(query)]

    def get_datasets_for_categories(self, categories: list[str]) -> list[NyxProduct]:
        """Retrieve all datasets for specific categories from the federated network.

        Args:
            categories (list[str]): A list of category names to filter by.

        Returns:
            list[NyxProduct]: A list of NyxProduct instances matching the specified categories.
        """
        query = f"""
        {_SELECT}
        WHERE {{
          {_COMMON_FILTER}
          ?s dcat:theme ?theme .
          FILTER({" || ".join([f'?theme = "{theme.lower()}"' for theme in categories])})
        }}
        """

        return [NyxProduct(**r, org=self.config.org) for r in self._federated_sparql_query(query)]

    def get_subscribed_datasets_for_genres(self, genres: list[str]) -> list[NyxProduct]:
        """Retrieve subscribed datasets for specific genres from the federated network.

        Args:
            genres (list[str]): A list of genre names to filter by.

        Returns:
            list[NyxProduct]: A list of NyxProduct instances matching the specified genres.
        """
        query = f"""
        {_SELECT}
        WHERE {{
          {_COMMON_FILTER}
          FILTER({" || ".join([f'?name = "{product}"' for product in self.subscribed_products])})
          ?s dct:type ?type .
          FILTER({" || ".join([f'?type = "{genre.lower()}"' for genre in genres])})
        }}
        """

        return [NyxProduct(**r, org=self.config.org) for r in self._federated_sparql_query(query)]

    def get_datasets_for_genres(self, genres: list[str]) -> list[NyxProduct]:
        """Retrieve datasets for specific genres from the federated network.

        Args:
            genres (list[str]): A list of genre names to filter by.

        Returns:
            list[NyxProduct]: A list of NyxProduct instances matching the specified genres.
        """
        query = f"""
        {_SELECT}
        WHERE {{
          {_COMMON_FILTER}
          ?s dct:type ?type .
          FILTER({" || ".join([f'?type = "{genre.lower()}"' for genre in genres])})
        }}
        """

        return [NyxProduct(**r, org=self.config.org) for r in self._federated_sparql_query(query)]

    def get_subscribed_datasets_for_creators(self, creators: list[str]) -> list[NyxProduct]:
        """Retrieve subscribed datasets from specific creators from the federated network.

        Args:
            creators (list[str]): A list of creators to filter by.

        Returns:
            list[NyxProduct]: A list of NyxProduct instances matching the specified creators.
        """
        query = f"""
        {_SELECT}
        WHERE {{
          {_COMMON_FILTER}
          FILTER({" || ".join([f'?name = "{product}"' for product in self.subscribed_products])})
          ?s dct:creator ?creator .
          FILTER({" || ".join([f'?creator = "{creator}"' for creator in creators])})
        }}
        """

        return [NyxProduct(**r, org=self.config.org) for r in self._federated_sparql_query(query)]

    def create_product(
        self,
        name: str,
        title: str,
        description: str,
        size: int,
        genre: str,
        categories: list[str],
        download_url: str,
        content_type: str,
        lang: str = "en",
        status: str = "published",
        preview: str = "",
        price: int = 0,
        license_url: str = "https://creativecommons.org/publicdomain/zero/1.0/",
    ):
        """Create a new product in the system.

        This method creates a new product with the provided details and posts it to Nyx.

        Args:
            name (str): The unique identifier for the product.
            title (str): The display title of the product.
            description (str): A detailed description of the product.
            size (int): The size of the product, typically in bytes.
            genre (str): The genre or category of the product.
            categories (list[str]): A list of categories the product belongs to.
            download_url (str): The URL where the product can be downloaded.
            content_type (str): The mime type of the data located at download_url.
            lang (str, optional): The language of the product. Defaults to "en".
            status (str, optional): The publication status of the product. Defaults to "published".
            preview (str, optional): A preview or sample of the product. Defaults to an empty string.
            price (int, optional): The price of the product in cents. If 0, the product is free. Defaults to 0.
            license_url (str, optional): The URL of the license for the product. Defaults to Creative Commons Zero.

        Returns:
            NyxProduct: An object representing the created product, containing the download URL and title.

        Raises:
            Any exceptions raised by the self._nyx_post method.

        Example:
            >>> product = self.create_product(
            ...     name="uniqueproductid",
            ...     title="Amazing Product",
            ...     description="This is an amazing product that does wonderful things.",
            ...     size=1024000,
            ...     genre="Software",
            ...     categories=["Utility", "Productivity"],
            ...     download_url="https://example.com/download/amazing-product",
            ...     content_type="text/csv",
            ...     price=1999  # $19.99
            ... )
            >>> print(f"Created product: {product.title}")
            Created product: Amazing Product
        """

        input_bytes = preview.encode("utf-8")
        base64_bytes = base64.b64encode(input_bytes)
        preview_base64_string = base64_bytes.decode("utf-8")

        data = {
            "name": name,
            "title": title,
            "description": description,
            "size": size,
            "genre": genre,
            "categories": categories,
            "lang": lang,
            "status": status,
            "preview": preview_base64_string,
            "downloadURL": download_url,
            "licenseURL": license_url,
            "contentType": content_type,
        }
        if price > 0:
            data["price"] = price

        multipart_data = MultipartEncoder(
            fields={
                "productMetadata": json.dumps(data),
            }
        )

        headers = {"X-Requested-With": "nyx-sdk", "Content-Type": multipart_data.content_type}

        resp = self._nyx_post("products", data, headers, multipart_data)

        args = {"name": name, "title": title, "org": self.config.org, "mediaType": content_type}

        download_url = resp.get("downloadURL")
        access_url = resp.get("accessURL")

        if download_url:
            args["download_url"] = download_url

        if access_url:
            args["access_url"] = access_url

        return NyxProduct(**args)

    def get_datasets_for_creators(self, creators: list[str]) -> list[NyxProduct]:
        """Retrieve datasets from specific creators from the federated network.

        Args:
            creators (list[str]): A list of creators to filter by.

        Returns:
            list[NyxProduct]: A list of NyxProduct instances matching the specified creators.
        """
        query = f"""
        {_SELECT}
        WHERE {{
          {_COMMON_FILTER}
          ?s dct:creator ?creator .
          FILTER({" || ".join([f'?creator = "{creator}"' for creator in creators])})
        }}
        """

        return [NyxProduct(**r, org=self.config.org) for r in self._federated_sparql_query(query)]

    def delete_product(self, product: NyxProduct):
        headers = {"X-Requested-With": "nyx-sdk", "Content-Type": "application/json"}
        if self._token:
            headers["authorization"] = "Bearer " + self._token
        resp = requests.delete(
            url=self.config.nyx_url + f"/api/portal/products/{product.name}",
            headers=headers,
        )
        resp.raise_for_status()

        return resp.json()
