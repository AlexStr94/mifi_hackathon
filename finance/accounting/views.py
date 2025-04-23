from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView

from .models import Transaction


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "transactions.html"
    paginate_by = 25
    login_url = '/accounts/login/'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
