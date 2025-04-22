from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm


from .models import Transaction

def logout_view(request):
    logout(request)
    return redirect('accounting:index')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            username = form.cleaned_data.get('username')
            messages.success(request, f'Создан аккаунт {username}!')
            return redirect('accounting:profile')
        else:
            return render(request, 'registration/register.html', {'form': form})
    else:
        form = UserRegisterForm()
        return render(request, 'registration/register.html', {'form': form})

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
        return super().get_queryset().filter(user=self.request.user).order_by("-date_time")

