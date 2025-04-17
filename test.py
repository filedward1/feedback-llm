import ollama

#  Initialize the Ollama client
client = ollama.Client()

# Define the model and the input prompt
model = "mistral"    # Replace with the actual model name you want to use
prompt = """"Create strictly a two paragraph that analyzes the user intake for, 
        carbs: 225g, sodium: 0g, and protein: 11.7g 
        it then compares to the recommended average intake for,
        carbs: 372g, sodium: 2g and protein: 57g.
        Provide feedback for each nutrient, indicating whether the user is above or below the recommended intake in concise bulleted format.
        Make a leeway for comparison that does not have a large gap between the user intake and the recommended intake.
        tells user about the common illness that may occur based on the compared values if there is a large gap between both intake.
        Make each paragraph short and brief but informative and make the tone academic.
        The format is as follows:
        FIRST PARAGRAPH: 2 to 3 senteces that provides an analysis of the user's intake and its comparison to the recommended values.
        """

# Send the query to the model
response = client.generate(model=model, prompt=prompt)


# Print the response from the model
print("Response:", response.response)