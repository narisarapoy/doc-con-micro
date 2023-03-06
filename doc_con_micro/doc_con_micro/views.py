from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from .models import Department, RequestDocument
import datetime
import uuid

def signIn(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request, 
            username=username,
            password=password
        )

        if user is not None:
            # Log user in
            login(request, user)
            next_page = request.POST['next_page']
            next_page = next_page.replace(".djt.html", "")
            next_page = "/" + next_page
            print(next_page)
            if next_page != "/":
                return redirect(next_page)
            return redirect("/documents")
        messages.error(request, 'Invalid Login')
        
    context = {
        'next_page': request.GET.get('next')
    }        
    return render(request, 'login.djt.html', context) 

def signOut(request):  
    # Sign user out
    logout(request)
    return redirect("/documents")

def checkLogin(request, page, context):
    if request.user.is_authenticated == False:
        return redirect("/login?next=" + page)

    return render(request, page, context) 

def documents(request):
    type = request.GET.get('type')
    request_doc_items = None
    if type == 'all' or type == None:
        request_doc_items = RequestDocument.objects.all()
    elif type == 'not-complete':
        request_doc_items = RequestDocument.objects.filter(Q(progress=1)|Q(progress=2)|Q(progress=3)|Q(progress=4))
    elif type == 'complete':
        request_doc_items = RequestDocument.objects.filter(Q(progress=5))
    context = {
        'request_doc_items': reversed(request_doc_items)
    }
    logout(request)
    return render(request, 'documents.djt.html', context)

def requestDoc(request):
    if request.method == "GET":
        if request.GET.get('id') != None:
            id = request.GET.get('id')
            requestDoc = RequestDocument.objects.filter(id=id)
            
            context= {
                'current_date': requestDoc[0].submit_date,
                'request_doc': requestDoc[0],
            }
            if request.user.is_authenticated == False:
                return redirect("/login?next=" + "request-document?id=" + id)
            else:
                logout(request)
                return render(request, 'request_document.djt.html', context)
            # return checkLogin(request, 'request_document.djt.html', context)
        else:
            now = datetime.datetime.now()
            context= {
               'current_date': now.date().strftime("%d/%m/%Y"),
            }
            if request.user.is_authenticated == False:
                return redirect("/login?next=" + "request-document")
            else:
                logout(request)
                return render(request, 'request_document.djt.html', context)
            # return checkLogin(request, 'request_document.djt.html', context)
    else:
        now = datetime.datetime.now()
        context= {
            'current_date': now.date().strftime("%d/%m/%Y"),
        }
        return checkLogin(request, 'request_document.djt.html', context)

def submitDoc(request):
    if 'submit' in request.POST:
        requestDoc = RequestDocument()
        updateRequestDocument(request, requestDoc)
    elif 'edit' in request.POST:
        requestDoc = RequestDocument.objects.filter(id=request.POST['id'])[0]
        updateRequestDocument(request, requestDoc)
    
    return redirect("/logout")

def submitDepartment(request):
    for _topic in Department.objects.all():
        print(_topic.name_en)
    # department = Department(id=uuid.uuid1())
    # department.name_en = "aa"
    # department.name_th = "bb"
    # department.save()
    return HttpResponse()

