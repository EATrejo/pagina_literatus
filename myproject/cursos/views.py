from django.shortcuts import render
from .models import Curso



# Create your views here.
def cursos_list(request):
    cursos = Curso.objects.all().order_by('id')
    return render(request, 'cursos/cursos_list.html', {'cursos': cursos})


def curso_page(request, slug):
    curso = Curso.objects.get(slug=slug)
    return render(request, 'cursos/curso_page.html', {'curso': curso})

