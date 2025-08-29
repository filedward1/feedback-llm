from typing import Tuple
from google import genai
import os

carbs_total = 4 
sodium_total = 5500  
protein_total = 3.5  

# Recommended ranges for each nutrient
recommended_carbs = (2.1, 2.2)  
recommended_sodium = (2.2, 3.2)  
recommended_protein = (2.3, 3.4)  

client = genai.Client(api_key="AIzaSyCboLTbdj9R_DbgIzxsV2UY-v6sbjIa1cY")
# Calculate average recommended values
carbs_sum = recommended_carbs[0] + recommended_carbs[1]
sodium_sum = recommended_sodium[0] + recommended_sodium[1]
protein_sum = recommended_protein[0] + recommended_protein[1]

avg_recommended_carbs = carbs_sum / 2 if carbs_sum != 0 else 0.0
avg_recommended_sodium = sodium_sum / 2 if sodium_sum != 0 else 0.0
avg_recommended_protein = protein_sum / 2 if protein_sum != 0 else 0.0

# Determine if values are within range
carbs_in_range = recommended_carbs[0] <= carbs_total <= recommended_carbs[1]
sodium_in_range = recommended_sodium[0] <= sodium_total <= recommended_sodium[1]
protein_in_range = recommended_protein[0] <= protein_total <= recommended_protein[1]

# Generate feedback paragraphs
first_paragraph = (
    f"Based on your daily intake of {carbs_total}g carbohydrates, "
    f"{sodium_total}mg sodium, and {protein_total}g protein, "
    f"here's how your nutrition compares to recommended values: "
    f"Your carbohydrate intake is {carbs_total - avg_recommended_carbs:+.1f}g "
    f"{'above' if carbs_total > avg_recommended_carbs else 'below'} the average recommendation of {avg_recommended_carbs:.1f}g. "
    f"Your sodium intake is {sodium_total - avg_recommended_sodium:+.1f}mg "
    f"{'above' if sodium_total > avg_recommended_sodium else 'below'} the average recommendation of {avg_recommended_sodium:.1f}mg. "
    f"Your protein intake is {protein_total - avg_recommended_protein:+.1f}g "
    f"{'above' if protein_total > avg_recommended_protein else 'below'} the average recommendation of {avg_recommended_protein:.1f}g."
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
        carbs_total, recommended_carbs[0], recommended_carbs[1]
    )
    severity = "significantly" if carb_deviation > 30 else "moderately" if carb_deviation > 15 else "slightly"
    
    if carbs_total < recommended_carbs[0]:
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
        sodium_total, recommended_sodium[0], recommended_sodium[1]
    )
    severity = "significantly" if sodium_deviation > 30 else "moderately" if sodium_deviation > 15 else "slightly"
    
    if sodium_total < recommended_sodium[0]:
        health_implications.append(
            f"**Sodium Deficiency ({severity} low):** "
            f"Inadequate sodium may cause muscle cramps, headaches, nausea, and in severe cases, "
            f"hypothermia. However, most people get adequate sodium from regular diet. "
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
        protein_total, recommended_protein[0], recommended_protein[1]
    )
    severity = "significantly" if protein_deviation > 30 else "moderately" if protein_deviation > 15 else "slightly"
    
    if protein_total < recommended_protein[0]:
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

first_response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=f"You are a nutrition expert system on a mobile app."
            f"Create a feedback assessment based on the user's nutrient intake data.\n\n"
            f"The feedback should be formal in tone yet concise and clear."
            f"The purpose is to provide the user with insights into their nutrition and health implications.\n\n"
            f"Do not include any introductory statement and provide only the paragraph without any additional commentary or text."
            f"Here is the analysis: {first_paragraph}"
)

second_response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=f"You are a nutrition expert system on a mobile app."
            f"Create a feedback assessment based on the user's nutrient intake data.\n\n"
            f"The feedback should be formal in tone yet concise and clear."
            f"The purpose is to provide the user with insights into their nutrition and health implications.\n\n"
            f"Do not include any introductory statement and provide only the paragraph without any additional commentary or text."
            f"Here is the analysis: {second_paragraph}"
)

print(first_response.text)
print(second_response.text)