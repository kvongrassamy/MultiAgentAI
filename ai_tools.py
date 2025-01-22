from langchain.agents import tool
from langchain.tools.retriever import create_retriever_tool
from langchain_community.document_loaders import ArxivLoader

from langchain_openai import OpenAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
import os
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=256)
# Vector Store Creation
vector_store = MongoDBAtlasVectorSearch.from_connection_string(
    connection_string=mongo_uri,
    namespace="articles.scientific_articles",
    embedding= embedding_model,
    index_name="vector_index",
    text_key="abstract"
)
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})
retriever_tool = create_retriever_tool(
        retriever=retriever,
        name="knowledge_base",
        description="This serves as the base knowledge source of the agent and contains some records of research papers from Arxiv. This tool is used as the first step for exploration and research efforts." 
    )

@tool
def get_metadata_information_from_arxiv(word: str) -> list:
    """
    Fetches and returns metadata for a maximum of ten documents from arXiv matching the given query word.
    Args:
    word (str): The search query to find relevant documents on arXiv.
    Returns:
    list: Metadata about the documents matching the query.
    """
    docs = ArxivLoader(query=word, load_max_docs=10).load()
    # Extract just the metadata from each document
    metadata_list = [doc.metadata for doc in docs]
    return metadata_list

@tool
def get_information_from_arxiv(word: str) -> list:
    """
    Fetches and returns metadata for a single research paper from arXiv matching the given query word, which is the ID of the paper, for example: 704.0001.
    Args:
    word (str): The search query to find the relevant paper on arXiv using the ID.
    Returns:
    list: Data about the paper matching the query.
    """
    doc = ArxivLoader(query=word, load_max_docs=1).load()
    return doc

@tool
def format_and_store(word: str) -> str:
    """
    Format the message before it is stored into a txt file
    """
    word = word.format()
    #print(word)
    with open("data/output.txt", "w+") as file:
        file.writelines(word)

    return word

