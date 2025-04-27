from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.views.generic import ListView, TemplateView
from django.shortcuts import render, redirect

from users.forms import CustomUserCreationForm  # Импортируем кастомную форму
from .models import Transaction


def logout_view(request):
    logout(request)
    return redirect("accounting:index")


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматически входим после регистрации
            messages.success(request, "Вы успешно зарегистрировались!")
            return redirect("accounting:profile")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/register.html", {"form": form})


class IndexView(TemplateView):
    template_name = "accounting/index.html"


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounting/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        transactions = Transaction.objects.filter(user=user)
        last_transactions = transactions.order_by("-date_time")[:10]

        total_income = transactions.filter(transaction_type="entry").aggregate(
            total=Sum("amount")
        )["total"] or 0
        total_expenses = transactions.filter(transaction_type="write-off").aggregate(
            total=Sum("amount")
        )["total"] or 0
        balance = total_income - abs(total_expenses)

        context.update({
            "transactions": last_transactions,
            "total_income": round(total_income, 2),
            "total_expenses": round(abs(total_expenses), 2),
            "balance": round(balance, 2),
            "user": user  # Добавляем пользователя в контекст
        })
        return context


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "accounting/transactions.html"
    paginate_by = 10
    context_object_name = "transactions"

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by("-date_time")