from django.urls import path
from . import views



app_name = 'inscripciones'

urlpatterns = [
    path('inscripcion_tertulia', views.inscripcion_tertulia, name="inscripcion_tertulia"),

    path('activate/<uidb64>/<token>/', views.activate, name="activate"),

    path('welcome_tertulia_page/', views.welcome_tertulia_page, name='welcome_tertulia_page'),

    path('no_hay_lugares/', views.no_hay_lugares, name='no_hay_lugares'),
    



]