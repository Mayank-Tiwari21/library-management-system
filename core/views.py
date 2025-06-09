from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import BookCopy ,Book, Reservation, BorrowTransaction
from .services import borrow_book, return_book
from  django.utils import timezone
from django.db.models import Q
# Create your views here.

@login_required
def borrow_book_view(request, copy_id):
    book_copy = get_object_or_404(BookCopy,id = copy_id)
    try:
        borrow_book(request.user,book_copy)
        messages.success(request,f"You have successfully borrowed {book_copy.book.title}")
    except Exception as e:
        messages.error(request,f"Borrow failed:{str(e)}")
    return redirect("core:book_detail",book_id=book_copy.book.id)


@login_required
def return_book_view(request,copy_id):
    book_copy = get_object_or_404(BookCopy,id = copy_id)
    try:
        return_book(book_copy)
        messages.success(request,f"Successfully returned {book_copy.book.title}")
    except Exception as e:
        messages.error(request,f"Return failed:{str(e)}")
    return redirect("core:book_detail",book_id = book_copy.book.id)

@login_required
def reserve_book_view(request, book_id):
    book = get_object_or_404(Book,id=book_id )

    #check for existing active reservation
    existing = Reservation.objects.get(user = request.user, book = book , status = 'ACTIVE').exists()
    if existing:
        messages.warning(request,"You already have an active reservation for this book.")
        return redirect("core:book_detail",book_id = book_id)

    #check if any available copies exist
    if book.available_copies> 0:
        messages.info(request, "Book is currently available. You can borrow it instead of reserving.")
        return redirect("core:book_detail", book_id = book_id)
    # create reservation
    Reservation.objects.create(
        user = request.user,
        book = book
    )
    messages.success(request,"Reservation placed successfully")
    return redirect("core:book_detail",book_id = book_id)
@login_required
def user_dashboard_view(request):
    #current active borrowings
    active_borrows  = BorrowTransaction.objects.filter(
        user = request.user,
        returned_at__isnull = True
    ).select_related("book_copy__book")

    #current active and fulfulled reservations
    reservations = Reservation.objects.filter(
        user = request.user
    ).select_related("book")
    today = timezone.now().date()
    for txn in active_borrows:
        txn.is_overdue = txn.due_date and txn.due_date< timezone.now().date()
        txn.has_fine = txn.fine_amount and txn.fine_amount > 0
    context = {
        'active_borrows':active_borrows,
        'reservations':reservations,
        'today':today
    }

    return render(request,'core/user_dashboard.html',context)

def book_list_view(request):
    query = request.GET.get('q','')
    books = Book.objects.all()

    if query:
        books = books.filter(
            Q(title__icontains =query) |
            Q(author__icontains = query)|
            Q(category__icontains = query)
        )
    context = {
        'books':books,
        'query':query,
    }
    return render(request,"core/book_list.html",context)

def book_detail_view (request,book_id):
    book = get_object_or_404(Book,id = book_id)
    copies = book.copies.all()

    available_copies = copies.filter(status = "AVAILABLE").count()
    total_copies = copies.count()

    context = {
        'book':book,
        'copies':copies,
        'available_copies':available_copies,
        "total_copies":total_copies
    }
    return render(request,"core/book_detail.html",context)

# For the admin panel admin views

def is_admin(user):
    return user.is_authenticated and user.role == 'ADMIN'


@user_passes_test(is_admin)
def admin_book_list(request):
    books = Book.objects.all().prefetch_related('copies')
    return render(request, 'core/admin/book_list.html', {'books': books})
