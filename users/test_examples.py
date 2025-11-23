"""
Приклади використання тестів SpeakMate

Цей файл містить приклади того, як писати та розширювати тести
для проекту SpeakMate.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import Language, Goal, Interest, UserLanguage

User = get_user_model()


# ============================================================================
# ПРИКЛАД 1: Простий тест моделі
# ============================================================================

class ExampleSimpleModelTest(TestCase):
    """Приклад простого тесту моделі"""
    
    def test_create_language(self):
        """Тест створення мови"""
        # Створюємо об'єкт
        language = Language.objects.create(code='en', name='English')
        
        # Перевіряємо що об'єкт створено правильно
        self.assertEqual(language.code, 'en')
        self.assertEqual(language.name, 'English')
        self.assertEqual(str(language), 'English')


# ============================================================================
# ПРИКЛАД 2: Тест з setUp методом
# ============================================================================

class ExampleTestWithSetup(TestCase):
    """Приклад тесту з методом setUp для підготовки даних"""
    
    def setUp(self):
        """Цей метод виконується перед КОЖНИМ тестом"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.language = Language.objects.create(code='en', name='English')
    
    def test_user_exists(self):
        """Тест що користувач створено в setUp"""
        self.assertIsNotNone(self.user)
        self.assertEqual(self.user.username, 'testuser')
    
    def test_language_exists(self):
        """Тест що мова створена в setUp"""
        self.assertIsNotNone(self.language)
        self.assertEqual(self.language.code, 'en')


# ============================================================================
# ПРИКЛАД 3: Тест форми
# ============================================================================

class ExampleFormTest(TestCase):
    """Приклад тестування форм"""
    
    def setUp(self):
        self.language = Language.objects.create(code='en', name='English')
    
    def test_valid_form(self):
        """Тест валідної форми"""
        from users.forms import UserLanguageForm
        
        form_data = {
            'language': self.language.id,
            'proficiency': 'B1',
        }
        form = UserLanguageForm(data=form_data)
        
        # Перевіряємо що форма валідна
        self.assertTrue(form.is_valid())
    
    def test_invalid_form(self):
        """Тест невалідної форми"""
        from users.forms import UserLanguageForm
        
        form_data = {
            'language': '',  # Порожнє поле
            'proficiency': '',
        }
        form = UserLanguageForm(data=form_data)
        
        # Перевіряємо що форма невалідна
        self.assertFalse(form.is_valid())
        
        # Перевіряємо що є помилки для конкретних полів
        self.assertIn('language', form.errors)
        self.assertIn('proficiency', form.errors)


# ============================================================================
# ПРИКЛАД 4: Тест view з авторизацією
# ============================================================================

class ExampleViewTest(TestCase):
    """Приклад тестування views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile_url = reverse('profile')
    
    def test_view_requires_login(self):
        """Тест що view вимагає авторизації"""
        response = self.client.get(self.profile_url)
        
        # Перевіряємо редірект на сторінку логіну
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
    
    def test_view_authenticated(self):
        """Тест view для авторизованого користувача"""
        # Логінимось
        self.client.login(username='testuser', password='testpass123')
        
        # Робимо запит
        response = self.client.get(self.profile_url)
        
        # Перевіряємо успішний статус
        self.assertEqual(response.status_code, 200)
        
        # Перевіряємо що використовується правильний шаблон
        self.assertTemplateUsed(response, 'users/profile.html')
        
        # Перевіряємо контекст
        self.assertEqual(response.context['user'], self.user)


# ============================================================================
# ПРИКЛАД 5: Тест POST запиту
# ============================================================================

class ExamplePostRequestTest(TestCase):
    """Приклад тестування POST запитів"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.language = Language.objects.create(code='en', name='English')
        self.client.login(username='testuser', password='testpass123')
    
    def test_post_valid_data(self):
        """Тест POST запиту з валідними даними"""
        url = reverse('add_language')
        form_data = {
            'language': self.language.id,
            'proficiency': 'B1',
        }
        
        # Відправляємо POST запит
        response = self.client.post(url, data=form_data)
        
        # Перевіряємо редірект після успішного збереження
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))
        
        # Перевіряємо що дані збережено в базі
        user_language = UserLanguage.objects.filter(
            user=self.user,
            language=self.language
        ).first()
        self.assertIsNotNone(user_language)
        self.assertEqual(user_language.proficiency, 'B1')


# ============================================================================
# ПРИКЛАД 6: Тест з перевіркою винятків
# ============================================================================

