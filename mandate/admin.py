from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(PaymentType)
admin.site.register(Category)
admin.site.register(Frequency)
admin.site.register(DebtorBank)
admin.site.register(DebtorAccType)