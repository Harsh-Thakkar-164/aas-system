from contextlib import redirect_stderr
from itertools import product
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib.auth import logout
from datetime import datetime

from app_accounts.models import Product, UserMaster, Customer, PendingOrders

def products(request):
        availableProducts = Product.objects.filter(cid=None).count()
        if availableProducts:
            if availableProducts <=5:
                buttonText = "Grab Now"
                screenText = "Few Products Left"
            else:
                buttonText = 'Buy Now'
                screenText = " "
        
        else:
            buttonText = "Pre-Order"
            screenText = "Sold Out"
        return render(request, "home.html",{"buttontext":buttonText,"screentext":screenText})

def registrationPhase1(request):
        if request.method =="POST":
            email = request.POST.get('emailPassed').lower()
            vehicleNumber = request.POST.get('vahicalNPassed').upper()
            vehicleModel = request.POST.get('vahicalMPassed').capitalize()
            
            if Customer.objects.filter(vehicleNumber = vehicleNumber).exists():
                    messages.error(request,"Vahical Number Exist")
            elif UserMaster.objects.filter(email = email).exists():
                 messages.error(request,"Email Already Exist")
            else:
                productName = Product.objects.filter(cid__isnull=True)[0]
                if productName:
                    uid = UserMaster(email= email, userType="customer", password="AAS.*@@@T@E@S*T*.")
                    uid.save()
                    cid = Customer(vehicleModel= vehicleModel, vehicleNumber= vehicleNumber, uid= uid)
                    cid.save()
                    Product.objects.filter(modelNumber=productName).update(cid=cid)
                    uid = int(UserMaster.objects.filter(email=email).values_list('uid')[0][0])
                    
                    return redirect(f'/products/registration_phase2/?id={uid}')
                else:
                    messages.error(request, 'Insufficient Product')
        return render(request,"home.html")

def registrationPhase2(request):
    uid = request.GET.get('id')
    print(uid)
    if uid:
        if request.method == "POST":
            fname = request.POST.get('fname').capitalize()
            lname = request.POST.get('lname').capitalize()
                
            print(fname, uid)
            if fname and uid:
                    mo = request.POST.get('mob')
                    birthdate = request.POST.get('birthdate')
                    gender = request.POST.get('gender').capitalize()
                    blood = request.POST.get('BG').capitalize()
                    add = request.POST.get('add').capitalize()
                    zcode = request.POST.get('zip')
                    state = request.POST.get('state').capitalize()
                    city = request.POST.get('city').capitalize() 

                    cid = Customer.objects.get(uid=uid)

                    customer = Customer.objects.filter(uid=uid)
                    customer.update(firstName=fname, lastName=lname, contact=mo, birthDate=birthdate, gender=gender, bloodGroup=blood, address=add, city=city, state=state, pincode= zcode)

                    ProductName = Product.objects.filter(cid=cid).values_list('modelNumber')[0][0]
                    email = UserMaster.objects.filter(uid=uid).values_list('email')[0][0]
                    print(email)
                    # Sending Mail
                    subject = "Device Purchase"
                    recipient_list = [email]
                    email_from = settings.EMAIL_HOST_USER
                    customer = fname
                    message = f"Dear {customer}, Your Order For AAS Device Has been Placed with corresponding Email: {email} Thank You.\nPlease Conform Your Product and active your profile using your Product Code: {ProductName}  on following site: http://127.0.0.1:8000/products/confirm_product/ .\nNote: You can not Login in the system until your product confirmation."
                    send_mail(subject, message, email_from, recipient_list)
                    messages.success(request, "Device Allocated Successfully! It will be on your door soon.")
                    return redirect('/products/')
        return render(request, "home.html")
    else:
        return redirect('/products/registration_phase1/')

def preOrder(request):
    if request.method == "POST":
        fname = request.POST.get('fname').capitalize()
        lname = request.POST.get('lname').capitalize()
        email = request.POST.get('email').lower()
        
        pending_order=PendingOrders(firstName=fname,lastName=lname,email=email)
        pending_order.save()
            # # Sending Mail
        subject = "Pre Order Booked"
        recipient_list = [email]
        email_from = settings.EMAIL_HOST_USER
        customer = fname+' '+ lname
        message = f"Dear {customer}, Your Pre-Order Product Request has been added successfully. \nWe will contact you whenever products are available."
        send_mail(subject, message, email_from, recipient_list)
        messages.success(request,"Your Pre-Order added SuccessFully")
        redirect('/products/')
    return render(request, "home.html")

def confirmProduct(request):
    if request.method == "POST":
        email = request.POST.get('email').lower()
        confirmDevice = request.POST.get('deviceId').upper()
        newPassword = request.POST.get('password')
        user = UserMaster.objects.get(email=email)
        if not user:
            messages.error(request,"No Such Registerd Device!")
        else:
            device = Product.objects.filter(modelNumber= confirmDevice, allocationTime=None)
            print(confirmDevice)
            if device:
                device.update(allocationTime=datetime.now())
                user.set_password(newPassword)
                user.save()
                messages.success(request,"AAS Device connected with you now!")
                # Sending Mail
                subject = "AAS Device Confirmation"
                recipient_list = [email]
                email_from = settings.EMAIL_HOST_USER
                message = f"Dear User, Your AAS Device is fully conncted.\nNow you can login in your account.\nYour Account Credentils are:- \nEmail: {email} \nPassword: {newPassword}"
                send_mail(subject, message, email_from, recipient_list)
                logout(request)
                return redirect('/')
            else:
                messages.error(request, "AAS Device Already Connedted.")                
    return render(request, "home.html")
