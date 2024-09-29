import google.generativeai as genai
import os
import getpass

if "GOOGLE_API_KEY" not in os.environ:
    GoogleKey = getpass.getpass("Provide your Google API key here: ")
else:
    GoogleKey = os.environ["GOOGLE_API_KEY"]

genai.configure(api_key=GoogleKey)
text = "Hello World!"
result = genai.embed_content(
            model="models/text-embedding-004", content=text, output_dimensionality=768
        )
print(result["embedding"])