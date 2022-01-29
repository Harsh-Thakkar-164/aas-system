from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from geopy.geocoders import Nominatim
from webpush import send_user_notification
from .models import Customer, ECC, AccidentRecords, UserMaster,Subscribers
from django.views.decorators.csrf import csrf_exempt


def home(request):
    if request.user.is_anonymous:
        logineduser = None
    else:
        logineduser = request.user.userType

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        if not email:
            submail = request.POST.get("subemail")
            obj = Subscribers(email=submail)
            obj.save()
            messages.success(request,"You are Subscribed to AAS...!")
        else:
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                if user.userType == 'customer':
                    return redirect('/customer/alerts/')
                elif user.userType == 'ecc':
                    return redirect('/ecc/alerts/')
                elif user.userType == 'super':
                    return redirect('/super_admin/alerts/')
            else:
                messages.error(request, "Invalid Credentials!")
    return render(request, "home.html", {"lguser": logineduser})    
def signout(request):
    logout(request)
    return redirect('/')

@csrf_exempt
def notifyAccident(request):
    if request.method == "POST":
        Lat = request.GET.get('lat')
        print(Lat)
        Long  = request.GET.get('long')
        print(Long)
        cid = request.GET.get('cid')
        print(cid)
        User_Loc = (float(Lat),float(Long)) 
        page = None
        users = None
        # Fetching State..
        geolocator = Nominatim(user_agent="Locater")
        location = geolocator.reverse(User_Loc)
        areaname = location.raw['display_name']
        area = location.raw['address']['county']
        state = location.raw['address']['state']
        pincode = None
        print(location)
        try:
            pincode = location.raw['address']['postcode']
        except KeyError:
            area = location.raw['address']['county']

        try:
            city  = location.raw['address']['city']
        except KeyError:
            try:
                city = location.raw['address']['town']
            except KeyError:
                try:
                    city = location.raw['address']['village']
                except KeyError:
                    try:
                        city = location.raw['address']['road']
                    except KeyError:
                        city = None
        customer = Customer.objects.get(cid=cid)
        cname =  Customer.objects.filter(cid=cid).values_list('firstName', 'lastName')
        cfullname = (cname[0][0]).capitalize() + ' ' + (cname[0][1]).capitalize() 

        Ecc = ECC.objects.get(state=state)
        # location = f"https://www.google.com/maps/search/?api=1&query={Lat},{Long}"
        acdata = AccidentRecords(cid=customer,eid=Ecc,latitude=Lat,longitude=Long,city=city,area=area,pincode=pincode)
        acdata.save()

        ecc = UserMaster.objects.get(email=Ecc.uid)
        # admins = UserMaster.objects.filter(email=Ecc.UID)
        eccPayload = {"head": "Accident Alert!", "body": f"{Ecc}, you got an Alert from {area}.", "icon": "D:\\aas-logo.png", "url": "http://127.0.0.1:8000/ECC-Alerts/"}
        send_user_notification(user=ecc, payload=eccPayload, ttl=3000)
        
        customer = UserMaster.objects.get(email=customer.uid)
        customerPayload = {"head": "Accident Alert!", "body": f"{cfullname}, new accident detected from your device at {area}.", "icon": "D:\\aas-logo.png", "url": "http://127.0.0.1:8000/Cust-Alerts/"}
        send_user_notification(user=customer, payload=customerPayload, ttl=3000)

        admins = UserMaster.objects.filter(userType= 'super')
        for a in admins:
            adminPayload = {"head": "Accident Alert!", "body": f"Admin, you got an Alert from {area}.", "icon": "D:\\aas-logo.png", "url": "http://127.0.0.1:8000/Admin-Alerts/"}
            send_user_notification(user=a, payload=adminPayload, ttl=3000)

    return HttpResponse('Accident Request Send.')