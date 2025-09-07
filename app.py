import pandas as pd
import json
import google.generativeai as genai

# 1. Setup Gemini client
genai.configure(api_key="AIzaSyDJ911ua_R37xjMf17VxgzR1BNRJI8pMYM") 
model = genai.GenerativeModel("gemini-2.5-flash")
input_text = '''A 46-year-old male schoolteacher with a history of hypertension and type 2 diabetes. He leads a mostly sedentary lifestyle, though he occasionally joins his students in cricket matches. His family history is significant for early-onset cardiac disease in his father.
 '''

prompt = f'''
consider yourself as a patient summary extractor in JSON format.
given a patient summary in the form of a string your task is to extract age, medical condition and occupation etc. details in the format of JSON.
consider synonyms while extracting above details, the json format is as below:
{{
    "age": 25,
    "medical condition": ["asthma", "blood cancer"],
    "occupation": ["mining"],
    "families history": "parents have asthma related genetic issue"
}}
if there are no conditions specified just mention NULL.
just return only json, do not return extra information.

patient summary: "{input_text}"
'''

try:
    response = model.generate_content(prompt)
    summary = response.text if response and response.text else ""
except Exception as e:
    summary = f"Error generating summary: {e}"

print(summary)

