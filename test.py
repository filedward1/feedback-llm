from google import genai
import os

client = genai.Client(api_key="AIzaSyCboLTbdj9R_DbgIzxsV2UY-v6sbjIa1cY")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="1+1?"
)

print(response.text)