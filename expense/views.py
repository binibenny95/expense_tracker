from datetime import date

from bottle import redirect
from django.contrib import messages
from django.db.models import Sum
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from expense.forms import EarningForm, ExpenseForm, PersonForm

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PersonForm, EarningForm, ExpenseForm
from .models import Earning, Expense, Person


def index(request):
    person_form = PersonForm()
    earning_form = EarningForm()
    expense_form = ExpenseForm()

    if request.method == 'POST':
        if 'submit_person_form' in request.POST:
            person_form = PersonForm(request.POST)
            if person_form.is_valid():
                person_form.save()
                messages.success(request, "Person form submitted successfully.")
            else:
                messages.error(request, "There was an error in the Person form.")
        elif 'submit_earning_form' in request.POST:
            earning_form = EarningForm(request.POST)
            if earning_form.is_valid():
                earning_form.save()
                messages.success(request, "Earning form submitted successfully.")
            else:
                messages.error(request, "There was an error in the Earning form.")
        elif 'submit_expense_form' in request.POST:
            expense_form = ExpenseForm(request.POST)
            if expense_form.is_valid():
                expense_form.save()
                messages.success(request, "Expense form submitted successfully.")
            else:
                messages.error(request, "There was an error in the Expense form.")

        return redirect('expense:index')  # Redirect to the same page to avoid resubmission

    context = {
        'person_form': person_form,
        'earning_form': earning_form,
        'expense_form': expense_form,
    }
    return render(request, 'expense/home.html', context)



def fetch_data_overview(request):
    if request.method == "GET" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        persons = list(Person.objects.values('id', 'name'))
        expenses = list(
            Expense.objects.select_related('person').values('id', 'amount', 'person__name', 'category')
        )

        # Fetch earnings with associated person names
        earnings = list(
            Earning.objects.select_related('person').values('id', 'amount', 'person__name')
        )
        print(earnings)
        return JsonResponse({
            'persons': persons,
            'expenses': expenses,
            'earnings': earnings
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def delete_entry(request):
    if request.method == "POST":
        entry_id = request.POST.get('entry_id')
        entry_type = request.POST.get('entry_type')

        if not entry_id or not entry_type:
            return JsonResponse({'success': False, 'error': 'Missing parameters.'})

        try:
            if entry_type == 'person':
                Person.objects.get(id=entry_id).delete()
            elif entry_type == 'earning':
                Earning.objects.get(id=entry_id).delete()
            elif entry_type == 'expense':
                Expense.objects.get(id=entry_id).delete()
            else:
                return JsonResponse({'success': False, 'error': 'Invalid entry type.'})

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

def draw_graph(request):
    current_date = date.today()
    start_date = current_date.replace(day=1)
    expense = Expense.objects.filter(date__range=(start_date, current_date)).values('category').annotate(total=Sum('amount'))
    earning = Earning.objects.filter(date__range=(start_date, current_date)).values('person__name', 'amount').annotate(total=Sum('amount'))
    expense_data = {
        'labels': [e['category'] for e in expense],
        'values': [e['total'] for e in expense]
    }
    earning_data = {
        'labels': [e['person__name'] for e in earning],
        'values': [e['total'] for e in earning]
    }
    print(expense_data)
    # if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    #     # Return JSON data for AJAX requests
    #     return JsonResponse({'expenses': expense_data, 'earnings': earning_data})



