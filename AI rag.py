import anthropic
import pandas as pd
import getpass

# Step 1: Enter your Anthropic API key securely
api_key = getpass.getpass('Enter your Anthropic API key: ')
client = anthropic.Anthropic(api_key=api_key)

# Step 2: List your CSV files
csv_files = [
    '77-89-4_pubchem.csv', '77-90-7_pubchem.csv','78-51-3_pubchem.csv','84-61-7_pubchem.csv',
    '84-66-2_IRIS_Summary.csv','84-66-2_pubchem.csv','84-74-2_IRIS_Summary.csv','84-74-2_pubchem.csv',
    '85-68-7_IRIS_Summary.csv','85-68-7_pubchem.csv','103-23-1_IRIS_Summary.csv','103-23-1_pubchem.csv',
    '103-24-2_pubchem.csv','105-75-9_pubchem.csv','105-76_pubchem.csv','109-43-3_pubchem.csv',
    '115-86-6_pubchem.csv','117-81-7_IRIS_Summary.csv','117-81-7_pubchem.csv','122-62-3_pubchem.csv',
    '126-73-8_pubchem.csv','131-11-3_IRIS_Summary.csv','131-11-3_pubchem.csv','137-89-3_pubchem.csv',
    '141-17-3_pubchem.csv','141-18-4_pubchem.csv','142-16-5_pubchem.csv','142-16-5_pubchem.csv',
    '6422-86-2_pubchem.csv','26444-49-5_pubchem.csv','26761-40-0_pubchem.csv','27178-16-1_pubchem.csv',
    '27253-26-5_pubchem.csv','28553-12-0_pubchem.csv','33703-08-01_pubchem.csv','85507-79-5_pubchem.csv',
    'Acetyl triethyl citrate_クエン酸三エチル_概要英訳.csv','debug_page.csv','Dibutyl phthalate_フタル酸ジイソデシル（DIDP）_概要英訳.csv',
    'Dibutyl phthalate_フタル酸ジイソノニル（DINP）_概要英訳.csv','Dibutyl phthalate_フタル酸ジブチル（DBP）_概要英訳[Food Safety].csv',
    'Dibutyl phthalate_フタル酸ジブチル（DBP）_概要英訳[Food Safety].csv','Dibutyl phthalate_フタル酸ベンジルブチル（BBP）_概要英訳.csv',
    'Dibutyl phthalate_フタル酸ベンジルブチル（BBP）_概要英訳[Food Safety].csv','Diisodecyl phthalate_フタル酸ジイソデシル（DIDP）_概要英訳.csv',
    'Diisodecyl phthalate_フタル酸ジイソノニル（DINP）_概要英訳.csv','Diisodecyl phthalate_フタル酸ジブチル（DBP）_概要英訳[Food Safety].csv',
    'Diisodecyl phthalate_フタル酸ビス（２－エチルヘキシル）（DEHP）_概要英訳[Food Safety].csv','Diisodecyl phthalate_フタル酸ベンジルブチル（BBP）_概要英訳.csv',
    'Diisodecyl phthalate_フタル酸ベンジルブチル（BBP）_概要英訳.csv','Diisononyl phthalate_フタル酸ジイソデシル（DIDP）_概要英訳.csv',
    'Diisononyl phthalate_フタル酸ジイソノニル（DINP）_概要英訳.csv','Diisononyl phthalate_フタル酸ジブチル（DBP）_概要英訳[Food Safety].csv',
    'Diisononyl phthalate_フタル酸ビス（２－エチルヘキシル）（DEHP）_概要英訳[Food Safety].csv','Diisononyl phthalate_フタル酸ベンジルブチル（BBP）_概要英訳.csv',
    'Diisononyl phthalate_フタル酸ベンジルブチル（BBP）_概要英訳[Food Safety].csv','Dioctyl phthalate_フタル酸ジイソデシル（DIDP）_概要英訳.csv',
    'Dioctyl phthalate_フタル酸ジイソノニル（DINP）_概要英訳.csv','Dioctyl phthalate_フタル酸ジブチル（DBP）_概要英訳[Food Safety].csv',
    'Dioctyl phthalate_フタル酸ビス（２－エチルヘキシル）（DEHP）_概要英訳[Food Safety].csv',
    'Dioctyl phthalate_フタル酸ベンジルブチル（BBP）_概要英訳.csv','Dioctyl phthalate_フタル酸ベンジルブチル（BBP）_概要英訳[Food Safety].csv',
    'Diundecyl phthalate_フタル酸ジブチル（DBP）_概要英訳[Food Safety].csv','eics0052.csv',
    'leadandleadcompounds.csv'
]

def ask_question_about_file(filename, question, n_rows=30):
    try:
        df = pd.read_csv(filename)
    except Exception as e:
        return f"Error reading {filename}: {e}"

    # Use only the first n_rows to avoid token overflow
    data_sample = df.head(n_rows).to_string(index=False)
    user_content = f"CSV data from file '{filename}' (showing first {n_rows} rows):\n{data_sample}\n\nQuestion: {question}"

    system_prompt = "You are a helpful assistant that answers questions based on the provided CSV data."

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        temperature=0,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_content}
        ]
    )
    return response.content

# Step 3: Interactive question loop
while True:
    print("\nAvailable CSV files:")
    for i, fname in enumerate(csv_files):
        print(f"{i+1}: {fname}")

    file_choice = input("Enter the number of the CSV file you want to query (or type 'exit' to quit): ")
    if file_choice.lower() == 'exit':
        break
    try:
        file_idx = int(file_choice) - 1
        if not (0 <= file_idx < len(csv_files)):
            print("Invalid file number. Try again.")
            continue
        chosen_file = csv_files[file_idx]
    except ValueError:
        print("Please enter a valid number.")
        continue

    user_question = input(f"Enter your question about '{chosen_file}' (or type 'exit' to quit): ")
    if user_question.lower() == 'exit':
        break

    answer = ask_question_about_file(chosen_file, user_question)
    print('\nAnswer from Claude:')
    print(answer)
