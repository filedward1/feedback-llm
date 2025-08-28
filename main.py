from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from google import genai
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
    carbohydrates: int  
    protein: int    
    sodium: int     
    carbAvg: int    
    proteinAvg: int 
    sodiumAvg: int  


@app.get("/")
async def welcome():
    return {"message": "Welcome to the Gemini API using Flash 2.5!"}

@app.post("/get-response")
async def get_response(request: QueryRequest):
    try:
        client = genai.Client(api_key="AIzaSyCboLTbdj9R_DbgIzxsV2UY-v6sbjIa1cY")

        response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=f"Carbs: {request.carbohydrates} (avg {request.carbAvg}), "
                            f"Protein: {request.protein} (avg {request.proteinAvg}), "
                            f"Sodium: {request.sodium} (avg {request.sodiumAvg}). "
                            "Give me a health recommendation."
                )

        return response.text

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
