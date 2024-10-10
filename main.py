import asyncio
from langchain_community.document_loaders import PyPDFLoader

from pdf_reader import load_pdf
from splitter import split_text
from db_driver import upload as upload_to_supabase

async def upload_pdf(pdf_file:str):
  ids = list()
  id_calibration = 0
  async for metadata, chunks in load_pdf(pdf_file):  # Use async
    for id, chunk in enumerate(chunks):
      chunk.metadata.update(metadata)
      ids.append(id_calibration+id)

    await upload_to_supabase(chunks,ids)
    id_calibration = ids[-1]
    ids = list()

async def upload_text():
  with open("test.txt") as f:
    text = f.read()
  chunks = await split_text(text)
  await upload_to_supabase(chunks, list(range(len(chunks))))

async def main():
  loader = PyPDFLoader("WekaManual_13to15.pdf",
    extract_images=True,
    headers=None,
    extraction_mode="plain",
  )
  i = 0
  async for _ in loader.alazy_load():
    i += 1
    print("page:",i)
  # asyncio.run(split_text(text))
  


if __name__ == "__main__":
  asyncio.run(upload_pdf("WekaManual_short.pdf"))

# if "GOOGLE_API_KEY" not in os.environ:
#    os.environ["GOOGLE_API_KEY"] = getpass("Provide your Google API key here")