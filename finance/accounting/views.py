from django.contrib import messages
from django.contrib.auth import logout, login
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.views.generic import View, TemplateView
from django.shortcuts import render, redirect
from api.v1.accounting.filters import TransactionFilterSet
from api.v1.accounting.serializers import CreateTransactionSerializer, UpdateTransactionSerializer

from users.forms import CustomUserCreationForm  # Импортируем кастомную форму
from .models import Bank, Category, Transaction


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
        balance = total_income - total_expenses

        context.update({
            "transactions": last_transactions,
            "total_income": round(total_income, 2),
            "total_expenses": round(abs(total_expenses), 2),
            "balance": round(balance, 2),
            "user": user  # Добавляем пользователя в контекст
        })

        return context


class TransactionListView(LoginRequiredMixin, FilterView):
    model = Transaction
    filterset_class = TransactionFilterSet
    context_object_name = 'transactions'
    template_name = "accounting/transactions.html"
    paginate_by = 10
    context_object_name = "transactions"

    def get_queryset(self):
        return (
            super().get_queryset().filter(user=self.request.user).order_by("-date_time")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statuses"] = Transaction.TRANSACTION_STATUSES
        context["banks"] = Bank.objects.all()
        context["categories"] = Category.objects.all()
        context["types"] = Transaction.TRANSACTION_TYPES
        return context


class TransactionCreateView(View):
    def post(self, request, *args, **kwargs):
        data = {key: value[0] for key, value in request.POST.lists()}
        serializer = CreateTransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            messages.success(request, "Транзакция добавлена.")
        else:
            messages.error(request, "Ошибка добавления транзакции.")
        return redirect("accounting:transactions")


class TransactionUpdateView(View):
    def post(self, request, id: int, *args, **kwargs):
        transaction = Transaction.objects.get(id=id)
        data = {key: value[0] for key, value in request.POST.lists()}
        serializer = UpdateTransactionSerializer(transaction, data=data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "Транзакция обновлена.")
        else:
            messages.error(request, "Ошибка обновления транзакции.")
        return redirect("accounting:transactions")


class TransactionDeleteView(View):
    def post(self, request, id: int, *args, **kwargs):
        if request.POST.get('_method') == 'DELETE':
            Transaction.objects.get(id=id).delete()
            messages.success(request, "Транзакция удалена")
            return redirect("accounting:transactions")
        return redirect("accounting:transactions")
