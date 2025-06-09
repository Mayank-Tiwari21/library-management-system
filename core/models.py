from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from django.conf import settings
from django.utils import timezone
from decimal import Decimal

# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN','Admin'),
        ('MEMBER','Member'),
    )
    role = models.CharField(max_length = 10, choices = ROLE_CHOICES,default='MEMBER')
    phone_number = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex = r'^\d{10}$',message = 'Enter a valid 10 digit phone number')],
        blank = True,
        null = True,
    )
    address = models.CharField(blank=True,null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100,blank = True, null=True)
    language = models.CharField(max_length=50,blank = True,null = True)
    isbn = models.CharField(max_length=13,unique=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default = 1)

    def __str__(self):
        return f"{self.title} by {self.author}"

class BookCopy(models.Model):
    STATUS_CHOICES = [
    ("AVAILABLE","Available"),
    ("BORROWED","Borrowed"),
    ("RESERVED","Reserved"),
    ("LOST","Lost")
    ]
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name="copies")
    copy_number = models.PositiveIntegerField()
    status = models.CharField(max_length = 10,choices=STATUS_CHOICES,default = "AVAILABLE")
    location = models.CharField(max_length=100,blank = True,null= True)

    class Meta:
        unique_together = ("book","copy_number")
    def __str__(self):
        return f"copy{self.copy_number} of {self.book} ({self.status})"

#Borrowing and Reservation Models

#------Borrowed MODEL
class BorrowTransaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE,related_name = "borrow_transactions")
    book_copy = models.ForeignKey(BookCopy,on_delete = models.CASCADE,related_name="borrowed_tranactions")
    borrowed_at = models.DateTimeField(auto_now_add=True,blank = True,null=True)
    due_date = models.DateField()
    returned_at = models.DateTimeField(blank =True,null =True)
    fine_amount = models.DecimalField(max_digits=6,decimal_places=2,default = Decimal('0.00'))

    def __str__(self):
        return f"{self.user.username} borrowed {self.book_copy} on {self.borrowed_at.date()}"
    class Meta:
        ordering = ["-borrowed_at"]

#--------Reservation made MODEL

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE','Active'),
        ('FULFILLED','Fulfilled'),
        ('CANCELLED','Cancelled'),
        ('EXPIRED','Expired')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE,related_name = "reservations")
    book = models.ForeignKey(Book,on_delete =models.CASCADE,related_name = "reservations")
    reserved_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default="ACTIVE")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} reserved {self.book} - {self.status}"

    class Meta:
        unique_together = ['user','book','status']
        ordering = ['-reserved_at']

