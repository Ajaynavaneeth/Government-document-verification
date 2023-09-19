from roboflow import Roboflow
import pytesseract
import cv2
import PyPDF2
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
rf = Roboflow(api_key="MeqIAerEsfqqP0iUlZj6")
project = rf.workspace().project("stamp-v2")
model = project.version(1).model
def is_stamp_present(image_path, confidence_threshold=40, overlap_threshold=30):
    try:
        predictions = model.predict(image_path, confidence=confidence_threshold, overlap=overlap_threshold).json()

        if len(predictions["predictions"]) > 0:
            detected_class = predictions["predictions"][0]["class"]
            if detected_class.lower() == "stamp":
                return "government docx"
            else:
                return "Non-government docx"

        return "Non-government docx"
    except Exception as e:
        print(f"Error checking stamp presence: {str(e)}")
        return "Non-government docx"

def preprocess_image(image_path):
    try:
        image = cv2.imread(image_path)
        # Resize the image for better OCR performance
        image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray
    except Exception as e:
        print(f"Error preprocessing image: {str(e)}")
        return None

def extract_text_from_image(image_path, language='eng'):
    try:
        gray = preprocess_image(image_path)
        if gray is not None:
            text = pytesseract.image_to_string(gray, lang=language)
            return text
        else:
            return None
    except Exception as e:
        print(f"Error extracting text from image: {str(e)}")
        return None

def extract_text_from_pdf(pdf_path, language='eng'):
    try:
        pdf_file = open(pdf_path, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        text = ""
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            text += page.extractText()
        pdf_file.close()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        return None

def is_legal_document(text):
    keywords = [
            "legal", "contract", "agreement", "signature", "india non judicial", "india",
    "government", "official", "public", "administration", "public service",
    "policy", "regulation", "authority", "agency", "department", "ministry",
    "legislation", "act", "bill", "ordinance", "gazette", "directive", "law",
    "constitution", "parliament", "council", "committee", "commission",
    "governmental", "executive", "legislative", "judicial", "public interest",
    "public welfare", "public opinion", "civil service", "public administration",
    "public policy", "social service", "healthcare", "education", "welfare",
    "social security", "housing", "international relations", "diplomacy", "treaty",
    "defense", "national security", "security policy", "homeland security",
    "intelligence", "immigration", "border control", "visa", "citizenship",
    "refugee", "environment", "conservation", "sustainability", "climate change",
    "infrastructure", "transportation", "urban planning", "election", "democracy",
    "voting", "political party", "human rights", "civil liberties", "freedom of speech",
    "freedom of assembly", "equality", "public records", "transparency", "accountability",
    "government procurement", "public contract", "government grant", "public funding",
    "government audit", "government subsidy", "government program", "government project",
    "government report", "government investigation", "government regulation",
    "government decision", "government review", "government assessment", "government policy",
    "government directive", "government announcement", "government publication",
    "government gazette", "government agency", "government department", "government ministry",
    "government commission", "government council", "government committee",
    "government task force", "government order", "government law", "government code",
    "government constitution", "government charter", "government treaty", "government agreement",
    "government contract", "government decision", "government declaration",
    "government notice", "government hearing", "government session", "government forum",
    "government summit", "government convention", "government protocol", "government strategy",
    "government plan", "government budget", "government expenditure", "government revenue",
    "government tax", "government fee", "government fine", "government license",
    "government permit", "government certification", "government registration",
    "government inspection", "government audit", "government investigation",
    "government enforcement", "government compliance", "government review",
    "government assessment", "government evaluation", "government performance",
    "government monitoring", "government oversight", "government accountability",
    "government transparency", "government ethics", "government compliance",
    "government data", "government records", "government document", "government archive",
    "government database", "government information", "government publication",
    "government website", "government portal", "government platform", "government service",
    "government program", "government initiative", "government project", "government grant",
    "government subsidy", "government fund", "government loan", "government contract",
    "government agreement", "government partnership", "government collaboration",
    "government cooperation", "government coordination", "government communication",
    "government engagement", "government consultation", "government feedback",
    "government survey", "government assessment", "government report", "government analysis",
    "government research", "government study", "government investigation",
    "government evaluation", "government review", "government benchmark",
    "government indicator", "government scorecard", "government ranking",
    "government benchmarking", "government best practices", "government standards",
    "government guidelines", "government protocol", "government strategy",
    "government plan", "government policy", "government directive", "government decision",
    "government action", "government implementation", "government execution",
    "government monitoring", "government enforcement", "government compliance",
    "government evaluation", "government improvement", "government reform",
    "government innovation", "government modernization", "government efficiency",
    "government effectiveness", "government performance", "government accountability",
    "government transparency", "government ethics", "government sustainability",
    "government resilience", "government inclusiveness", "government diversity",
    "government accessibility", "government public service", "government citizen service",
    "government community service", "government public welfare", "government civic engagement",
    "government citizen engagement", "government public participation", "government democracy",
    "government governance", "government leadership", "government public trust",
    "government public opinion", "government public perception", "government public satisfaction",
    "driving licence", "union of india"
    ]

    text_lower = text.lower()
    for keyword in keywords:
        if keyword.lower() in text_lower:
            return True
    return False

def verify_indian_language_document(document_path):
    indian_languages = ["eng", "hin", "ben", "tam", "tel", "kan", "mal", "pan", "guj", "ori", "urd"]
    text = None
    
    if document_path.lower().endswith('.pdf'):
        text = extract_text_from_pdf(document_path)
    else:
        text = extract_text_from_image(document_path)

    if text is not None:
        for language in indian_languages:
            if is_legal_document(text):
                return True
    return False


# Input the image
image_path = "6.jpg"



result = is_stamp_present(image_path)
if result == "Non-government docx":
    text = extract_text_from_image(image_path)
    if text is not None:
        if is_legal_document(text):
            print("The document appears to be legal.")
        else:
            print("The document does not appear to be legal.")
    else:
        print("Failed.")
else:
    print("The document appears to be legal.")
