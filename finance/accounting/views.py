from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from django.contrib.auth import logout
from django.shortcuts import redirect


from .models import Transaction

def logout_view(request):
    logout(request)
    return redirect('accounting:index')

class IndexView(TemplateView):
    template_name = "accounting/index.html"

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounting/profile.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем текущего пользователя
        user = self.request.user

        # Получаем последние 10 транзакций текущего пользователя, отсортированные по дате
        transactions = Transaction.objects.filter(user=user)
        last_transactions = transactions.order_by('-date_time')[:10]

        # Вычисляем общие доходы и расходы
        total_income = round(sum(t.amount for t in transactions if t.transaction_type == 'entry'), 2)
        total_expenses = round(sum(t.amount for t in transactions if t.transaction_type == 'write-off'), 2)


        # Добавляем данные в контекст      
        context['transactions'] = last_transactions       
        context['total_income'] = total_income
        context['total_expenses'] = total_expenses

        # Возвращаем контекст 
        return context

class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "accounting/transactions.html"
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

