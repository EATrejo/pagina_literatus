from django.urls import path
from . import views

app_name = 'tertulias'

urlpatterns = [
    path('', views.tertulias_list, name="list"),
    path('<int:slug>/', views.tertulia_page, name="page"),
]