#Importing Libraries
#import cv2
import os
import re
import pytesseract
import textract
import PyPDF2
from PIL import Image
from docdata.models import RawData
#Google Cloud APIs requirements
from google.cloud import language_v1
from google.cloud.language_v1 import enums
from google.oauth2 import service_account
from google.protobuf.json_format import MessageToJson

#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#Defining terms for documents
certTerms = ['cerificate', 'certify', 'certify that', 'to whom', 'to whomsoever', 'it may concern', 'certified', 'awarded', 'awarded to', 'presented', 'presented to', 'completed', 'successful', 'completion', 'appreciation', 'participation', 'completion', 'completition of']
legTerms = ['affidavit', 'bail bond', 'bond', 'case citation', 'condition', 'contract', 'party', 'parties', 'defence', 'law', 'order', 'claim', 'parol', 'patent', 'petition', 'restraining', 'clause', 'terms', 'will', 'warranty', 'witness', 'testimony', 'sentenc', 'mediation', 'interrog', 'felony', 'damages', 'agreement', 'court', 'rights', 'section', 'declar', 'memorandum', 'contract', 'policy', 'lease', 'rent']
medTerms = ['medi', 'medical', 'examin', 'person', 'patient', 'health', 'examination', 'practitioner', 'disease', 'suffer', 'hospital', 'emergency', 'vaccin', 'care', 'pathology', 'report', 'condition', 'physical', 'mental', 'doctor', 'dr', 'analysis', 'blood', 'specialist', 'clinic', 'symptom']
billTerms = ['account', 'bill', 'billing', 'due', 'total', 'amount', 'supply', 'service', 'tax', 'customer', 'description', 'units', 'charge', 'payment', 'balance', 'gst', 'goods', 'packing', 'cash', 'cheque', 'rate', 'item', 'qty', 'quantity', 'transaction', 'uses', 'particulars', '[0-9]', '[0-9]\.?[0-9]?', '[A-Z]\d']


def entityextract(filename, text):
    #Cleaning Text
    text = str(text)
    text = text.rstrip("\n")
    text = text.replace("\\n", " ")
    text = text.replace("b'", "")
    text = text.replace("b\"", "")
    text = text.replace("'", "")
    text = text.replace("\"", "")

    #Output Variables for Google API
    persons, locations, organizations, phone_numbers, dates, others, extras = [], [], [], [], [], [], []

    #Creating Credentials and API Client
    credentials = service_account.Credentials.from_service_account_file('intern_project/intern_project/credentials.json')
    client = language_v1.LanguageServiceClient(credentials=credentials)

    # Available types: PLAIN_TEXT, HTML
    type_ = enums.Document.Type.PLAIN_TEXT
    #language = "en"
    document = {"content": text, "type": type_}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = enums.EncodingType.UTF8

    response = client.analyze_entities(document, encoding_type=encoding_type)

    #Entry to Database
    RawData.objects.create(source_file=filename, json_data=MessageToJson(response))

    # Loop through entitites returned from the API
    for entity in response.entities:
        if (enums.Entity.Type(entity.type).name == "PERSON"):
          persons.append(entity.name)
        elif (enums.Entity.Type(entity.type).name == "LOCATION"):
          locations.append(entity.name)
        elif (enums.Entity.Type(entity.type).name == "ORGANIZATION"):
          organizations.append(entity.name)
        elif (enums.Entity.Type(entity.type).name == "PHONE_NUMBER"):
          phone_numbers.append(entity.name)
        elif (enums.Entity.Type(entity.type).name == "DATE"):
          dates.append(entity.name)
        elif (enums.Entity.Type(entity.type).name == "OTHER"):
          others.append(entity.name)
        else:
          extras.append(entity.name)

    return (persons, locations, organizations, phone_numbers, dates, others, extras)

def imgtopdf(filename):
    image = Image.open('intern_project/doctype/media/' + filename)
    process = image.convert('RGB')
    process.save('intern_project/doctype/media/' + filename[:-4] + ".pdf")

def readimg(filename):
    #Loading Image
    #img = cv2.imread('./media/2.jpg')

    #Extracting text from Image
    text = pytesseract.image_to_string('intern_project/doctype/media/'+filename)
    imgtopdf(filename)
    return text

def readpdf(filename):
    #Loading File
    path = os.getcwd() + '/intern_project/doctype/media/' + filename
    pdfFileObj = open(path,'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    #Reading PDF Pages
    num_pages = pdfReader.numPages
    count = 0
    text = ""
    #The while loop will read each page.
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count +=1
        text += pageObj.extractText()

    #Switching method if the above one did not work
    if text != "":
       text = text
    else:
       text = textract.process(path, method='tesseract', language='eng')

    #Converting text to str & Cleaning text for API
    text = str(text)
    text = text.replace("\n", " \n ")
    return text

def analyze(text):
    #Initializing word detect count to 0
    certificate = 0
    legal = 0
    medical = 0
    bill = 0

    #Matching words with document
    for element in certTerms:
        x = re.findall(element, text, re.IGNORECASE)
        if len(x)>0:
          certificate = certificate + 1

    for element in legTerms:
        x = re.findall(element, text, re.IGNORECASE)
        if len(x)>0:
          legal = legal + 1

    for element in medTerms:
        x = re.findall(element, text, re.IGNORECASE)
        if len(x)>0:
          medical = medical + 1

    for element in billTerms:
        x = re.findall(element, text, re.IGNORECASE)
        if len(x)>0:
          bill = bill + 1

    #Identifying document type

    var = [certificate, legal, medical, bill]
    occurance = max(var)

    if occurance == certificate and occurance>0:
        doctype = 'Certificate'
    elif occurance == legal and occurance>0:
        doctype = 'Legal'
    elif occurance == medical and occurance>0:
        doctype = 'Medical'
    elif occurance == bill and occurance>0:
        doctype = 'Bill'
    else:
        doctype = 'Unidentified'

    return  doctype

def detect(filename):
    text = ""
    doctype = ""
    if(re.findall('.pdf', filename, re.IGNORECASE)):
        text = readpdf(filename)
    else:
        text = readimg(filename)
    doctype = analyze(text)
    return (doctype, text)
