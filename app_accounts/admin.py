from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import ECC, AccidentRecords, Admin, Customer, PendingOrders, Product, UserMaster


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = UserMaster
    list_display = ('email', 'is_staff', 'is_active','userType')
    list_filter = ('email', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password','userType')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active','userType')}
        ),
        
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(UserMaster,CustomUserAdmin)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Admin)
admin.site.register(ECC)
admin.site.register(AccidentRecords)
admin.site.register(PendingOrders)
