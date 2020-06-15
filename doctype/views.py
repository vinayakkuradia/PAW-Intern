from django.shortcuts import render
from django.http import HttpResponse
from . dtdalgo import detect
from . dtdalgo import entityextract
from django.shortcuts import redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def doctype(request):
    x = detect()
    return render(request, 'doctype.html', {'doctype': x})


def home(request):
    response = redirect('/upload/')
    return response

def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        doctype, text = detect(filename)
        return render(request, 'upload.html', {
            'uploaded_file_url': uploaded_file_url,
            'doctype': doctype,
            'text': text
        })
    return render(request, 'upload.html')

'''
def trial(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        doctype, text = detect(filename)
        persons, locations, organizations, phone_numbers, dates, others, extras = entityextract(filename, text)
        return render(request, 'trial.html', {
            'uploaded_file_url': uploaded_file_url,
            'doctype': doctype,
            'text': text,
            'persons': persons,
            'locations': locations,
            'organizations': organizations,
            'phone_numbers': phone_numbers,
            'dates': dates,
            'others': others
        })
    return render(request, 'trial.html')
'''
@csrf_exempt
def trial(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        doctype, text = detect(filename)
        invoice_id, order_id, customer_id, date_issue, amount_total, amount_due, sender_name, sender_address, sender_vat_id, recipient_name, recipient_address, item_description = entityextract(filename)
        return render(request, 'trial.html', {
            'uploaded_file_url': uploaded_file_url,
            'doctype': doctype,
            'invoice_id': invoice_id,
            'order_id': order_id,
            'customer_id': customer_id,
            'date_issue': date_issue,
            'amount_total': amount_total,
            'amount_due': amount_due,
            'sender_name': sender_name,
            'sender_address': sender_address,
            'sender_vat_id': sender_vat_id,
            'recipient_name': recipient_name,
            'recipient_address': recipient_address,
            'item_description': item_description
        })
    return render(request, 'trial.html')