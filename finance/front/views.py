from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404
from accounting.models import Category, Transaction, Bank

# Create your views here.
def index(request):
    return render(request, 'main.html')

#def single_course(request, course_id):
#    course = get_object_or_404(Course, pk=course_id)
#    return render(request, 'single_course.html', {'course': course})

def transactions(request):
    categories = Category.objects.all()
    transactions = Transaction.objects.get_queryset().order_by('date_time')
    banks = Bank.objects.all()
    paginator = Paginator(transactions, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'transactions.html', {"page_obj": page_obj})    

