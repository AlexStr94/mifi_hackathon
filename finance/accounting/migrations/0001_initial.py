# Generated by Django 5.2 on 2025-04-16 19:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Наименования банка')),
                ('inn', models.CharField(max_length=10, unique=True, verbose_name='ИНН')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Название категории.')),
                ('description', models.CharField(max_length=256, verbose_name='Описание категории.')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания категории.')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата и время последнего обновления категории.')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_person', models.CharField(choices=[('company', 'Юридическое лицо'), ('person', 'Физическое лицо')], max_length=10, verbose_name='Тип лица')),
                ('date_time', models.DateTimeField(verbose_name='Дата и время операции.')),
                ('transaction_type', models.CharField(choices=[('entry', 'Поступление'), ('write-off', 'Списание')], max_length=10, verbose_name='Тип транзакции')),
                ('comment', models.CharField(max_length=500, verbose_name='Комментарий к операции.')),
                ('amount', models.DecimalField(decimal_places=5, max_digits=20, verbose_name='Сумма транзакции.')),
                ('status', models.CharField(choices=[('new', 'Новая'), ('confirmed', 'Подтвержденная'), ('in_process', 'В обработке'), ('canceled', 'Отменена'), ('completed', 'Платеж выполнен'), ('deleted', 'Платеж удален'), ('refund', 'Возврат')], max_length=10, verbose_name='Статус операции')),
                ('receiver_phone', models.CharField(max_length=18, verbose_name='Телефон получателя')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to='accounting.category')),
                ('receiver_bank', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='received_transactions', to='accounting.bank')),
                ('sender_bank', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sent_transactions', to='accounting.bank')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL, verbose_name='Идентификатор пользователя, который создал транзакцию.')),
            ],
        ),
    ]
