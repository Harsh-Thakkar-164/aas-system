from django.shortcuts import render

#Error Pages

def notfound404(request, exception):
    return render(request,"404.html",status=400)

def notfound500(request):
    return render(request,"500.html",status=500)