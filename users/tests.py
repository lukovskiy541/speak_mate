from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date
from .models import Language, Goal, Interest, UserLanguage
from .forms import UserProfileForm, UserLanguageForm

User = get_user_model()


class LanguageModelTest(TestCase):
    """Тести для моделі Language"""
    
    def test_create_language(self):
        """Тест створення мови"""
        language = Language.objects.create(code='en', name='English')
        self.assertEqual(language.code, 'en')
        self.assertEqual(language.name, 'English')
        self.assertEqual(str(language), 'English')
    
    def test_language_unique_code(self):
        """Тест унікальності коду мови"""
        Language.objects.create(code='en', name='English')
        with self.assertRaises(Exception):
            Language.objects.create(code='en', name='English UK')


class GoalModelTest(TestCase):
    """Тести для моделі Goal"""
    
    def test_create_goal(self):
        """Тест створення цілі"""
        goal = Goal.objects.create(name='Travel')
        self.assertEqual(goal.name, 'Travel')
        self.assertEqual(str(goal), 'Travel')


class InterestModelTest(TestCase):
    """Тести для моделі Interest"""
    
    def test_create_interest(self):
        """Тест створення інтересу"""
        interest = Interest.objects.create(name='Music')
        self.assertEqual(interest.name, 'Music')
        self.assertEqual(str(interest), 'Music')


class UserModelTest(TestCase):
    """Тести для моделі User"""
    
    def setUp(self):
        """Налаштування тестових даних"""
        self.language_en = Language.objects.create(code='en', name='English')
        self.language_uk = Language.objects.create(code='uk', name='Ukrainian')
        self.goal = Goal.objects.create(name='Travel')
        self.interest = Interest.objects.create(name='Music')
    
    def test_create_user(self):
        """Тест створення користувача"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertEqual(str(user), 'test@example.com')
    
    def test_user_with_native_language(self):
        """Тест користувача з рідною мовою"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            native_language=self.language_en
        )
        self.assertEqual(user.native_language, self.language_en)
    
    def test_user_with_goals_and_interests(self):
        """Тест користувача з цілями та інтересами"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        user.goals.add(self.goal)
        user.interests.add(self.interest)
        
        self.assertEqual(user.goals.count(), 1)
        self.assertEqual(user.interests.count(), 1)
        self.assertIn(self.goal, user.goals.all())
        self.assertIn(self.interest, user.interests.all())
    
    def test_user_default_timezone(self):
        """Тест дефолтного часового поясу"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.timezone, 'UTC')


class UserLanguageModelTest(TestCase):
    """Тести для моделі UserLanguage"""
    
    def setUp(self):
        """Налаштування тестових даних"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.language = Language.objects.create(code='en', name='English')
    
    def test_create_user_language(self):
        """Тест створення зв'язку користувач-мова"""
        user_language = UserLanguage.objects.create(
            user=self.user,
            language=self.language,
            proficiency='B1'
        )
        self.assertEqual(user_language.user, self.user)
        self.assertEqual(user_language.language, self.language)
        self.assertEqual(user_language.proficiency, 'B1')
        self.assertIn('testuser', str(user_language))
        self.assertIn('English', str(user_language))
        self.assertIn('B1', str(user_language))
    
    def test_user_language_unique_together(self):
        """Тест унікальності пари користувач-мова"""
        UserLanguage.objects.create(
            user=self.user,
            language=self.language,
            proficiency='B1'
        )
        with self.assertRaises(Exception):
            UserLanguage.objects.create(
                user=self.user,
                language=self.language,
                proficiency='B2'
            )
    
    def test_user_language_proficiency_choices(self):
        """Тест рівнів володіння мовою"""
        proficiency_levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
        for level in proficiency_levels:
            user_language = UserLanguage.objects.create(
                user=self.user,
                language=Language.objects.create(
                    code=f'lang_{level}',
                    name=f'Language {level}'
                ),
                proficiency=level
            )
            self.assertEqual(user_language.proficiency, level)


