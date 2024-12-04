from django.db import models


# Create your models here.
class Person(models.Model):
    name = models.CharField(verbose_name='Name', max_length=50)

    def __str__(self):
        return self.name


class Earning(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='Amount', default=0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.amount)


class Expense(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='Amount', default=0)
    date = models.DateField(auto_now_add=True)
    category = models.CharField(verbose_name='Category', max_length=50)

    def __str__(self):
        return str(self.amount)
