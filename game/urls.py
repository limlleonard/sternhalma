from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("return_board/", views.return_board, name="return_board"),
    path("return_pieces/", views.return_pieces, name="return_pieces"),
    # path("find_valid_pos/", views.find_valid_pos, name="find_valid_pos"),
    path("klicken/", views.klicken, name="klicken"),
    path("reset/", views.reset, name="reset"),
    path("test_react/", views.test_react, name="test_react"),
]
