from django.shortcuts import render
from tertulias.models import Tertulia



def home(request):
    tertulias = Tertulia.objects.all()  # Obtener todas las tertulias
    return render(request, 'home.html', {'tertulias': tertulias})



def about(request):
    return render(request, 'about.html')

