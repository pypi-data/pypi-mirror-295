"""
Optional module for tight integration between Nyx and LangChain
"""

import logging
import os
from typing import Optional

from nyx_client.configuration import BaseNyxConfig, CohereNyxConfig, OpenAINyxConfig

try:
    from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
    from langchain_community.utilities import SQLDatabase
    from langchain_core.language_models import BaseChatModel
    from langchain_core.messages import SystemMessage
except ImportError as err:
    raise ImportError(
        "LangChain dependencies are not installed. "
        "Please install them with `pip install nyx_client[langchain_openai]` or "
        "`pip install nyx_client[langchain_cohere]`"
    ) from err

try:
    from langgraph.prebuilt import create_react_agent
except ImportError as err:
    raise ImportError(
        "LangGraph dependencies are not installed. "
        "Please install them with `pip install nyx_client[langchain_openai]` or "
        "`pip install nyx_client[langchain_cohere]`"
    ) from err

try:
    from langchain_openai import ChatOpenAI
except ImportError:

    class ChatOpenAI:
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "LangChain OpenAI dependencies are not installed. "
                "Please install them with `pip install nyx_client[langchain_openai]`"
            )


try:
    from langchain_cohere import ChatCohere
except ImportError:

    class ChatCohere:
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "LangChain Cohere dependencies are not installed. "
                "Please install them with `pip install nyx_client[langchain_cohere]`"
            )


from nyx_client.client import NyxClient
from nyx_client.products import NyxProduct
from nyx_client.utils import Parser, Utils

SQL_SYSTEM_PROMPT = """You are an agent designed to interact with a SQLite database.
Given an input question, create a syntactically correct SQLite query to run, 
then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, 
always limit your query to at most 5 results issuing follow-up queries for more data.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the below tools unless you have been given the extra database information. 
Only use the information returned by the below tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, 
rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

To start you should ALWAYS look at the tables in the database to see what you can query.
Do NOT skip this step.
Then you should query the schema of the most relevant tables.
"""

DEFAULT_COHERE_MODEL = "command-r"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"


class NyxLangChain(NyxClient):
    """An opinionated client wrapping langChain to evaluate user queries against contents of a Nyx network.

    This class extends NyxClient to provide LangChain-based functionality for querying Nyx network contents.

    Args:
        config (Optional[NyxConfig], optional): Configuration for the Nyx client. Defaults to None.
        env_file (str, optional): Path to the environment file. Defaults to None.
        llm (Optional[BaseChatModel], optional): Language model to use. Defaults to None.

    Attributes:
        llm (BaseChatModel): The language model used for querying

    Note:
        The LLM must support tool calling.
    """

    def __init__(
        self,
        config: Optional[BaseNyxConfig] = None,
        env_file: str = None,
        llm: Optional[BaseChatModel] = None,
        log_level: int = logging.INFO,
    ):
        super().__init__(env_file, config)

        logging.basicConfig(format="%(asctime)s %(levelname)s [%(module)s] %(message)s", level=log_level)
        self.log = logging.getLogger(__name__)
        self.log.setLevel(log_level)

        if llm:
            self.llm = llm
        else:
            if isinstance(self.config, CohereNyxConfig):
                self.llm = ChatCohere(model=DEFAULT_COHERE_MODEL, api_key=self.config.api_key)
            elif isinstance(self.config, OpenAINyxConfig):
                self.llm = ChatOpenAI(model=DEFAULT_OPENAI_MODEL, api_key=self.config.api_key)
            else:
                raise ValueError("No language model provided and no valid config found")

        self.system_message = SystemMessage(SQL_SYSTEM_PROMPT)

    def query(
        self,
        prompt: str,
        products: Optional[list[NyxProduct]] = None,
        sqlite_file: Optional[str] = None,
        update_subscribed: bool = True,
        k: int = 3,
    ) -> str:
        """Query the LLM with a user prompt and context from Nyx.

        This method takes a user prompt and invokes it against the LLM associated with this instance,
        using context from Nyx.

        Args:
            prompt (str): The user prompt.
            products (Optional[list[NyxProduct]], optional): List of products to use for context.
                If None, uses all subscribed products. Defaults to None.
            sqlite_file (Optional[str]): A file location to write the sql_lite file to.
            update_subscribed (bool): if set to true this will re-poll Nyx for subscribed products
            k (int): Max number of vector matches to include

        Returns:
            str: The answer from the LLM.

        Note:
            If products are not provided, this method updates subscriptions and retrieves all subscribed datasets.
        """
        if update_subscribed:
            self.update_subscriptions()
        if not products:
            products = self.get_subscribed_datasets()
        self.log.debug(f"using products: {[p.title for p in products]}")

        parser = Parser()
        parser.dataset_as_vectors([p for p in products if p.content_type != "csv"], chunk_size=100)
        matching_vectors = parser.query(prompt, k)

        engine = Parser.dataset_as_db(products, matching_vectors.chunks, sqlite_file=sqlite_file, if_exists="replace")
        db = SQLDatabase(engine=engine)

        # Optionally provide extra context to the model system prompt
        table_context = {
            "tables": db.get_usable_table_names(),
            "schemas": db.get_table_info(),
        }

        toolkit = SQLDatabaseToolkit(db=db, llm=self.llm, dialect=db.dialect)
        agent_executor = create_react_agent(self.llm, toolkit.get_tools(), state_modifier=self.system_message)
        events = agent_executor.stream(
            {"messages": [("user", Utils.build_query(prompt, **table_context))]},
            stream_mode="values",
        )

        last_content: str = ""
        for event in events:
            last_content = event["messages"][-1].content
            self.log.debug(last_content)

        if sqlite_file:
            os.remove(sqlite_file)

        return last_content
