from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Count, Sum, Q
from django.db.models.functions import TruncWeek, TruncMonth, TruncQuarter, TruncYear
from accounting.models import Transaction, Bank, Category
from io import BytesIO
from reportlab.pdfgen import canvas
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import plotly.graph_objects as go


class ReportView(LoginRequiredMixin, View):
    template_name = 'reports/report.html'
    login_url = '/login/'  # URL для перенаправления неавторизованных пользователей

    def get(self, request):
        # Проверяем, что пользователь аутентифицирован
        if not request.user.is_authenticated:
            return redirect(self.login_url)

        try:
            period = request.GET.get('period', 'week')  # week/month/quarter/year

            # 1. Динамика транзакций
            trunc_func = {
                'week': TruncWeek,
                'month': TruncMonth,
                'quarter': TruncQuarter,
                'year': TruncYear
            }[period]

            transactions_dynamic = (
                Transaction.objects.filter(user_id=request.user.id)  # Используем user_id вместо user
                .annotate(period=trunc_func('date_time'))
                .values('period')
                .annotate(count=Count('id'), total=Sum('amount'))
                .order_by('period')
            )

            # 2. Статистика по типам
            type_stats = (
                Transaction.objects.filter(user_id=request.user.id)
                .values('transaction_type')
                .annotate(count=Count('id'), total=Sum('amount'))
            )

            # 3. Сравнение поступлений/расходов
            income = Transaction.objects.filter(
                user_id=request.user.id, transaction_type='entry'
            ).aggregate(total=Sum('amount'))['total'] or 0
            expense = Transaction.objects.filter(
                user_id=request.user.id, transaction_type='write-off'
            ).aggregate(total=Sum('amount'))['total'] or 0

            # 4. Статусы транзакций
            status_stats = (
                Transaction.objects.filter(user_id=request.user.id)
                .values('status')
                .annotate(count=Count('id'))
            )

            # 5. Банки
            sender_banks = (
                Transaction.objects.filter(user_id=request.user.id)
                .values('sender_bank__name')
                .annotate(count=Count('id'), total=Sum('amount'))
                .order_by('-count')[:5]
            )

            # 6. Категории
            categories = (
                Transaction.objects.filter(user_id=request.user.id)
                .values('category__name', 'transaction_type')
                .annotate(total=Sum('amount'))
            )

            # Генерация графиков Plotly
            # График 1: Динамика транзакций
            if transactions_dynamic:
                periods = [t['period'].strftime('%Y-%m-%d') for t in transactions_dynamic]
                counts = [t['count'] for t in transactions_dynamic]

                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=periods,
                    y=counts,
                    name='Количество транзакций'
                ))
                fig.update_layout(
                    title='Динамика транзакций',
                    xaxis_title='Период',
                    yaxis_title='Количество'
                )
                dynamic_chart = fig.to_html(full_html=False)
            else:
                dynamic_chart = "<div class='alert alert-info'>Нет данных для отображения</div>"

            # График 2: Доходы/расходы
            fig_pie = go.Figure()
            fig_pie.add_trace(go.Pie(
                labels=['Поступления', 'Расходы'],
                values=[income, abs(expense)],
                name='Соотношение'
            ))
            fig_pie.update_layout(title='Соотношение поступлений и расходов')
            income_chart = fig_pie.to_html(full_html=False)

            context = {
                'dynamic_chart': dynamic_chart,
                'income_chart': income_chart,
                'transactions_dynamic': transactions_dynamic,
                'type_stats': type_stats,
                'income': income,
                'expense': expense,
                'status_stats': status_stats,
                'sender_banks': sender_banks,
                'categories': categories,
                'period': period,
            }

            if request.GET.get('export') == 'pdf':
                return self.generate_pdf(context)

            return render(request, self.template_name, context)

        except Exception as e:
            # Логируем ошибку для отладки
            print(f"Error generating report: {str(e)}")
            return render(request, 'reports/error.html', {'error': str(e)})

    def generate_pdf(self, context):
        buffer = BytesIO()
        p = canvas.Canvas(buffer)

        # Заголовок
        p.drawString(100, 800, "Финансовый отчёт")

        # Динамика транзакций
        p.drawString(100, 780, "Динамика транзакций:")
        y = 760
        for item in context['transactions_dynamic']:
            p.drawString(120, y, f"{item['period'].strftime('%Y-%m-%d')}: {item['count']} транзакций")
            y -= 20

        # Поступления/расходы
        p.drawString(100, y - 20, f"Поступления: {context['income']}")
        p.drawString(100, y - 40, f"Расходы: {context['expense']}")

        p.showPage()
        p.save()
        buffer.seek(0)

        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="financial_report.pdf"'
        return response