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
    path("book/<int:book_id/>",views.book_detail_view,name = "book_detail"),
]