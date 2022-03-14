from django.urls import path
from . import views
from .views import *


urlpatterns = [
	path('contact/', views.ContactView.as_view(), name="contact"),
    path('blog/', views.blog, name='blog'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail, name='post_detail'),
    path('tag/<slug:tag_slug>/',views.blog, name='post_tag'),
    # path('search/', views.post_search, name='post_search'),
]