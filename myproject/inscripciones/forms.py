from django import forms
from .models import Student


class TertuliaRegistro(forms.ModelForm):
    class Meta:
        model = Student
        fields = [ 'last_name','first_name', 'email', 'phone_number', 'tertulia_name', 'tertulia_folio_id']
