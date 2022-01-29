from django.urls import path
from . import views

urlpatterns = [
      path('alerts/',views.alerts,name="Admin_Alerts_page"),
      path('alert/',views.alertDetails,name="Admin_Alerts_details_page"),
      path('eccs/',views.eccList,name="Admin_ECC_list_page"),
      path('ecc/',views.eccProfile,name="Admin_ECC_details_page"),
      path('add_ecc/',views.eccAdd,name="Admin_Add_ECC_page"),
      path('ecc_alerts/',views.eccAlerts,name="Admin_ECC_Alerts_page"),
      
      path('customers/',views.customerList,name="Admin_Customer_list_page"),
      path('customer/',views.customerProfile,name="Admin_Customer_details_page"),
      path('customer_alerts/',views.customerAlerts,name="Admin_Customer_Alerts_page"),

      path('products/',views.productList,name ="Admin_Product_List_page"),
      path('product/',views.productProfile,name ="Admin_Product_Profile"),
      path('add_product/',views.productAdd,name="Admin_Add_Product_Page"),
      path('page_notfound401/',views.notFound401,name = "401 Page Not Found"),

]
