from langchain_community.document_loaders import PyPDFLoader
from langchain.docstore.document import Document

from text_splitter import split_text

async def load_pdf(pdf_file):
  # Initialize the PDF loader inside the function
  loader = PyPDFLoader(
    pdf_file,
    extract_images=True,
    headers=None,
    extraction_mode="plain",
  )

  async for page in loader.alazy_load():
    document = Document(
      metadata=page.metadata,
      page_content=page.page_content
    )

    yield await split_text(document) # Yield each chunk one at a time 