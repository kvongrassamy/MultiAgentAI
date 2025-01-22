# import openai
# from langsmith import wrappers, traceable

# # Auto-trace LLM calls in-context
# client = wrappers.wrap_openai(openai.Client())

# @traceable # Auto-trace this function
# def pipeline(user_input: str):
#     result = client.chat.completions.create(
#         messages=[{"role": "user", "content": user_input}],
#         model="gpt-4o-mini"
#     )
#     return result.choices[0].message.content

# print(pipeline("Hello, world!"))

import pandas as pd
from pymongo import MongoClient
# Initialize MongoDB python client
import os
from dotenv import load_dotenv
from datasets import load_dataset

load_dotenv()

data = load_dataset("MongoDB/subset_arxiv_papers_with_embeddings")
dataset_df = pd.DataFrame(data["train"])

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
DB_NAME = "articles"
COLLECTION_NAME = "scientific_articles"
ATLAS_VECTOR_SEARCH_INDEX_NAME = "vector_index"
collection = client.get_database(DB_NAME).get_collection(COLLECTION_NAME)

# Delete any existing records in the collection
collection.delete_many({})
# Data Ingestion
records = dataset_df.to_dict('records')
collection.insert_many(records)
print("Data ingestion into MongoDB completed")



