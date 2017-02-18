from django.contrib import admin
from .models import User,Currency,Expense,Track,Chat,Chattrack,ChatExpense,Bills

admin.site.register(User)
admin.site.register(Currency)
admin.site.register(Expense)
admin.site.register(Track)

admin.site.register(Chat)
admin.site.register(Chattrack)
admin.site.register(ChatExpense)
admin.site.register(Bills)
