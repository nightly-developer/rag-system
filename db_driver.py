from supabase.client import create_client, Client
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_core.documents import Document
from typing import List
# import Embeddings
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
import asyncio

OpenAiKey = os.getenv("OPENAI_API_KEY")
GoogleKey = os.getenv("GOOGLE_API_KEY")
sbApiKey = os.getenv("SB_API_KEY")
sbUrl = os.getenv("SB_URL")

supabase:Client = create_client(sbUrl, sbApiKey)
# embeddings = OpenAIEmbeddings(openai_api_key=OpenAiKey)
embeddings = GoogleGenerativeAIEmbeddings(apiKey=GoogleKey,model="models/text-embedding-004")

vector_store = SupabaseVectorStore(
    embedding=embeddings,
    client=supabase,
    table_name="documents",
    query_name="match_documents",
    chunk_size=500
  )

# Create a Supabase client
async def upload_to_supabase(documents:List[Document],ids:List[int]):
  ids = await vector_store.aadd_documents(documents=documents,ids=ids)
  print(ids)

# Get the last id from the documents table
async def get_last_id():
  return supabase.table('documents').select('id') .order('id', desc=True).limit(1).execute()  
  
async def main():
  response = await get_last_id()
  print(response)

if __name__ == "__main__":
  asyncio.run(main())