class UserProfileFormTest(TestCase):
    """Тести для форми UserProfileForm"""
    
    def setUp(self):
        """Налаштування тестових даних"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.language = Language.objects.create(code='en', name='English')
        self.goal = Goal.objects.create(name='Travel')
        self.interest = Interest.objects.create(name='Music')
    
    def test_valid_profile_form(self):
        """Тест валідної форми профілю"""
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'bio': 'Test bio',
            'birth_date': '1990-01-01',
            'native_language': self.language.id,
            'timezone': 'Europe/Kiev',
            'goals': [self.goal.id],
            'interests': [self.interest.id],
        }
        form = UserProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
    
    def test_empty_profile_form(self):
        """Тест порожньої форми профілю"""
        form = UserProfileForm(data={}, instance=self.user)
        # Форма може бути створена, навіть якщо не всі поля заповнені
        self.assertIsInstance(form, UserProfileForm)
    
    def test_profile_form_fields(self):
        """Тест наявності полів у формі"""
        form = UserProfileForm(instance=self.user)
        expected_fields = [
            'avatar', 'first_name', 'last_name', 'bio', 
            'birth_date', 'native_language', 'timezone', 
            'goals', 'interests'
        ]
        for field in expected_fields:
            self.assertIn(field, form.fields)


class UserLanguageFormTest(TestCase):
    """Тести для форми UserLanguageForm"""
    
    def setUp(self):
        """Налаштування тестових даних"""
        self.language = Language.objects.create(code='en', name='English')
    
    def test_valid_user_language_form(self):
        """Тест валідної форми мови користувача"""
        form_data = {
            'language': self.language.id,
            'proficiency': 'B1',
        }
        form = UserLanguageForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_user_language_form(self):
        """Тест невалідної форми мови користувача"""
        form_data = {
            'language': '',
            'proficiency': '',
        }
        form = UserLanguageForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('language', form.errors)
        self.assertIn('proficiency', form.errors)


class ProfileViewTest(TestCase):
    """Тести для view профілю"""
    
    def setUp(self):
        """Налаштування тестових даних"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile_url = reverse('profile')
    
    def test_profile_view_requires_login(self):
        """Тест що профіль вимагає авторизації"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)  # Редірект на логін
        self.assertIn('/accounts/login/', response.url)
    
    def test_profile_view_authenticated(self):
        """Тест профілю для авторизованого користувача"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertEqual(response.context['user'], self.user)


