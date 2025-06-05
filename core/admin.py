from django.contrib import admin
from .models import CustomUser, Book,BookCopy, BorrowTransaction,Reservation
from django.contrib.auth.admin import UserAdmin
# Register your models here.
admin.site.register(CustomUser,UserAdmin)
admin.site.register(Book)
admin.site.register(BookCopy)
admin.site.register(Reservation)
admin.site.register(BorrowTransaction)