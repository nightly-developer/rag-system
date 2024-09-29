from pdf_reader import load_pdf
import asyncio

async def main():
  pdf_file = "WekaManual_13to15.pdf"
  ids = list()
  id_calibration = 0
  async for metadata, chunks in load_pdf(pdf_file):  # Use async
    for id, chunk in enumerate(chunks):
      chunk.metadata.update(metadata)
      ids.append(id_calibration+id)
  
    # await upload_to_supabase(chunks,ids)
    id_calibration = ids[-1]
    ids = list()


if __name__ == "__main__":
  asyncio.run(main())

# if "GOOGLE_API_KEY" not in os.environ:
#     os.environ["GOOGLE_API_KEY"] = getpass("Provide your Google API key here")