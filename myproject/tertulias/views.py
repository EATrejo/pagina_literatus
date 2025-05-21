from django.shortcuts import get_object_or_404, render, redirect
from .models import Tertulia
from django.http import HttpResponse



def tertulias_list(request):
    
    tertulias = Tertulia.objects.all().order_by('id')



    context = {
        'tertulias': tertulias,
}
    return render(request, 'tertulias/tertulias_list_copia.html', context)


def tertulia_page(request, slug):
    tertulia = get_object_or_404(Tertulia, slug=slug)
    return render(request, 'tertulias/tertulia_page.html', {'tertulia': tertulia})






