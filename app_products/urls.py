from django.urls import path
from . import views

urlpatterns = [
    path('',views.products,name="Products_page"),
    path('confirm_product/',views.confirmProduct,name="Product_Confirmation_page"),
    path('registration_phase1/',views.registrationPhase1,name="Product_registration_Phase1"),
    path('registration_phase2/',views.registrationPhase2,name="Product_registration_Phase2"),
    path('pre_order/',views.preOrder,name="Pending_Product_Details"),
]
