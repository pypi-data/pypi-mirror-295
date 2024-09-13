"""Module that manages individual Nyx products."""

import logging
import urllib

log = logging.getLogger(__name__)


class NyxProduct:
    """Represents a product in the Nyx system.

    This class encapsulates the information and functionality related to a product
    in the Nyx system, including its metadata and content retrieval.
    """

    @property
    def name(self) -> str:
        """The unique name of the product."""
        return self._name

    @property
    def title(self) -> str:
        """The title of the product."""
        return self._title

    @property
    def content_type(self) -> str:
        """Content type (as a simple string, without IANA prefix)."""
        if self._content_type.startswith("http"):
            return self._content_type.split("/")[-1]
        return self._content_type

    @property
    def url(self):
        """The server generated url for brokered access to a subscribed dataset/product."""
        if not self._access_url:
            return self._download_url
        return self._access_url + f"?buyer_org={self._org}"

    @property
    def content(self) -> str | None:
        """The downloaded content of the product (None if not yet downloaded)."""
        return self._content

    def __init__(self, **kwargs):
        """Initialize a NyxProduct instance.

        Args:
            **kwargs: Keyword arguments containing product information.
                Required keys: 'access_url'/'download_url', 'title', 'org'

        Raises:
            KeyError: If any of the required fields are missing.
        """
        if not kwargs.get("title") or not kwargs.get("org"):
            raise KeyError(f"Required fields include 'title' and 'org'. Provided fields: {', '.join(kwargs.keys())}")
        if not (kwargs.get("access_url") or kwargs.get("download_url")):
            raise KeyError(
                f"At least one of 'access_url' or 'download_url' is required. "
                f"Provided fields: {', '.join(kwargs.keys())}"
            )

        self._title = kwargs.get("title")
        self._access_url = kwargs.get("access_url")
        self._download_url = kwargs.get("download_url")
        self._org = kwargs.get("org")
        self._content = None
        self._name = kwargs.get("name", "unknown")

        if content_type := kwargs.get("mediaType"):
            self._content_type = content_type
        else:
            self._content_type = "unknown"

    def __str__(self):
        return f"Product({self._title}, {self.url}, {self._content_type})"

    def download(self):
        """Download the content of the product and populate the class content field.

        This method attempts to download the content from the product's URL
        and stores it in the `content` attribute.

        Returns:
            The downloaded content, or None if the download fails.

        Note:
            If the content has already been downloaded, this method returns the cached content without re-downloading.
        """
        if self._content:
            return self._content
        url = self.url
        try:
            with urllib.request.urlopen(url) as f:
                self._content = f.read().decode("utf-8")
                return self._content
        except urllib.error.URLError as err:
            log.warning(
                "Failed to download content of data product [%s], "
                "confirm the source is still available with the data producer: %s",
                self._title,
                err,
            )
            return None
