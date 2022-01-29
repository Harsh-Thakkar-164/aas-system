from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="Home_page"),
    path('notify_accident/',views.notifyAccident,name="New_Accident_Request"),
    path('signout/',views.signout,name="Signout"),
]
