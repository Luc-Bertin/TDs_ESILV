from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('houses/<int:house_id>/', views.house_detail, name='detail'),
    path('houses/', views.i_want_a_list, name='list_of_houses'),
    path('predict/', views.predict, name='to_predict')
]
