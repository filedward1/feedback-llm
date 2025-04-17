import ollama

# Initialize the Ollama client
client = ollama.Client()

# Define the model and the input prompt
model = "llama2"    # Replace with the actual model name you want to use
prompt = "give relationship advice to my friend zoe (he is a male)"

# Send the query to the model
response = client.generate(model=model, prompt=prompt)


# Print the response from the model
print("Response:", response.response)