from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django_select2.forms import Select2Widget

from expense.models import Earning, Expense, Person


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper(self)
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit', 'Submit'))

class ExpenseForm(forms.ModelForm):

    CATEGORIES = [
        ('food', 'Food'),
        ('transport', 'Transport'),
        ('children', 'Children'),
        ('housing', 'Housing'),
        ('health', 'Health'),
    ]
    category = forms.ChoiceField(choices=CATEGORIES, label="Category")
    class Meta:
        model = Expense
        fields = '__all__'

        widgets = {
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),

        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper(self)
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit', 'Submit'))

class EarningForm(forms.ModelForm):
    class Meta:
        model = Earning
        fields = '__all__'
        widgets = {
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper(self)
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit', 'Submit'))

