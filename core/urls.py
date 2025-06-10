from django.urls import path

# from library_management.urls import urlpatterns
from . import views
app_name = "core"
urlpatterns = [
    path("borrow/<int:copy_id>/",views.borrow_book_view,name = "borrow_book"),
    path("return/<int:copy_id>/",views.return_book_view,name = "return_book"),
    path("reserve/<int:book_id>/",views.reserve_book_view,name = "reserve_book"),
    path("dashboard/",views.user_dashboard_view,name = "user_dashboard"),
    path("",views.book_list_view,name = "book_list"),
    path("book/<int:book_id>/",views.book_detail_view,name = "book_detail"),
    path('admins/books/',views.admin_book_list, name ='admin_book_list'),
    path('admins/books/add/',views.add_book, name = 'add_book'),
    path('admins/books/<int:book_id>/edit/',views.edit_book,name="edit_book"),
    path('admins/books/<int:book_id>/delete/',views.delete_book,name = 'delete_book'),
    path('admins/books/<int:book_id>/copies',views.book_copies,name = 'book_copies'),
    path('admins/books/<int:book_id>/copies/add/',views.add_book_copy,name = 'add_book_copy'),
    path('admins/books/<int:copy_id>/copies/delete/',views.delete_book_copy,name = "delete_book_copy"),
    path('admins/overdue-report/',views.admin_overdue_report,name = 'admin_overdue_report'),
    path('admins/inventory/',views.inventory_view,name = 'inventory_view'),
]