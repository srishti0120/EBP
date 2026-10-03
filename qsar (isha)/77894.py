import csv

input_file = '77894.csv'
output_file = '77894_comma.csv'

encodings = ['utf-8', 'utf-16', 'latin1']
for enc in encodings:
    try:
        with open(input_file, newline='', encoding=enc) as tsvfile:
            reader = csv.reader(tsvfile, delimiter='\t')
            rows = list(reader)
        break
    except UnicodeDecodeError:
        rows = None
        continue
else:
    raise UnicodeDecodeError(f"Could not decode {input_file} with tried encodings: {encodings}")

if not rows or len(rows) < 2:
    raise ValueError("CSV file is empty or only contains headers.")

# Remove column A (index 0) from all rows
rows = [row[1:] for row in rows]

# Get values from row 2 (index 1) for columns B and C (now index 0 and 1)
cas_value = rows[1][0] if len(rows[1]) > 0 else ''
chem_name_value = rows[1][1] if len(rows[1]) > 1 else ''

# Copy these values to all rows (except header), only if the row has enough columns
for i in range(1, len(rows)):
    if len(rows[i]) > 0:
        rows[i][0] = cas_value
    if len(rows[i]) > 1:
        rows[i][1] = chem_name_value

# Write back to CSV with comma delimiter
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerows(rows)

print("Removed column A and copied values from row 2, columns B and C to all rows in columns B and C.")
print(f"Converted {input_file} (tab-separated) to {output_file} (comma-separated).")
