from langchain_community.document_loaders import PyPDFLoader
from langchain.docstore.document import Document

from splitter import split_document

async def load_pdf(pdf_file):
  # Initialize the PDF loader inside the function
  loader = PyPDFLoader(
    pdf_file,
    extract_images=True,
    headers=None,
    extraction_mode="plain",
  )
  pacge_count = 1
  async for page in loader.alazy_load():
    document = Document(
      metadata=page.metadata,
      page_content=page.page_content
    )
    print("page:",pacge_count)
    pacge_count += 1

    yield await split_document(document) # Yield each chunk one at a time 