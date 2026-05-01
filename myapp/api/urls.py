from . views import *
from django.urls import path

urlpatterns = [
    path('limited/', limited_view),
    path('send/email/', SendMail.as_view() ),
]