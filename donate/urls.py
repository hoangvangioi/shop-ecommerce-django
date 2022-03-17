from django.urls import path
from . import views


urlpatterns = [
	path('', views.DonateListView.as_view(), name="donate"),
]