import requests
import PyPDF2

API_KEY = "AIzaSyD88rGRZayjexP05T5yy4LypsMsSqIPjC8"  # Replace with your actual API key
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"


def Censura(temperature: float, pdf_path: str) -> dict:
    """Generates content based on the given prompt text (extracted from a PDF)
    and a temperature parameter to control randomness. It instructs the
    language model to censor personal information in the extracted text.

    Args:
        temperature (float): The temperature parameter for controlling randomness.
        pdf_path (str): The path to the PDF file to process.

    Returns:
        dict: A dictionary containing the API response, which ideally includes
              the censored text.
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
    except FileNotFoundError:
        return {"error": f"File not found at {pdf_path}"}
    except Exception as e:
        return {"error": f"An error occurred during PDF processing: {e}"}

    headers = {
        "Content-Type": "application/json"
    }

    prompt = f"Keep the original language of the following text and act as someone that censures personal information including Name, address, documents, billing information, salary, etc. Replace every personal information word with '*' of the same lenght :\n\n{text}"

    body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": temperature
        }
    }

    response = requests.post(API_URL, headers=headers, json=body)

    return response.json()


output = Censura(0.0, "/home/eduardohp/Desktop/hackathon/nos-gen-ai-hackathon/raw_data/document_to_anonymize.pdf")
print(output)