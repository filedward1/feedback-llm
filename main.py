from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import ollama
import os


app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    carbohydrates: int  # User daily intake of carbohydrates
    protein: int    # User daily intake of protein
    sodium: int     # User daily intake of sodium
    carbAvg: int    # Recommended daily intake of carbohydrates
    proteinAvg: int # Recommended daily intake of protein
    sodiumAvg: int  # Recommended daily intake of sodium

@app.get("/")
async def welcome():
    return {"message": "Welcome to the Ollama2 API!"}

@app.post("/get-response")
async def get_response(request: QueryRequest):
    try:
        # Initialize the Ollama client
        client = ollama.Client()

        # Define the model and the input prompt
        user_carbohydrates = request.carbohydrates
        user_protein = request.protein
        user_sodium = request.sodium
        recommended_carbohydrates = request.carbAvg
        recommended_protein = request.proteinAvg
        recommended_sodium = request.sodiumAvg

        model = "llama2"  # Replace with the actual model name you want to use
        prompt = """Create a two paragraph that analyzes the user intake for, 
        carbs:{user_carbohydrates}, sodium: user_sodium}, and protein:{user_protein}  
        it then compares to the recommended average intake for,
        carbs:{recommended_carbohydrates}, sodium: {recommended_sodium} and protein: {recommended_protein}.
        Based it then tells user about the common illness that may occur based on the compared values.
        Make each paragraph short and brief but informative and make the tone academic. 
        """ # Use the query from the request      

        # Send the query to the model
        response = client.generate(model=model, prompt=prompt)

        # Return the response from the model
        return {"response": response.response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)


# # Initialize the Ollama client
# client = ollama.Client()

# # Define the model and the input prompt
# model = "llama2"    # Replace with the actual model name you want to use
# prompt = "what is the difference between you and ChatGPT and deepseek?"

# # Send the query to the model
# response = client.generate(model=model, prompt=prompt)


# # Print the response from the model
# print("Response:", response.response)