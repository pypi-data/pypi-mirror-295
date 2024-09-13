from django.urls import path
from . import views

urlpatterns = [
    path('logs/', views.userlog_view, name='userlog_view'),
]