class ProfileEditViewTest(TestCase):
    """Тести для view редагування профілю"""
    
    def setUp(self):
        """Налаштування тестових даних"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.language = Language.objects.create(code='en', name='English')
        self.goal = Goal.objects.create(name='Travel')
        self.interest = Interest.objects.create(name='Music')
        self.edit_url = reverse('profile_edit')
    
    def test_profile_edit_view_requires_login(self):
        """Тест що редагування профілю вимагає авторизації"""
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
    
    def test_profile_edit_view_get(self):
        """Тест GET запиту на редагування профілю"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile_edit.html')
        self.assertIsInstance(response.context['form'], UserProfileForm)
    
    def test_profile_edit_view_post_valid(self):
        """Тест POST запиту з валідними даними"""
        self.client.login(username='testuser', password='testpass123')
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'bio': 'Updated bio',
            'birth_date': '1990-01-01',
            'native_language': self.language.id,
            'timezone': 'Europe/Kiev',
            'goals': [self.goal.id],
            'interests': [self.interest.id],
        }
        response = self.client.post(self.edit_url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))
        
        # Перевірка що дані збережено
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.bio, 'Updated bio')
    
    def test_profile_edit_view_post_invalid(self):
        """Тест POST запиту з невалідними даними"""
        self.client.login(username='testuser', password='testpass123')
        form_data = {
            'birth_date': 'invalid-date',
        }
        response = self.client.post(self.edit_url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile_edit.html')


class AddLanguageViewTest(TestCase):
    """Тести для view додавання мови"""
    
    def setUp(self):
        """Налаштування тестових даних"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.language = Language.objects.create(code='en', name='English')
        self.add_language_url = reverse('add_language')
    
    def test_add_language_view_requires_login(self):
        """Тест що додавання мови вимагає авторизації"""
        response = self.client.get(self.add_language_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
    
    def test_add_language_view_get(self):
        """Тест GET запиту на додавання мови"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.add_language_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/add_language.html')
        self.assertIsInstance(response.context['form'], UserLanguageForm)
    
    def test_add_language_view_post_valid(self):
        """Тест POST запиту з валідними даними"""
        self.client.login(username='testuser', password='testpass123')
        form_data = {
            'language': self.language.id,
            'proficiency': 'B1',
        }
        response = self.client.post(self.add_language_url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))
        
        # Перевірка що мова додана
        user_language = UserLanguage.objects.filter(
            user=self.user,
            language=self.language
        ).first()
        self.assertIsNotNone(user_language)
        self.assertEqual(user_language.proficiency, 'B1')
    
    def test_add_language_view_post_invalid(self):
        """Тест POST запиту з невалідними даними"""
        self.client.login(username='testuser', password='testpass123')
        form_data = {
            'language': '',
            'proficiency': '',
        }
        response = self.client.post(self.add_language_url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/add_language.html')
        
        # Перевірка що мова не додана
        self.assertEqual(UserLanguage.objects.filter(user=self.user).count(), 0)


class IntegrationTest(TestCase):
    """Інтеграційні тести"""
    
    def setUp(self):
        """Налаштування тестових даних"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.language_en = Language.objects.create(code='en', name='English')
        self.language_uk = Language.objects.create(code='uk', name='Ukrainian')
        self.goal = Goal.objects.create(name='Travel')
        self.interest = Interest.objects.create(name='Music')
    
    def test_complete_user_profile_workflow(self):
        """Тест повного процесу налаштування профілю"""
        # Логін
        self.client.login(username='testuser', password='testpass123')
        
        # Редагування профілю
        profile_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'bio': 'Language learner',
            'birth_date': '1990-01-01',
            'native_language': self.language_uk.id,
            'timezone': 'Europe/Kiev',
            'goals': [self.goal.id],
            'interests': [self.interest.id],
        }
        response = self.client.post(reverse('profile_edit'), data=profile_data)
        self.assertEqual(response.status_code, 302)
        
        # Додавання мови
        language_data = {
            'language': self.language_en.id,
            'proficiency': 'B2',
        }
        response = self.client.post(reverse('add_language'), data=language_data)
        self.assertEqual(response.status_code, 302)
        
        # Перевірка результатів
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.native_language, self.language_uk)
        self.assertEqual(self.user.goals.count(), 1)
        self.assertEqual(self.user.interests.count(), 1)
        
        user_language = UserLanguage.objects.get(user=self.user)
        self.assertEqual(user_language.language, self.language_en)
        self.assertEqual(user_language.proficiency, 'B2')
    
    def test_user_can_learn_multiple_languages(self):
        """Тест що користувач може вивчати декілька мов"""
        self.client.login(username='testuser', password='testpass123')
        
        # Додавання першої мови
        language_data_1 = {
            'language': self.language_en.id,
            'proficiency': 'B1',
        }
        self.client.post(reverse('add_language'), data=language_data_1)
        
        # Додавання другої мови
        language_data_2 = {
            'language': self.language_uk.id,
            'proficiency': 'A2',
        }
        self.client.post(reverse('add_language'), data=language_data_2)
        
        # Перевірка
        self.assertEqual(UserLanguage.objects.filter(user=self.user).count(), 2)
        languages = self.user.learning_languages.all()
        self.assertEqual(languages.count(), 2)
        self.assertIn(self.language_en, languages)
        self.assertIn(self.language_uk, languages)
