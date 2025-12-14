import os
import requests

# Folder to save files
save_folder = r'C:\Users\srish\OneDrive\Desktop\internship\chem6\pdf\7439-92-1'
os.makedirs(save_folder, exist_ok=True)

# List of lead document URLs with their official titles
lead_docs = [
    ("Lead, inorganic (PIM 301)", "https://www.inchem.org/documents/pims/chemical/inorglea.htm"),
    ("Lead and Lead Compounds (IARC Summary & Evaluation, Supplement7, 1987)", "https://www.inchem.org/documents/iarc/suppl7/leadandleadcompounds.html"),
    ("Lead (EHC 3, 1977)", "https://www.inchem.org/documents/ehc/ehc/ehc003.htm"),
    ("Lead (UKPID)", "https://www.inchem.org/documents/ukpids/ukpids/ukpid25.htm"),
    ("Lead (WHO Food Additives Series 44)", "https://www.inchem.org/documents/jecfa/jecmono/v44jec12.htm"),
    ("Lead (ICSC)", "https://www.inchem.org/documents/icsc/icsc/eics0052.htm"),
    ("Lead (WHO Food Additives Series 21)", "https://www.inchem.org/documents/jecfa/jecmono/v21je16.htm"),
    ("Lead (WHO Food Additives Series 13)", "https://www.inchem.org/documents/jecfa/jecmono/v13je13.htm"),
    ("Lead (WHO Food Additives Series 4)", "https://www.inchem.org/documents/jecfa/jecmono/v004je03.htm")
]

for title, url in lead_docs:
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        # Get filename from URL
        filename = os.path.basename(url)
        filepath = os.path.join(save_folder, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {title} -> {filepath}")
    except Exception as e:
        print(f"Failed to download {title}: {str(e)}")