from django.urls import path
from . import views

urlpatterns = [
      path('alerts/',views.alerts,name="Customer_Alerts_page"),
      path('alert/',views.alertDetails,name="Customer_Alerts_details_page"),
      path('my_profile/',views.myProfile,name="Customer_My_Profile_page"),
      path('ecc/',views.eccProfile,name="Admin_ECC_details_page"),
      path('page_notfound401/',views.notFound401,name = "401 Page Not Found"),
]
