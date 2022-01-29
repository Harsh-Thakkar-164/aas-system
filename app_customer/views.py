from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from app_accounts.models import AccidentRecords, ECC, Customer, Product, UserMaster

def signout(request):
    logout(request)
    return redirect('/')

def alerts(request):
    if request.user.is_authenticated and request.user.userType == 'customer':
        customerId = Customer.objects.get(uid=request.user)
        alerts = AccidentRecords.objects.filter(cid=customerId).order_by('-time')
        if not alerts:
            messages.success(request, "No Alerts Yet!")
    else:
        return render(request,"401.html") 
    return render(request,"alerts.html",{"alerts":alerts})

def alertDetails(request):
    if request.user.is_authenticated and request.user.userType == 'customer':
        accidenId = request.GET.get('id')
        print(accidenId)
        accident = AccidentRecords.objects.filter(rid=accidenId)
        for i in accident:
            print(i)
            customer = Customer.objects.filter(uid=i.cid.uid)
            ecc_details = ECC.objects.filter(uid=i.eid.uid)
            
        return render(request,'alert_Details.html',{"accident":accident,"customer":customer,"ecc":ecc_details})
    else:
        return render(request,"401.html")   

def myProfile(request):
        if request.user.is_authenticated and request.user.userType == 'customer':
            customerDetails = Customer.objects.filter(uid=request.user)
            # product_data = Product.objects.get(cid__in = customerDetails)
            print(customerDetails)
            if request.method == "POST":
                mobile = request.POST.get('mobile')
                email = request.POST.get('email')
                address = request.POST.get('address')
                city = request.POST.get('city')
                state = request.POST.get('state')
                pincode = request.POST.get('pincode')
                oldMobile = request.POST.get('old_mobile')
                oldEmail = request.POST.get('old_email')
                oldAddress = request.POST.get('old_address')
                oldCity = request.POST.get('old_city')
                oldState = request.POST.get('old_state')
                oldPincode = request.POST.get('old_pincode')
                customer = Customer.objects.filter(uid=request.user)
                updMobile = updAddress = updCity = updState = updPincode = updEmail = ''
                if  mobile!= oldMobile:
                    customer.update(contact =mobile)
                    updMobile = f'\nMobile: {mobile}'
                if  address!= oldAddress:
                    customer.update(address=address)
                    updAddress = f'\nAddress: {address}'
                if  city!= oldCity:
                    customer.update(city=city)
                    updCity = f'\nCity: {city}'
                if  state!= oldState:
                    customer.update(state=state)
                    updState = f'\nState: {state}'
                if  pincode!= oldPincode:
                    customer.update(pincode=pincode)
                    updPincode = f'\nPincode: {pincode}'
                if email!= oldEmail:
                        try:
                            UserMaster.objects.filter(email= request.user).update(email= email)
                            updEmail = f'\nEmail: {email}'
                        except:
                            messages.error(request, 'You can not update your Mail Address, try another Mail Address!')   
                updProfile = updMobile + updEmail + updAddress + updCity + updState + updPincode
                if updProfile:
                    print(updProfile)
                    print(customer)
                    # Sending Mail
                    subject = "Profile Updated"
                    if email!=oldEmail:
                        recipient_list = [request.user]
                    else:
                        recipient_list = [request.user, email]
                    email_from = settings.EMAIL_HOST_USER
                    message = f"Dear {customer[0]}, Your Profile updated Successfully.{updProfile}."
                    send_mail(subject, message, email_from, recipient_list)
                    messages.success(request,"Profile Updated.")
                    if email!=oldEmail:
                        logout(request)
                        return redirect('/')
                    else:
                        redirect('/Cust-Profile/')
                else:
                    messages.success(request,"No Changes there!")
        else:
            return render(request,"401.html")
        return render(request,"profile_details.html",{"customer_details":customerDetails})

def notFound401(request):
    data = {}
    return render(request,"401.html",data)

def notfound404(request, exception):
    return render(request,"404.html",status=400)

def eccProfile(request):
    if request.user.is_authenticated and request.user.userType == 'customer':
        eccId = request.GET.get("id")
        eccDetails = ECC.objects.filter(eid=eccId)
    else:
        return render(request,"401.html")
    return render(request,"profile_details.html",{"ecc_details":eccDetails})

def notfound500(request):
    return render(request,"500.html")