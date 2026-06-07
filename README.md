# AI Powered Accounting Assistant

A Django-based application that helps automate bookkeeping workflows for small accounting firms through AI-powered invoice processing and accounting automation.
## Overview

This project combines traditional accounting workflows with Large Language Models (LLMs) to reduce manual work involved in processing invoices and accounting documents.

Users can upload invoices as images or PDFs, automatically extract relevant information using AI, manage client companies, create accounting verifications, and generate SIE files for export to accounting systems.

## Highlights

- AI-powered invoice extraction using OpenAI
- PDF and image invoice processing
- Client and invoice management
- Accounting verification (verifikation) handling
- SIE file generation
- Built with Django, Python, Bootstrap, and OpenAI APIs

---

## Key Features

### Document Processing

* Upload invoices as PDF or image files
* Automatic extraction of invoice information using OpenAI APIs
* Preview uploaded files directly in the browser

### Client Management

* Manage multiple client companies
* Store company information
* Organize accounting data per client

### Invoice Management

* Store incoming invoices
* Link invoices to clients
* Track invoice metadata and extracted information

### Accounting Verification Management

* Create and manage verifications (verifikationer)
* Store accounting entries
* Maintain bookkeeping records

### AI-Assisted Bookkeeping

* Extract:
  * Supplier information
  * Invoice numbers
  * Dates
  * Amounts
  * VAT information
* Assist accountants in creating bookkeeping entries
* Reduce manual data entry

### SIE Export

* Generate SIE files
* Export accounting data for use in external accounting systems
* Support accountant workflows

---

## Technology Stack

### Backend

* Django
* Python
* Django ORM
* SQLite / PostgreSQL

### AI & Document Processing

* OpenAI API
* Large Language Models (LLMs)
* PDF Processing
* OCR / Document Analysis

### Frontend

* HTML
* CSS
* Bootstrap
* JavaScript

### Storage

* File uploads
* PDF storage
* Invoice image storage

---

## System Architecture

1. User uploads an invoice (PDF or image).
2. The document is stored securely.
3. OpenAI processes the document and extracts accounting-relevant information.
4. Extracted data is presented to the user for review.
5. The user creates or updates accounting records.
6. Accounting data can be exported as SIE files.

---

## Screenshots

Will be filled later

---

### 1. Clone the repository

```bash
git clone https://github.com/almalekbilal85-wq/accounting-ai-invoices.git
cd accounting-ai-invoices
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variables
Create a `.env` file and add:

API_KEY=your_openai_api_key_here

⚠️ The API key is not included in this repository and must be provided by the user.

### 5. Run migrations and start server
python manage.py migrate

python manage.py runserver
