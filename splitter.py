from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    length_function=len,
    keep_separator=False,
    add_start_index=True,
    is_separator_regex=False,
    separators=['\n\n', '\n', ' ', '']
  )

# Split the document into chunks
async def split_document(text:Document):
  return text.metadata, splitter.create_documents([text.page_content])
  # return splitter.split_documents([text])

async def split_text(input:str|List[str]):
  if isinstance(input,str):
    return splitter.create_documents([input])
  if isinstance(input,List[str]):
    return splitter.create_documents(input)
  return ''
