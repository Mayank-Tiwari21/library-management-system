from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from .models import BorrowTransaction, Reservation,BookCopy
from django.core.mail import send_mail

#setting global variables
BORROW_LIMIT = 3
BORROW_DURATION_DAYS =14
FINE_PER_DAY = Decimal('5.00')
EMAIL_BACKEND = "django.core.mail.console.Email.Backend"
DEFAULT_FROM_EMAIL = 'library@example.com'


def borrow_book(user, book_copy):
    if book_copy.status != "AVAILABLE":
        raise Exception("Book copy is not available")
    active_borrows = BorrowTransaction.objects.filter(user = user, returned_at__isnull = True).count()
    if active_borrows >= BORROW_LIMIT:
        raise Exception("Borrowing Limit exceeded")
    overdue_books = BorrowTransaction(user = user, due_date__lt = timezone.now().date(),returned_at_isNull= True)
    if overdue_books.exists():
        raise Exception("You have overdue books. Return them before borrowing")
    # updating teh book_copy status
    book_copy.status = "BORROWED"
    book_copy.save()

    #updating the book available_copies
    book_copy.book.available_copies -=1
    book_copy.book.save()

    #setting the due date
    due_date = timezone.now().date() + timedelta(days = BORROW_DURATION_DAYS)

    BorrowTransaction(
        user = user,
        book_copy = book_copy,
        due_date = due_date
    )

def return_book(book_copy):
    try:
        transaction = BorrowTransaction.objects.get(book_copy = book_copy,returned_at__isnull = True )
    except BorrowTransaction.DoesNotExist:
        raise Exception("This book copy is not currently borrowed.")

    #updating the return date of the borrowed book
    transaction.returned_at = timezone.now()

    #fine calculation
    today = timezone.now().date()
    if today > transaction.due.date:
        overdue_days = (today- transaction.due_date).days
        transaction.fine_amount = overdue_days*FINE_PER_DAY

    transaction.save()

    #update the available copies
    book_copy.book.available_copies +=1
    book_copy.book.save()

    #fullfilll earliest active reservation (if any)
    reservation = Reservation(book = book_copy.book, status = "ACTIVE").order_by("reserved_at").first()
    if reservation:
        try:
            borrow_book(reservation.user,book_copy)
            reservation.status = "FULFILLED"
            reservation.save()
            #send success notifiacation
            transaction = BorrowTransaction.objects.get(
                user = reservation.user,
                book_copy = book_copy,
                returned_at__isnull = True
            )
            send_mail(
                subject = "Your Book reservation is Fulfilled",
                message = f"""Dear {reservation.user.username},


Good News! Your reserved book '{book_copy.book.title}' is now available and has been issued to you.\n
PLease return the book before the due date {transaction.due_date}.

Thank You,
Library Team
""",
                from_email='library@example.com',
                recipient_list= [reservation.user.email],
                fail_silently=True
            )
        except Exception as e:
            #send the failure notification
            send_mail(
                subject = "Issue with your Book reservation.",
                message= f"""Dear {reservation.user.username},


We tried to issue your reserved book {book_copy.book.title} but could not complete the process.
Reason :{str(e)}.
Please check your account and resolve any outstanding issues.

Thank you,
Library Team.""",
                from_email='library@example.com',
                recipient_list=[reservation.user.email],
                fail_silently=True
            )
            print(f"Could not fulfill reservation for user {reservation.user.username}:{e}")
