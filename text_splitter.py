from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# Split the document into chunks
async def split_text(text:Document):
  text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=5,
    length_function=len,
    keep_separator=False,
    add_start_index=True,
    is_separator_regex=False,
    separators=["\n\n","\n"," ",".",",",]
  )

  return text.metadata, text_splitter.create_documents([text.page_content])

  # return text_splitter.split_documents([text])