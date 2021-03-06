from django.conf.urls import url
from django.urls import path
from lists.views import views
# from lists.views.views import ShowListView
from lists.views.views import ShowDetailView

urlpatterns = [
    url(r'^new$', views.new_list, name='new_list'),
    path('<int:pk>/new_item', views.create_item, name='create_item'),
    path('<int:pk>/', ShowDetailView.as_view(), name='list_detail'),
]