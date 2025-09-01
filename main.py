from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Tuple
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
    # User's daily intake values
    carbs_total: float 
    sodium_total: float  
    protein_total: float  
    
    # Recommended ranges for each nutrient
    recommended_carbs: Tuple[float, float]  
    recommended_sodium: Tuple[float, float]  
    recommended_protein: Tuple[float, float]  


@app.get("/")
async def welcome():
    return {"message": "Welcome to the Gemini API using Flash 2.5!"}

@app.post("/get-response")
async def get_response(request: QueryRequest):
    try:
        client = genai.Client(api_key="AIzaSyCboLTbdj9R_DbgIzxsV2UY-v6sbjIa1cY")
        # Calculate average recommended values
        carbs_sum = request.recommended_carbs[0] + request.recommended_carbs[1]
        sodium_sum = request.recommended_sodium[0] + request.recommended_sodium[1]  
        protein_sum = request.recommended_protein[0] + request.recommended_protein[1]
        
        avg_recommended_carbs = carbs_sum / 2 if carbs_sum != 0 else 0.0
        avg_recommended_sodium = sodium_sum / 2 if sodium_sum != 0 else 0.0
        avg_recommended_protein = protein_sum / 2 if protein_sum != 0 else 0.0
        
        # Determine if values are within range
        carbs_in_range = request.recommended_carbs[0] <= request.carbs_total <= request.recommended_carbs[1]
        sodium_in_range = request.recommended_sodium[0] <= request.sodium_total <= request.recommended_sodium[1]
        protein_in_range = request.recommended_protein[0] <= request.protein_total <= request.recommended_protein[1]
        
        first_paragraph = (
            f"Based on your daily intake of {request.carbs_total}g carbohydrates, "
            f"{request.sodium_total}mg sodium, and {request.protein_total}g protein, "
            f"here's how your nutrition compares to recommended values: "
            f"Your carbohydrate intake is {request.carbs_total - avg_recommended_carbs:+.1f}g "
            f"{'above' if request.carbs_total > avg_recommended_carbs else 'below'} the average recommendation of {avg_recommended_carbs:.1f}g. "
            f"Your sodium intake is {request.sodium_total - avg_recommended_sodium:+.1f}mg "
            f"{'above' if request.sodium_total > avg_recommended_sodium else 'below'} the average recommendation of {avg_recommended_sodium:.1f}mg. "
            f"Your protein intake is {request.protein_total - avg_recommended_protein:+.1f}g "
            f"{'above' if request.protein_total > avg_recommended_protein else 'below'} the average recommendation of {avg_recommended_protein:.1f}g."
        )

        # Generate health implications
        # Improved health_implications section

        # Calculate deviation percentages for severity assessment
        def calculate_deviation_percentage(actual, min_range, max_range):
            if actual < min_range:
                if min_range == 0:
                    return 100.0  # Consider 100% deviation if min_range is 0
                return ((min_range - actual) / min_range) * 100
            elif actual > max_range:
                if max_range == 0:
                    return 100.0  # Consider 100% deviation if max_range is 0
                return ((actual - max_range) / max_range) * 100
            return 0

        # Generate health implications with severity levels
        health_implications = []

        if not carbs_in_range:
            carb_deviation = calculate_deviation_percentage(
                request.carbs_total, request.recommended_carbs[0], request.recommended_carbs[1]
            )
            severity = "significantly" if carb_deviation > 30 else "moderately" if carb_deviation > 15 else "slightly"
        
            if request.carbs_total < request.recommended_carbs[0]:
                health_implications.append(
                    f"**Carbohydrate Deficiency ({severity} low):** "
                    f"Low carbohydrate intake may lead to fatigue, brain fog, nutritional deficiencies, "
                    f"and reduced athletic performance. Consider incorporating healthy complex carbs like "
                    f"whole grains, fruits, and vegetables."
                )
            else:
                health_implications.append(
                    f"**Excessive Carbohydrates ({severity} high):** "
                    f"High carbohydrate intake may contribute to weight gain, blood sugar spikes, "
                    f"increased diabetes risk, and cardiovascular issues. Consider reducing refined sugars "
                    f"and focusing on fiber-rich, complex carbohydrates."
                )

        if not sodium_in_range:
            sodium_deviation = calculate_deviation_percentage(
                request.sodium_total, request.recommended_sodium[0], request.recommended_sodium[1]
            )
            severity = "significantly" if sodium_deviation > 30 else "moderately" if sodium_deviation > 15 else "slightly"
        
            if request.sodium_total < request.recommended_sodium[0]:
                health_implications.append(
                    f"**Sodium Deficiency ({severity} low):** "
                    f"Inadequate sodium may cause muscle cramps, headaches, nausea, and in severe cases, "
                    f"hyponatremia. However, most people get adequate sodium from regular diet. "
                    f"Consult a healthcare provider if experiencing symptoms."
                )
            else:
                health_implications.append(
                    f"**High Sodium Intake ({severity} high):** "
                    f"Excessive sodium consumption may lead to high blood pressure, increased stroke risk, "
                    f"kidney strain, and fluid retention. Consider reducing processed foods, restaurant meals, "
                    f"and added salt."
                )

        if not protein_in_range:
            protein_deviation = calculate_deviation_percentage(
                request.protein_total, request.recommended_protein[0], request.recommended_protein[1]
            )
            severity = "significantly" if protein_deviation > 30 else "moderately" if protein_deviation > 15 else "slightly"
        
            if request.protein_total < request.recommended_protein[0]:
                health_implications.append(
                    f"**Protein Deficiency ({severity} low):** "
                    f"Insufficient protein may result in muscle loss, slow wound healing, weakened immunity, "
                    f"hair thinning, and mood changes. Include lean meats, fish, eggs, legumes, "
                    f"or plant-based protein sources."
                )
            else:
                health_implications.append(
                    f"**High Protein Intake ({severity} high):** "
                    f"While protein is essential, excessive intake may strain kidneys, cause digestive issues, "
                    f"and potentially increase calcium loss. Ensure adequate hydration and consider "
                    f"balancing with other macronutrients."
                )

        # Generate the third paragraph with better formatting
        if health_implications:
            second_paragraph = (
                "**Health Considerations:**\n\n" + 
                "\n\n".join(health_implications)
            )
        else:
            second_paragraph = (
                "**Health Assessment:** Your nutrient intake appears well-balanced and within recommended ranges. "
                "This suggests a healthy nutritional pattern that supports your overall well-being. "
                "Continue maintaining this balanced approach while ensuring dietary variety for optimal nutrition."
            )

        comparison_analysis = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"You are a nutrition expert system on a mobile app."
                    f"Create a feedback assessment (3-5 sentence only) based on the user's nutrient intake data.\n\n"
                    f"The feedback should be formal in tone yet concise and clear."
                    f"The purpose is to provide the user with insights into their nutrition and health implications.\n\n"
                    f"Do not include any introductory statement or title and provide only the paragraph without any additional commentary or text."
                    f"Here is the analysis: {first_paragraph}"
        )

        health_implication = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"You are a nutrition expert system on a mobile app."
                    f"Create a feedback assessment (3-5 sentence only) based on the user's nutrient intake data.\n\n"
                    f"The feedback should be formal in tone yet concise and clear."
                    f"The purpose is to provide the user with insights into their nutrition and health implications.\n\n"
                    f"Do not include any introductory statement or title and provide only the paragraph without any additional commentary or text."
                    f"Here is the analysis: {second_paragraph}"
        )

        return {
            "feedback": {
                "comparison_analysis": comparison_analysis.text,
                "health_implication": health_implication.text
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)