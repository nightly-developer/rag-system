from langchain_text_splitters import RecursiveCharacterTextSplitter

# This is a long document we can split up.
with open("test.txt") as f:
    text = f.read()

text_splitter = RecursiveCharacterTextSplitter(
  # Set a really small chunk size, just to show.
  chunk_size=10,
  chunk_overlap=2,
  length_function=len,
  is_separator_regex=False,
)

texts = text_splitter.create_documents([text])
print(texts[0])
print(texts[1])

text_splitter.split_text(text)[:2]