class ExampleExceptionTest(TestCase):
    """Приклад тестування винятків"""
    
    def test_unique_constraint(self):
        """Тест що унікальне обмеження працює"""
        # Створюємо першу мову
        Language.objects.create(code='en', name='English')
        
        # Спроба створити мову з таким же кодом повинна викликати помилку
        with self.assertRaises(Exception):
            Language.objects.create(code='en', name='English UK')


# ============================================================================
# ПРИКЛАД 7: Інтеграційний тест
# ============================================================================

class ExampleIntegrationTest(TestCase):
    """Приклад інтеграційного тесту"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.language_en = Language.objects.create(code='en', name='English')
        self.language_uk = Language.objects.create(code='uk', name='Ukrainian')
        self.goal = Goal.objects.create(name='Travel')
    
    def test_complete_workflow(self):
        """Тест повного процесу роботи користувача"""
        # 1. Логін
        self.client.login(username='testuser', password='testpass123')
        
        # 2. Редагування профілю
        profile_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'native_language': self.language_uk.id,
            'timezone': 'Europe/Kiev',
            'goals': [self.goal.id],
        }
        response = self.client.post(reverse('profile_edit'), data=profile_data)
        self.assertEqual(response.status_code, 302)
        
        # 3. Додавання мови для вивчення
        language_data = {
            'language': self.language_en.id,
            'proficiency': 'B2',
        }
        response = self.client.post(reverse('add_language'), data=language_data)
        self.assertEqual(response.status_code, 302)
        
        # 4. Перевірка результатів
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.native_language, self.language_uk)
        
        user_language = UserLanguage.objects.get(user=self.user)
        self.assertEqual(user_language.language, self.language_en)
        self.assertEqual(user_language.proficiency, 'B2')


# ============================================================================
# ПРИКЛАД 8: Тест з множинними assertions
# ============================================================================

class ExampleMultipleAssertionsTest(TestCase):
    """Приклад тесту з множинними перевірками"""
    
    def test_user_creation_comprehensive(self):
        """Комплексний тест створення користувача"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        
        # Перевірка базових полів
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        
        # Перевірка паролю
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.check_password('wrongpassword'))
        
        # Перевірка дефолтних значень
        self.assertEqual(user.timezone, 'UTC')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


# ============================================================================
# КОРИСНІ ASSERTION МЕТОДИ
# ============================================================================

"""
Найбільш використовувані assertion методи:

# Рівність
self.assertEqual(a, b)           # a == b
self.assertNotEqual(a, b)        # a != b

# Істинність
self.assertTrue(x)               # bool(x) is True
self.assertFalse(x)              # bool(x) is False

# Наявність
self.assertIsNone(x)             # x is None
self.assertIsNotNone(x)          # x is not None

# Типи
self.assertIsInstance(a, b)      # isinstance(a, b)
self.assertNotIsInstance(a, b)   # not isinstance(a, b)

# Колекції
self.assertIn(a, b)              # a in b
self.assertNotIn(a, b)           # a not in b

# Винятки
self.assertRaises(Exception)     # Перевірка що виникає виняток

# HTTP
self.assertEqual(response.status_code, 200)
self.assertRedirects(response, url)
self.assertTemplateUsed(response, 'template.html')

# Форми
self.assertTrue(form.is_valid())
self.assertIn('field', form.errors)

# Queryset
self.assertEqual(Model.objects.count(), 5)
self.assertTrue(Model.objects.filter(name='test').exists())
"""


# ============================================================================
# НАЙКРАЩІ ПРАКТИКИ
# ============================================================================

"""
1. ІЗОЛЯЦІЯ ТЕСТІВ
   - Кожен тест повинен бути незалежним
   - Використовуйте setUp() для підготовки даних
   - Не покладайтесь на порядок виконання тестів

2. ОПИСОВІ НАЗВИ
   - Використовуйте зрозумілі назви тестів
   - Назва повинна описувати що тестується
   - Приклад: test_user_cannot_login_with_wrong_password

3. ОДИН ТЕСТ - ОДНА ПЕРЕВІРКА
   - Кожен тест повинен перевіряти одну конкретну річ
   - Якщо тест падає, повинно бути зрозуміло що саме не працює

4. ВИКОРИСТОВУЙТЕ DOCSTRINGS
   - Додавайте документацію до тестів
   - Поясніть що і чому тестується

5. ТЕСТУЙТЕ EDGE CASES
   - Тестуйте граничні випадки
   - Тестуйте помилкові сценарії
   - Тестуйте валідацію

6. ПІДТРИМУЙТЕ ТЕСТИ
   - Оновлюйте тести при зміні коду
   - Видаляйте застарілі тести
   - Рефакторьте тести разом з кодом
"""
