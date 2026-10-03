Chemical Information Web Scraping and Data Collection
Overview
This project is a collection of Python-based web scraping and document collection scripts developed during an internship focused on chemical and environmental information.
The scripts access different Japanese and international chemical information resources, identify relevant documents, and download available PDF, HTML, ZIP, and other supporting files for further analysis and reference.
Project Objectives
- Collect chemical-related information from online sources.
- Automate the downloading of publicly available chemical documents.
- Extract and organize chemical reference materials.
- Collect information based on CAS numbers where applicable.
- Maintain downloaded documents in structured folders.
- Support further chemical data analysis and research.
Technologies Used
- Python
- Selenium – browser automation and webpage access
- Requests – HTTP requests and file downloads
- BeautifulSoup – HTML parsing and link extraction
- OpenPyXL – Excel file processing
- Pandas – data handling
- Chrome / ChromeDriver
Project Structure
EBP/
│
├── chem1-1.py
├── chem1-2_1.py
├── chem6_.py
├── chem9.py
├── chem9-1.py
├── chem9-2.py
├── chem12_1.py
├── chem15.py
├── chem22-1.py
├── chem22-2.py
│
├── chem1/
├── chem1-2/
├── chem6/
├── chem9/
├── chem9-1/
├── chem9-2/
├── chem12/
├── chem15/
├── chem22-1/
├── chem22-2/
│
├── AI rag/
├── qsar (isha)/
├── Japan/
├── log/
│
├── assessment sheet.xlsx
├── casno for test.xlsx
└── title9.txt

Script Description
chem1-1.py
Collects chemical-related documents from specified environmental information webpages and downloads the available linked files.
chem1-2_1.py
Processes CAS numbers from an Excel file and searches the relevant chemical information source for corresponding documents.
It automatically downloads available PDF documents and stores debugging HTML files when required.
chem6_.py
Collects information related to Lead (CAS: 7439-92-1) from chemical information resources and saves the retrieved HTML documents.
chem9.py
Accesses AIST chemical risk information pages, extracts PDF links, and downloads available documents.
chem9-1.py
Performs another structured collection of AIST chemical reference documents and saves the downloaded PDFs.
chem9-2.py
Processes multiple AIST chemical information pages and downloads available supporting documents, including:
- Executive summaries
- Appendices
- Reference tables
- Supporting PDF documents
- ZIP files
chem12_1.py
Automates collection of chemical-related information from its configured source.
chem15.py
Automates document retrieval from its configured chemical information source.
chem22-1.py and chem22-2.py
Additional chemical information collection scripts used for retrieving and organizing relevant online documents.
Data Sources
The project works with chemical information obtained from sources including:
- Japanese environmental information websites
- AIST – National Institute of Advanced Industrial Science and Technology
- Chemical reference databases
- Other configured chemical information webpages
Input Data
Some scripts use Excel files containing chemical identifiers such as CAS Registry Numbers (CAS RN).
Example:
CAS Number
117-81-7
85-68-7
103-23-1
126-73-8

These identifiers are used by the scripts to locate relevant chemical information.
Output
Depending on the script, the collected information may include:
- PDF documents
- HTML documents
- ZIP files
- Chemical reference documents
- Supporting tables
- Executive summaries
- Debugging HTML pages
The output is organized into separate folders corresponding to each chemical information collection script.
Workflow
Input Chemical Data / Target URLs
              ↓
       Python Script
              ↓
   Website / Database Access
              ↓
   HTML Parsing / CAS Search
              ↓
      Find Download Links
              ↓
      Download Documents
              ↓
     Organize Local Files
              ↓
      Further Analysis

Installation
Clone the repository:
git clone https://github.com/srishti0120/EBP.git

Navigate to the project:
cd EBP

Install the required Python packages:
pip install selenium beautifulsoup4 requests openpyxl lxml pandas

Running the Scripts
For example:
python chem1-2_1.py

or:
python chem9.py

Individual scripts can be executed according to the required chemical information source.
Notes
- Some source websites contain older or unavailable documents. Therefore, individual downloads may return errors such as HTTP 404 when a document no longer exists.
- Some webpages may require browser automation using Selenium.
- Downloaded files are stored in their respective project folders.
- Internet access is required when running the web-scraping scripts.
- The exact output depends on the availability and structure of the source websites at the time of execution.
Internship Project
This repository contains the scripts, datasets, and supporting files developed and used during the internship for automated collection and organization of chemical information.
