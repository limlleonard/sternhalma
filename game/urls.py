from django.urls import path, include
from rest_framework import routers # Class viewers
from . import views

router = routers.DefaultRouter()
router.register(r'score', views.ViewsetScore)

urlpatterns = [
    # path("", views.index, name="index"),
    path("return_board/", views.return_board, name="return_board"),
    path("starten/", views.starten, name="starten"),
    # path("find_valid_pos/", views.find_valid_pos, name="find_valid_pos"),
    path("klicken/", views.klicken, name="klicken"),
    # path("reset/", views.reset, name="reset"),
    path("", views.test_react, name="test_react"),

    # path("return_score/", views.return_score, name="return_score"),
    path('api/', include(router.urls)),

    path('api/add_score/', views.ViewsetScore.as_view({'post': 'add_score'})),
]