def updateRequestDocument(request, requestDoc):
    submit_date = request.POST['submit_date']
    department = request.POST['department']
    telephone = request.POST['telephone']
    req_new = request.POST['req_new']
    req_cancel = request.POST['req_cancel']
    req_doctype_control = request.POST['req_doctype_control']
    req_doctype_uncontrol = request.POST['req_doctype_uncontrol']
    req_alter = request.POST['req_alter']
    req_other = request.POST['req_other']
    req_type = 0
    if 'req_type' in request.POST:
        req_type = request.POST['req_type']
    # request_user_id = 
    attached_doc = False

    if 'attached_doc' in request.POST :
        if request.POST['attached_doc'] == "1":
            attached_doc = False
        else:
            attached_doc = True
    print(attached_doc)
    approved = None
    if 'approved' in request.POST :
        if request.POST['approved'] == "1":
            approved = True
        else:
            approved = False
    approved_name = request.POST['approved_name']

    response_type = 0
    if 'response' in request.POST:
        response_type = request.POST['response']
    
    response_code = request.POST['response_code']
    # master_list_cancel = request.POST['master_list_cancel']
    # master_list_edit = request.POST['master_list_edit']
    response_other = request.POST['response_other']
    response_name = request.POST['response_name']
    response_date = ""
    if response_name != requestDoc.response_name or response_type != requestDoc.response_type or response_other != requestDoc.response_other:
        response_date = request.POST['response_date']

    response_original_number = False
    if 'response_original_number' in request.POST:
        response_original_number = True

    request_name = request.POST['request_name']
    request_position = request.POST['request_position']

    request_date = ""
    if 'request_date' in request.POST:
        request_date = request.POST['request_date']

    receive_name = request.POST['receive_name']
    receive_date = ""
    if receive_name != requestDoc.receive_name or response_original_number != requestDoc.response_original_number:
        receive_date = request.POST['receive_date']
    
    control_type = 0
    if 'control' in request.POST:
        control_type = request.POST['control']

    # control_receive_complete_file = request.POST['control_receive_complete_file']
    # control_keep_original_and_restore_copy = request.POST['control_keep_original_and_restore_copy']
    # control_destroy_copy = request.POST['control_destroy_copy']
    # control_send_copy = request.POST['control_send_copy']
    control_name = request.POST['control_name']
    
    control_date = ""
    if control_type != requestDoc.control_type or control_name != requestDoc.control_name:
        control_date = request.POST['control_date']
    if requestDoc.request_number_in_year == None:
        now = datetime.datetime.now()
        year = now.date().year
        items = RequestDocument.objects.filter(Q(year=year))
        requestDoc.year = year
        requestDoc.request_number_in_year = (items.count() + 1)

    requestDoc.submit_date = submit_date
    requestDoc.department = department
    requestDoc.telephone = telephone
    requestDoc.req_new = req_new
    requestDoc.req_cancel = req_cancel
    requestDoc.req_doctype_control = req_doctype_control
    requestDoc.req_doctype_uncontrol = req_doctype_uncontrol
    requestDoc.req_alter = req_alter
    requestDoc.req_other = req_other
    requestDoc.has_attached_doc = attached_doc
    requestDoc.approved_name = approved_name
    requestDoc.response_code = response_code
    # requestDoc.master_list_cancel = master_list_cancel
    # requestDoc.master_list_edit = master_list_edit
    requestDoc.response_other = response_other
    requestDoc.response_name = response_name
    requestDoc.response_date = response_date
    requestDoc.response_original_number = response_original_number
    requestDoc.request_name = request_name
    requestDoc.request_date = request_date
    # requestDoc.control_receive_complete_file = control_receive_complete_file
    # requestDoc.control_keep_original_and_restore_copy = control_keep_original_and_restore_copy
    # requestDoc.control_destroy_copy = control_destroy_copy
    # requestDoc.control_send_copy = control_send_copy
    requestDoc.control_name = control_name
    requestDoc.control_date = control_date
    requestDoc.control_type = control_type
    requestDoc.response_type = response_type
    requestDoc.receive_name = receive_name
    requestDoc.receive_date = receive_date
    requestDoc.approved = approved
    requestDoc.req_type = req_type
    requestDoc.request_position = request_position
    progress = 0
    if control_type != 0:
        progress = 5
    elif receive_name !=  "":
        progress = 4
    elif response_type != 0:
        progress = 3
    elif approved_name != "":
        progress = 2
    else:
        progress = 1
    requestDoc.progress = progress

    requestDoc.save()
    return
