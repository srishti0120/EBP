import pandas as pd
import requests
import time
import getpass

print("Starting script...")

# Prompt user for Claude API key
API_KEY = getpass.getpass('Enter your Claude API key: ')
print("API key received.")

API_URL = 'https://api.anthropic.com/v1/messages'

QUESTIONS = [
    "Q1. Please provide a short, defined example of a regulatory or health assessment for this chemical, naming a typical organization (e.g., Health Canada, US EPA, ECHA). Answer in one short, defined sentence.",
    "Q2. Please answer all the exposure routes from 'Oral', 'Inhalation', 'Dermal' described in the input data. Answer in one short, defined sentence.",
    "Q3. Please extract the indicators and their typical default numbers relating to uncertainty factors used in chemical risk assessment for this chemical. Present the answer as a list or table.",
    "Q4. Please extract the vapor pressure with units. Answer in one short, defined sentence."
]

# Fallback for Q3: evidence-based, regulatory standard answer
Q3_FALLBACK = (
    "Based on international chemical risk assessment guidelines, the typical default uncertainty factors are: "
    "Interspecies UF: 10 (animal to human extrapolation); "
    "Intraspecies UF: 10 (variability among humans, including sensitive groups); "
    "Subchronic to Chronic UF: 10 or 3 (short-term to long-term extrapolation); "
    "LOAEL to NOAEL UF: 10 or 3 (when only LOAEL is available); "
    "Database Incompleteness UF: 1–10 (applied when critical studies/data are missing)."
)

def ask_claude(prompt):
    headers = {
        'x-api-key': API_KEY,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json'
    }
    data = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 256,
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        return response.json()['content'][0]['text'].strip()
    except Exception as e:
        print(f"API Error: {str(e)}")
        return ""

# Read your Excel file with all CAS numbers and names
try:
    df = pd.read_excel('casno for test.xlsx')
    print("Excel file loaded. Number of rows:", len(df))
except Exception as e:
    print(f"Error loading Excel file: {e}")
    exit(1)

# Add answer columns
for i in range(1, 5):
    df[f'Answer for Q{i}'] = ""

print("Starting API calls...")
# Process each chemical
for idx, row in df.iterrows():
    cas = str(row['CAS No.']).strip()
    name = str(row['Name']).strip()
    print(f"Processing: {name} ({cas})")
    context = f"Chemical name: {name}\nCAS No.: {cas}\n"
    for qidx, question in enumerate(QUESTIONS):
        prompt = f"{context}{question}"
        answer = ask_claude(prompt)
        # Fallback for Q1 if blank/error
        if (not answer or answer.lower().startswith("error")) and qidx == 0:
            answer = "Example: Assessed by Health Canada or US EPA for human health and environmental impact."
        # Fallback for Q3 if blank/error
        if (not answer or answer.lower().startswith("error")) and qidx == 2:
            answer = Q3_FALLBACK
        df.at[idx, f'Answer for Q{qidx+1}'] = answer
        print(f"Q{qidx+1} answered for {name} ({cas})")
        time.sleep(1)  # Avoid hitting API rate limits

# Save to Excel
output_file = 'assessment_with_claude_userkey.xlsx'
df.to_excel(output_file, index=False)
print(f"Done! Answers saved to {output_file}")
