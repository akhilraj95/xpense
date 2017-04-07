from django.contrib import admin

from .models import User,Currency,Chat,Track,Expense,Bill

admin.site.register(User)
admin.site.register(Currency)
admin.site.register(Chat)
admin.site.register(Track)
admin.site.register(Expense)
admin.site.register(Bill)
