import pandas as pd
import json
import google.generativeai as genai

# 1. Setup Gemini client
genai.configure(api_key="AIzaMyByWnYsIs7TfMPWq4wKubs") 
model = genai.GenerativeModel("gemini-1.5-flash")


# 2. Load CSV & clean headers
df = pd.read_csv(r"C:\openai\HDHI Admission data.csv")

# Normalize column names: strip spaces, force uppercase
df.columns = df.columns.str.strip().str.upper()


# 3. Define condition columns (normalized to uppercase too)
condition_cols = [
    'DM', 'HTN', 'CAD', 'CKD', 'ANAEMIA', 'SEVERE ANAEMIA',
    'HEART FAILURE', 'HFREF', 'HFNEF', 'VALVULAR', 'STABLE ANGINA',
    'ACS', 'STEMI', 'ATYPICAL CHEST PAIN', 'CHB', 'SSS', 'AKI',
    'CVA INFRACT', 'CVA BLEED', 'AF', 'VT', 'PSVT', 'CONGENITAL',
    'UTI', 'NEURO CARDIOGENIC SYNCOPE', 'ORTHOSTATIC',
    'INFECTIVE ENDOCARDITIS', 'DVT', 'CARDIOGENIC SHOCK',
    'SHOCK', 'PULMONARY EMBOLISM', 'CHEST INFECTION'
]

records = []

# 4. Iterate rows & build prompts
for idx, row in df.iterrows():
    conditions = [col for col in condition_cols if row.get(col, 0) == 1]
    conditions_str = ", ".join(conditions) if conditions else "none reported"

    smoking = "smoker" if row.get("SMOKING", 0) == 1 else "non-smoker"
    alcohol = "alcoholic" if row.get("ALCOHOL", 0) == 1 else "non-alcoholic"

    prompt = (
        f"The patient is {row['AGE']} years old, "
        f"{'male' if row['GENDER'] == 'M' else 'female'}, "
        f"from {'rural' if row['RURAL']=='R' else 'urban'} area, "
        f"admitted through {'emergency' if row['TYPE OF ADMISSION-EMERGENCY/OPD']=='E' else 'OPD'}. "
        f"They stayed {row['DURATION OF STAY']} days. "
        f"Lifestyle history: {smoking}, {alcohol}. "
        f"Medical conditions: {conditions_str}. "
        f"Key labs: HB={row['HB']}, Glucose={row['GLUCOSE']}, Urea={row['UREA']}, Creatinine={row['CREATININE']}. "
        f"Outcome: {row['OUTCOME']}."
    )

    # Show thinking message
    print(f"[{idx+1}/{len(df)}] Thinking...", end="\r", flush=True)
    print(prompt)

    try:
        response = model.generate_content(prompt)
        summary = response.text if response and response.text else ""
    except Exception as e:
        summary = f"Error generating summary: {e}"

    records.append({
        "prompt": prompt,
        "summary": summary
    })

# 5. Save JSON
with open("patient_summaries.json", "w", encoding="utf-8") as f:
    json.dump(records, f, indent=4, ensure_ascii=False)

print("\n✅ Done. JSON saved as patient_summaries.json")

