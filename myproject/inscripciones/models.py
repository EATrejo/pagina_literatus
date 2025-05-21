from django.db import models
from users.models import User
from tertulias.models import Tertulia


class TertuliaForm(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True, default=None)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)
    tertulia_name = models.ForeignKey(Tertulia, on_delete=models.CASCADE, default=None)
    tertulia_folio_id =models.IntegerField()



    def __str__(self):
        return self.email
    

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=50)
    tertulia_name = models.ForeignKey(Tertulia, on_delete=models.DO_NOTHING, default=False, null=False)
    tertulia_folio_id =models.IntegerField()


    # Concatenate first name and last name
    @property
    def name(self):
        return f'{self.last_name} {self.first_name}'

    def __str__(self):
        return self.email
