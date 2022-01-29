from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from app_accounts.models import AccidentRecords, ECC, Customer, UserMaster

def signout(request):
    logout(request)
    return redirect('/')

def alerts(request):
    if request.user.is_authenticated and request.user.userType == 'ecc':
        eccId = ECC.objects.get(uid=request.user)
        alerts = AccidentRecords.objects.filter(eid=eccId).order_by('-time')
        if not alerts:
            messages.success(request, "No Alerts Yet!") 
        return render(request,"alerts.html",{"alerts":alerts})
    else:
        return render(request,"401.html")

def alertDetails(request):
    if request.user.is_authenticated and request.user.userType == 'ecc':
        accidentId = request.GET.get('id')
        accident = AccidentRecords.objects.filter(rid=accidentId)
        for i in accident:
            customer = Customer.objects.filter(uid=i.cid.uid)
        return render(request,'alert_details.html',{"accident":accident,"customer":customer})
    else:
        return render(request,"401.html")

def myProfile(request):
   if request.user.is_authenticated and request.user.userType == 'ecc':
        eccDetails = ECC.objects.filter(uid=request.user)
        if request.method == "POST":
           contact  = request.POST.get("contact")
           email = request.POST.get("email")
           oldContact  = request.POST.get("old_contact")
           oldEmail = request.POST.get("old_email")
           print(contact, oldContact)
           print(email, oldEmail)
           if contact!= oldContact:
                if email!= oldEmail:
                    try:
                        ecc = ECC.objects.filter(uid=request.user)
                        ecc.update(contact = contact)
                        UserMaster.objects.filter(email= request.user).update(email= email)
                        # Sending Mail
                        subject = "Profile Updated"
                        recipient_list = [request.user, email]
                        email_from = settings.EMAIL_HOST_USER
                        message = f"Dear {ecc[0]}, Your Profile updated Successfully.\nMobile: {contact} \nEmail Address: {email}."
                        send_mail(subject, message, email_from, recipient_list)
                        messages.success(request,"Profile Updated.")
                        logout(request)
                        return redirect('/')
                    except:
                        messages.error(request, 'You can not update your Mail Address, try another Mail Address!')                        
                else:
                        ecc = ECC.objects.filter(uid=request.user)
                        ecc.update(contact = contact)
                        # Sending Mail
                        subject = "Profile Updated"
                        recipient_list = [request.user, email]
                        email_from = settings.EMAIL_HOST_USER
                        message = f"Dear {ecc[0]}, Your Profile updated Successfully.\nMobile: {contact}."
                        send_mail(subject, message, email_from, recipient_list)
                        messages.success(request,"Profile Updated.")
                        redirect('/ECC-Profile/')
           elif email!= oldEmail:
                    try:
                        ecc = ECC.objects.filter(uid=request.user)
                        UserMaster.objects.filter(email= request.user).update(email= email)
                        # Sending Mail
                        subject = "Profile Updated"
                        recipient_list = [request.user, email]
                        email_from = settings.EMAIL_HOST_USER
                        message = f"Dear {ecc[0]}, Your Profile updated Successfully.\nEmail Address: {email}."
                        send_mail(subject, message, email_from, recipient_list)
                        messages.success(request,"Profile Updated.")
                        logout(request)
                        return redirect('/')
                    except:
                        messages.error(request, 'You can not update your Mail Address, try another Mail Address!')                        
           else:
               messages.success(request,"No Changes There!")
   else:
        redirect('/page_notfound401/')

   return render(request,"profile_details.html",{"ecc_details":eccDetails})

def notFound401(request):
    data = {}
    return render(request,"401.html",data)

def notfound404(request, exception):
    return render(request,"404.html",status=400)

def notfound500(request):
    return render(request,"500.html")