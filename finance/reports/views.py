from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from django.views.generic import TemplateView
from xhtml2pdf import pisa

from accounting.models import Transaction


class ReportView(LoginRequiredMixin, TemplateView):
    template_name = "report.html"


class PdfView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        template_path = 'transactions-export.html'
        transactions = Transaction.objects.all()
        context = {'transactions': transactions}
        template = get_template(template_path)
        html = template.render(context)

        pisa_status = pisa.pisaDocument(html, dest=None)

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')

        return HttpResponse(
            content=pisa_status.dest.getvalue(),
            headers={
                "Content-Type": "application/pdf",
                "Content-Disposition": 'attachment; filename="report.pdf"',
            }
        )
