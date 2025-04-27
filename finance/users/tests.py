from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.forms import UserRegisterForm
from users.models import User

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            inn='1234567890'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.inn, '1234567890')
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertFalse(self.user.is_superuser)
        self.assertTrue(self.user.is_active)

    def test_user_str_representation(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_user_inn_uniqueness(self):
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='testuser2',
                email='test2@example.com',
                password='testpass123',
                inn='1234567890'  # Дубликат ИНН
            )

class UserRegisterFormTest(TestCase):
    def test_valid_registration_form(self):
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'inn': '0987654321',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_inn_length(self):
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'inn': '12345',  # Слишком короткий ИНН
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('inn', form.errors)

    def test_non_numeric_inn(self):
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'inn': 'abcdefghij',  # Нечисловой ИНН
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('inn', form.errors)

    def test_password_mismatch(self):
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'inn': '1234567890',
            'password1': 'complexpassword123',
            'password2': 'differentpassword'
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

class UserViewsTest(TestCase):
    def test_registration_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertContains(response, 'Регистрация')

    def test_successful_registration(self):
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'inn': '0987654321',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        }
        response = self.client.post(reverse('register'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Редирект после успешной регистрации
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_failed_registration(self):
        form_data = {
            'username': 'newuser',
            'email': 'invalid-email',  # Невалидный email
            'inn': '12345',  # Невалидный ИНН
            'password1': 'complexpassword123',
            'password2': 'differentpassword'  # Пароли не совпадают
        }
        response = self.client.post(reverse('register'), data=form_data)
        self.assertEqual(response.status_code, 200)  # Остается на странице
        self.assertFalse(User.objects.filter(username='newuser').exists())
        self.assertContains(response, 'Введите корректный адрес электронной почты')
        self.assertContains(response, 'ИНН должен содержать 10 или 12 цифр')
        self.assertContains(response, 'Пароли не совпадают')

    def test_login_view(self):
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            inn='1234567890'
        )
        response = self.client.post(
            reverse('login'),
            {'username': 'testuser', 'password': 'testpass123'}
        )
        self.assertEqual(response.status_code, 302)  # Редирект после успешного входа

class UserAdminTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            inn='9876543210'
        )
        self.client.force_login(self.admin)

    def test_user_list_in_admin(self):
        User.objects.create_user(
            username='regularuser',
            email='regular@example.com',
            password='regularpass123',
            inn='1234567890'
        )
        response = self.client.get('/admin/users/user/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'admin')
        self.assertContains(response, 'regularuser')
        self.assertContains(response, 'ИНН')  # Проверяем, что поле ИНН отображается

    def test_user_creation_in_admin(self):
        response = self.client.post(
            '/admin/users/user/add/',
            {
                'username': 'newadmin',
                'email': 'newadmin@example.com',
                'inn': '1122334455',
                'password1': 'newadminpass123',
                'password2': 'newadminpass123',
                'is_superuser': 'on'
            }
        )
        self.assertEqual(response.status_code, 302)  # Редирект после успешного создания
        self.assertTrue(User.objects.filter(username='newadmin').exists())
        self.assertEqual(User.objects.get(username='newadmin').inn, '1122334455')