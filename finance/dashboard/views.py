from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count, Sum, Q
from django.http import JsonResponse
from accounting.models import Transaction
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.cache import cache_page
from django.core.cache import cache

# Константы для кэширования
CACHE_TIMEOUT = 60 * 15  # 15 минут


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@cache_page(CACHE_TIMEOUT)
def transaction_dynamics(request):
    """Динамика транзакций по периодам"""
    period = request.GET.get("period", "week")
    now = timezone.now()

    # Определяем период для выборки
    if period == "week":
        date_from = now - timedelta(days=7)
        group_by = "date"
    elif period == "month":
        date_from = now - timedelta(days=30)
        group_by = "week"
    elif period == "quarter":
        date_from = now - relativedelta(months=3)
        group_by = "month"
    else:  # year
        date_from = now - relativedelta(years=1)
        group_by = "month"

    # Ключ для кэширования
    cache_key = f"transaction_dynamics_{request.user.id}_{period}"
    cached_data = cache.get(cache_key)

    if cached_data:
        return JsonResponse(cached_data, safe=False)

    transactions = (
        Transaction.objects.filter(user=request.user, date_time__gte=date_from)
        .extra(
            select={
                "date": "date(date_time)",
                "week": "EXTRACT(week FROM date_time)",
                "month": "EXTRACT(month FROM date_time)",
            }
        )
        .values(group_by)
        .annotate(count=Count("id"), total_amount=Sum("amount"))
        .order_by(group_by)
    )
    result = list(transactions)
    cache.set(cache_key, result, CACHE_TIMEOUT)
    return JsonResponse(result, safe=False)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@cache_page(CACHE_TIMEOUT)
def transaction_type_stats(request):
    """Статистика по типам транзакций"""
    cache_key = f"transaction_type_stats_{request.user.id}"
    cached_data = cache.get(cache_key)

    if cached_data:
        return JsonResponse(cached_data, safe=False)

    stats = (
        Transaction.objects.filter(user=request.user)
        .values("transaction_type")
        .annotate(count=Count("id"), total_amount=Sum("amount"))
    )

    result = list(stats)
    cache.set(cache_key, result, CACHE_TIMEOUT)
    return JsonResponse(result, safe=False)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@cache_page(CACHE_TIMEOUT)
def income_vs_expense(request):
    """Сравнение доходов и расходов"""
    cache_key = f"income_vs_expense_{request.user.id}"
    cached_data = cache.get(cache_key)

    if cached_data:
        return JsonResponse(cached_data)

    result = Transaction.objects.filter(user=request.user).aggregate(
        total_income=Sum("amount", filter=Q(transaction_type="entry")),
        total_expense=Sum("amount", filter=Q(transaction_type="write-off")),
    )

    cache.set(cache_key, result, CACHE_TIMEOUT)
    return JsonResponse(result)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@cache_page(CACHE_TIMEOUT)
def transaction_status_stats(request):
    """Статистика по статусам транзакций"""
    cache_key = f"transaction_status_stats_{request.user.id}"
    cached_data = cache.get(cache_key)

    if cached_data:
        return JsonResponse(cached_data, safe=False)

    stats = (
        Transaction.objects.filter(user=request.user)
        .values("status")
        .annotate(count=Count("id"))
    )

    result = list(stats)
    cache.set(cache_key, result, CACHE_TIMEOUT)
    return JsonResponse(result, safe=False)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@cache_page(CACHE_TIMEOUT)
def bank_stats(request):
    """Статистика по банкам"""
    cache_key = f"bank_stats_{request.user.id}"
    cached_data = cache.get(cache_key)

    if cached_data:
        return JsonResponse(cached_data)

    sender_stats = (
        Transaction.objects.filter(user=request.user)
        .values("sender_bank__name")
        .annotate(count=Count("id"), total_amount=Sum("amount"))
    )

    receiver_stats = (
        Transaction.objects.filter(user=request.user)
        .values("receiver_bank__name")
        .annotate(count=Count("id"), total_amount=Sum("amount"))
    )

    result = {
        "sender_banks": list(sender_stats),
        "receiver_banks": list(receiver_stats),
    }
    cache.set(cache_key, result, CACHE_TIMEOUT)
    return JsonResponse(result)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@cache_page(CACHE_TIMEOUT)
def category_stats(request):
    """Статистика по категориям"""
    cache_key = f"category_stats_{request.user.id}"
    cached_data = cache.get(cache_key)

    if cached_data:
        return JsonResponse(cached_data, safe=False)

    stats = (
        Transaction.objects.filter(user=request.user)
        .values("category__name", "transaction_type")
        .annotate(count=Count("id"), total_amount=Sum("amount"))
    )

    result = list(stats)
    cache.set(cache_key, result, CACHE_TIMEOUT)
    return JsonResponse(result, safe=False)


def dashboard_view(request):
    """Основное представление дашборда"""
    if not request.user.is_authenticated:
        return render(request, "registration/login.html")

    # Получаем последние 5 транзакций для быстрого просмотра
    recent_transactions = Transaction.objects.filter(user=request.user).select_related(
        "sender_bank", "receiver_bank", "category"
    )[:5]

    # Основные метрики
    total_income = (
        Transaction.objects.filter(
            user=request.user, transaction_type="entry"
        ).aggregate(total=Sum("amount"))["total"]
        or 0
    )

    total_expense = (
        Transaction.objects.filter(
            user=request.user, transaction_type="write-off"
        ).aggregate(total=Sum("amount"))["total"]
        or 0
    )

    context = {
        "recent_transactions": recent_transactions,
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": total_income - abs(total_expense),
        "transaction_count": Transaction.objects.filter(user=request.user).count(),
    }

    return render(request, "dashboard/dashboard.html", context)
