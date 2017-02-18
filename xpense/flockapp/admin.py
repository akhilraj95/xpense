from django.contrib import admin
from .models import User,Currency,Expense,Track

admin.site.register(User)
admin.site.register(Currency)
admin.site.register(Expense)
admin.site.register(Track)
