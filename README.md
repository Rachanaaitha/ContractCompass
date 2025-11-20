# ContractCompass

AI-powered legal contract analysis tool that automatically extracts obligations, deadlines, and risks from contracts.

## Project Overview

ContractCompass is an automated legal contract review system that uses AI and workflow automation to streamline the contract analysis process for legal and compliance teams.

## Features

- Document Processing: PDF and DOCX contract upload and text extraction
- AI Analysis: Rule-based intelligence for contract review and analysis
- Risk Assessment: Automated risk flagging and classification
- Workflow Automation: n8n integration for alerts and notifications
- Structured Output: Extraction of dates, obligations, financial terms, and summaries

## Technology Stack

- Frontend: Streamlit
- Backend: Python
- Document Processing: PyPDF2, python-docx
- Workflow Automation: n8n
- AI: Rule-based pattern matching

## Installation

```bash
git clone https://github.com/Rachanaaitha/ContractCompass.git
cd ContractCompass
pip install -r requirements.txt
streamlit run app/main.py
```

## Usage

1. Upload a contract file (PDF or DOCX format)
2. View the extracted text from the document
3. Click "Analyze Contract" to run AI analysis
4. Review the extracted obligations, dates, risks, and financial terms
5. High-risk contracts will trigger n8n workflow simulations for alerts

## Project Structure

```
contractcompass/
├── app/
│   ├── main.py              # Streamlit application
│   ├── utils.py             # PDF and DOCX text extraction
│   └── llm_processor.py     # AI analysis engine
├── workflows/
│   └── n8n_workflow.json    # n8n automation workflow
├── requirements.txt
└── README.md
```

## JD Requirement Coverage

- Work with department teams to understand workflows: Analyzed legal team contract review processes
- Conduct structured requirement-gathering sessions: Identified key pain points in manual contract review
- Use n8n to design and prototype workflow automations: Implemented automated alert system for high-risk contracts
- Analyze processes to classify tasks: Differentiated between automatable and human-judgment tasks
- Evaluate data feasibility: Handled PDF and DOCX document processing challenges
- Support in prioritizing opportunities: Focused on high-impact features first
- Document findings and recommendations: Comprehensive project documentation
- Research emerging AI tools: Implemented rule-based AI with workflow automation

## Business Impact

- Reduces contract review time from hours to minutes
- Automates risk detection and compliance tracking
- Provides consistent analysis across all contracts
- Enables legal teams to focus on high-value strategic work

## License

This project is open source and available under the MIT License.
