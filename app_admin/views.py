from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from app_accounts.models import AccidentRecords, Customer, ECC, UserMaster,Product,PendingOrders

def signout(request):
    logout(request)
    return redirect('/')

def alerts(request):
    if request.user.is_authenticated and request.user.userType == 'super':
        alerts = AccidentRecords.objects.all().order_by('-time')
        if not alerts:
            messages.success(request, "No Alerts Yet!")
    else:
        return render(request,"401.html")
    return render(request,"alerts.html",{"alerts": alerts})

def alertDetails(request):
    if request.user.is_authenticated and request.user.userType == 'super':
        alertId = request.GET.get('id')
        accident = AccidentRecords.objects.filter(rid=alertId)
        if not accident:
            redirect("/super_admin/alerts")
        else:
            for i in accident:
                customer = Customer.objects.filter(uid=i.cid.uid)
                ecc_details = ECC.objects.filter(uid=i.eid.uid)
    else:
         return render(request,"401.html")
    return render(request,'alert_details.html',{"accident":accident, "customer": customer,"ecc":ecc_details})

def eccAlerts(request):
    if request.user.is_authenticated and request.user.userType == 'super':
            eid = request.GET.get("id")
            user = ECC.objects.get(eid = eid)
            alerts = AccidentRecords.objects.filter(eid=user).order_by('-time')
            if not alerts:
                messages.success(request, "No Alerts Yet!") 
    else:
        return render(request,"401.html")
    return render(request,"alerts.html",{"alerts":alerts})

def eccList(request):
    if request.user.is_authenticated and request.user.userType == 'super':
        eccList = ECC.objects.all()
    else:
        return render(request,"401.html")
    return render(request,"profiles.html",{"eccs":eccList})

def eccProfile(request):
    if request.user.is_authenticated and request.user.userType == 'super':
        eccId = request.GET.get("id")
        if request.method == "POST":
            ecc = ECC.objects.get(eid=eccId)
            UserMaster.objects.filter(email=ecc.uid).delete()
            subject = "Profile Deleted"
            recipient_list = [ecc.uid]
            email_from = settings.EMAIL_HOST_USER
            message = f"Dear {ecc.name}, ECC Profile connected with you is removed from Accident ALert Securities."
            send_mail(subject, message, email_from, recipient_list)
            messages.success(request,"ECC Deleted!")     
            return redirect("/super_admin/eccs/")
        else:
            eccDetails = ECC.objects.filter(eid=eccId)
    else:
        return render(request,"401.html")
    return render(request,"profile_details.html",{"ecc_details":eccDetails})

def eccAdd(request):
    if request.user.is_authenticated and request.user.userType == 'super':
            if request.method == "POST":
                name = request.POST.get('ecc_name')
                email = request.POST.get('ecc_email')
                password = request.POST.get('ecc_password')
                contact = request.POST.get('ecc_contact')
                state = request.POST.get('ecc_state')
            try: 
                addUser = UserMaster.objects.create_user(email= email, password= password, userType='ecc')
                addUser.save()
                userId = UserMaster.objects.get(email=email)

                ecc = ECC(name = name ,state =state, contact= contact, uid = userId)
                ecc.save()

                # Sending Mail
                subject = "Profile Registration"
                recipient_list = [email]
                email_from = settings.EMAIL_HOST_USER
                message = f"Dear {name}, New ECC Profile Registered for you in Accident Alert Securities is Successfull.\nYour Credentials are here: \nEmail: {email} \nPassword: {password}"
                send_mail(subject, message, email_from, recipient_list)
                messages.success(request, "ECC Registered.")
                return redirect("/super_admin/eccs/")
            except:
                    messages.error(request, 'Mail Address already exists, try with another Mail Address!')                        
    else:
        return render(request,"401.html")
    return render(request, "profile_details.html")

def customerList(request):
    if request.user.is_authenticated and request.user.userType == 'super':
        customerList = Customer.objects.all()
    else:
        return render(request,"401.html")
    return render(request,"profiles.html",{"customers":customerList})

def customerProfile(request):
    if request.user.is_authenticated and request.user.userType == 'super':
        cid = request.GET.get('id')
        customerDetails = Customer.objects.filter(cid=cid)
        productDetails = Product.objects.get(cid = cid)
    else:
            return render(request,"401.html")
    return render(request,"profile_details.html",{"customer_details":customerDetails, 'product': productDetails})

def customerAlerts(request):
    if request.user.is_authenticated and request.user.userType == 'super':
            cid = request.GET.get("id")
            user = Customer.objects.get(cid = cid)
            alerts = AccidentRecords.objects.filter(cid=user).order_by('-time')
            if not alerts:
                messages.success(request, "No Alerts Yet!") 
    else:
            return render(request,"401.html")
    return render(request,"alerts.html",{"alerts":alerts})

def productList(request):
        if request.user.is_authenticated and request.user.userType == 'super':
            products = Product.objects.all()
            notAllocatedProduct = Product.objects.filter(cid__isnull=True).count()
            print(notAllocatedProduct)
            allocatProduct  = Product.objects.filter(cid__isnull=False).count()
            totalProduct = Product.objects.all().count()
        else:
                return render(request,"401.html")
        return render(request,"profiles.html",{"product":products,"notallocat_product":notAllocatedProduct,"allocate_product":allocatProduct,"total_product":totalProduct})

def productAdd(request):
        if request.user.is_authenticated and request.user.userType == 'super':
            if request.method == "POST":
                enter_products_number = int(request.POST.get('add_product'))
                enter_products_names = []
                try:
                    last_product_number = (Product.objects.order_by("-productTime")[0])
                    last_product_number = int(str(last_product_number)[3:])
                except:
                    last_product_number = 0

                print(last_product_number,enter_products_number)
                for i in range(last_product_number+1, (last_product_number+enter_products_number+1)):
                    enter_products_names.append("DEV" + str(i))
    
                for i in enter_products_names:
                    add_product = Product(modelNumber = i)
                    add_product.save()

                pending_orders_count = PendingOrders.objects.all().count()
                if pending_orders_count:
                    pending_orders_emails = []
                    pending_orders = PendingOrders.objects.values_list("email")
                    for i in pending_orders:
                        pending_orders_emails.append(i[0])

                    print(pending_orders_emails)
                    # Sending Mail
                    subject = "Stock Available"
                    # recipient_list = [email]
                    email_from = settings.EMAIL_HOST_USER
                    message = f"Dear Cusomer, New {enter_products_number} devices added, grab fast from here."
                    send_mail(subject, message, email_from,pending_orders_emails)
                PendingOrders.objects.all().delete()
            messages.success(request,"Product Add Succsess Fullly")
            redirect('/super_admin/products/')
        else:
            return render(request,"401.html")
        return render(request,"profile_details.html")

def productProfile(request):
    if request.user.is_authenticated and request.user.userType == 'super':
        pid = request.GET.get('id')
        data1 = Product.objects.filter(pid=pid).values_list('cid')
        print(data1)
        data = Customer.objects.filter(cid__in = data1)
        product_data = Product.objects.get(cid__in = data)
    else:
        return render(request,"401.html")
    return render(request,"profile_details.html",{"customer_details":data,"product":product_data})

def notFound401(request):
    data = {}
    return render(request,"401.html",data)

def notfound404(request, exception):
    return render(request,"404.html",status=400)

def notfound500(request):
    return render(request,"500.html")