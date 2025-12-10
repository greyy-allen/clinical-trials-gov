import datetime
import requests
import json

# Outcome shows signs of the benefit or result of the trial, so i used to to generate the categories/health-benefits involved in the array of categories relevant to the study. It was then added as an array to the documents as "categories"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

with open("simplified_data_ashwagandha.json", "r", encoding="utf-8") as f:
    trial_details = json.load(f)

system_prompt = """
    Classify the study outcomes into the most relevant CANON_CATEGORIES.
    Return ONLY JSON: {"categories": []}

    Use only these categories:
    [
    "Weight Management",
    "Digestive & Gut Health",
    "Energy",
    "Sports Nutrition",
    "Joint & Mobility",
    "Cognitive Health",
    "Immune Health",
    "Hair, Skin & Nails",
    "Men's Wellness",
    "Women's Wellness",
    "Prenatal & Postnatal",
    "Liver & Detox",
    "Sleep & Relaxation",
    "Stress & Mood",
    "Bone Health",
    "Heart Health",
    "Blood Sugar Support",
    "Healthy Aging",
    "Vision & Eye Health",
    "Inflammation & Pain"
    ]

    Read the outcome measures + descriptions and choose all relevant categories.
    No explanations. Only return {"categories": [...]}.
"""

for td in trial_details:
    print(f"[INFO] generating categories for study {td["nctId"]}")
    all_study_outcomes = []
    outcomes = td.get("outcome", [])

    if outcomes:
        all_study_outcomes.append(outcomes)

    # print(outcomes)

    
    try:
        payload = {
            "model": "gpt-5-mini",
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(all_study_outcomes)}
            ]
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENAI_API_KEY}",
            },
            timeout=180
        )

        if response is None:
            raise Exception("No response returned from OpenAI")

        if response.status_code >= 400:
            raise Exception(f"Bad status code: {response.status_code} — {response.text}")

        ai = response.json()

        if "choices" not in ai:
            raise Exception("Missing 'choices' field in response")

        content = ai["choices"][0]["message"].get("content")
        if not content:
            raise Exception("Empty content returned from model")

        categories = json.loads(content)

    except Exception as e:
        print(f"Upstream error: {e}", 502)

    td["categories"] = categories.get("categories", [])

with open("simplified_data_ashwagandha.json", "w", encoding="utf-8") as f:
    json.dump(trial_details, f, indent=2, ensure_ascii=False)
