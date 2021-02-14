from django.conf.urls import url
from django.urls import path
from lists.views import views
from lists.views.views import ShowListView


urlpatterns = [
    url(r'^new$', views.new_list, name='new_list'),
    path('<int:pk>/', ShowListView.as_view(), name='view_list'),
]