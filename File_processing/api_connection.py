from .image_processing import getOCRtext
from .pdf_processing import readPdfText
from dotenv import load_dotenv
import os

from openai import OpenAI



system = "You are an accounting assistant specialized in Swedish bookkeeping using the BAS chart of accounts. " \
"Your task is to extract data from an OCR invoice and generate accounting entries." \
"Rules:" \
"- Return ONLY valid JSON that follows the provided schema." \
"- Do NOT include any explanations or text outside the JSON." \
"- All amounts must be numbers (not strings)." \
"- Ensure accounting entries are balanced (total debit = total credit)." \
"- Use Swedish BAS accounts:" \
"  - 2440 for supplier liabilities" \
"  - 2641 for input VAT" \
"  - Choose an appropriate cost account based on the invoice content (e.g. 5030 for utilities like water, electricity, heating)." \
"- VAT must be calculated correctly based on the invoice." \
"- If information is missing or unclear, make a reasonable assumption but stay consistent." \
"- Do not invent extreme values or unrealistic data." \
"Behavior:" \
"- Extract: invoice number, dates, amounts, VAT, supplier." \
"- Classify the expense type." \
"- Generate correct accounting entries." 

instructions_dic = {
    "format": {
        "type": "json_schema",
        "name": "invoice_accounting",
        "strict": True,
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "invoice_number": {"type": "string"},
                "invoice_date": {"type": "string"},
                "total_amount": {"type": "number"},
                "vat_amount": {"type": "number"},
                "accounting_entries": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "account": {"type": "string"},
                            "debit": {"type": "number"},
                            "credit": {"type": "number"}
                        },
                        "required": ["account", "debit", "credit"]
                    }
                }
            },
            "required": [
                "invoice_number",
                "invoice_date",
                "total_amount",
                "vat_amount",
                "accounting_entries"
            ]
        }
    }
}

def getTextFromFile(file, file_type):
    invoice_text = ''

    if file_type == 'jpeg' or file_type == 'png':
        invoice_text = getOCRtext(file)
    else:
        invoice_text = readPdfText(file)

    return invoice_text
    

def getAIOutput(file, file_type):

    invoice_text = getTextFromFile(file, file_type)

    user_text = "Here is an OCR-extracted invoice. Process it according to the rules." \
    "--- INVOICE START --- " + invoice_text + "--- INVOICE END ---"

    # Change the api key to be secure


    load_dotenv()  

    api_key = os.getenv("API_KEY")
    
    client = OpenAI(
    api_key=api_key
    )

    # make model changabe
    response = client.responses.create(
    model="gpt-5.4",
    input=[
        {"role": "system", "content": system},
        {"role": "user", "content": user_text}
        ],
        text=instructions_dic,
    store=True,
    )

    return response.output_text
        