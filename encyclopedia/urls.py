from django.urls import path

from . import views

app_name = "tasks"
urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("wiki/<str:id>", views.data, name="data"),
    path('edit/', views.edit, name="edit"),
    path('ran/', views.ran, name="random"),
    path('check/', views.check, name="check")
]
