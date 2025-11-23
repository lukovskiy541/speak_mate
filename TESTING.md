# Документація тестування SpeakMate

## Огляд

Проект SpeakMate містить комплексний набір модульних тестів, які покривають всі основні компоненти додатку `users`. Загалом створено **28 тестів**, які забезпечують **100% покриття коду**.

## Статистика покриття

```
Name                               Stmts   Miss  Cover
------------------------------------------------------
users/__init__.py                      0      0   100%
users/admin.py                        15      0   100%
users/apps.py                          4      0   100%
users/forms.py                        11      0   100%
users/migrations/0001_initial.py      10      0   100%
users/migrations/__init__.py           0      0   100%
users/models.py                       36      0   100%
users/tests.py                       222      0   100%
users/urls.py                          3      0   100%
users/views.py                        30      0   100%
------------------------------------------------------
TOTAL                                331      0   100%
```

## Структура тестів

### 1. Тести моделей (10 тестів)

#### LanguageModelTest (2 тести)
- `test_create_language` - Перевірка створення мови
- `test_language_unique_code` - Перевірка унікальності коду мови

#### GoalModelTest (1 тест)
- `test_create_goal` - Перевірка створення цілі навчання

#### InterestModelTest (1 тест)
- `test_create_interest` - Перевірка створення інтересу

#### UserModelTest (4 тести)
- `test_create_user` - Перевірка створення користувача
- `test_user_with_native_language` - Перевірка користувача з рідною мовою
- `test_user_with_goals_and_interests` - Перевірка користувача з цілями та інтересами
- `test_user_default_timezone` - Перевірка дефолтного часового поясу

#### UserLanguageModelTest (3 тести)
- `test_create_user_language` - Перевірка створення зв'язку користувач-мова
- `test_user_language_unique_together` - Перевірка унікальності пари користувач-мова
- `test_user_language_proficiency_choices` - Перевірка всіх рівнів володіння мовою (A1-C2)

### 2. Тести форм (5 тестів)

#### UserProfileFormTest (3 тести)
- `test_valid_profile_form` - Перевірка валідної форми профілю
- `test_empty_profile_form` - Перевірка створення порожньої форми
- `test_profile_form_fields` - Перевірка наявності всіх необхідних полів

#### UserLanguageFormTest (2 тести)
- `test_valid_user_language_form` - Перевірка валідної форми додавання мови
- `test_invalid_user_language_form` - Перевірка невалідної форми

### 3. Тести views (11 тестів)

#### ProfileViewTest (2 тести)
- `test_profile_view_requires_login` - Перевірка що профіль вимагає авторизації
- `test_profile_view_authenticated` - Перевірка відображення профілю для авторизованого користувача

#### ProfileEditViewTest (4 тести)
- `test_profile_edit_view_requires_login` - Перевірка що редагування вимагає авторизації
- `test_profile_edit_view_get` - Перевірка GET запиту на редагування
- `test_profile_edit_view_post_valid` - Перевірка успішного збереження даних
- `test_profile_edit_view_post_invalid` - Перевірка обробки невалідних даних

#### AddLanguageViewTest (4 тести)
- `test_add_language_view_requires_login` - Перевірка що додавання мови вимагає авторизації
- `test_add_language_view_get` - Перевірка GET запиту на додавання мови
- `test_add_language_view_post_valid` - Перевірка успішного додавання мови
- `test_add_language_view_post_invalid` - Перевірка обробки невалідних даних

### 4. Інтеграційні тести (2 тести)

#### IntegrationTest (2 тести)
- `test_complete_user_profile_workflow` - Перевірка повного процесу налаштування профілю (редагування + додавання мови)
- `test_user_can_learn_multiple_languages` - Перевірка можливості вивчати декілька мов одночасно


## Що покривають тести

### Моделі
✅ Створення та валідація всіх моделей  
✅ Унікальні обмеження  
✅ Зв'язки між моделями (ForeignKey, ManyToMany)  
✅ Методи `__str__`  
✅ Дефолтні значення  
✅ Choices для полів  

### Форми
✅ Валідація форм з коректними даними  
✅ Валідація форм з некоректними даними  
✅ Наявність всіх необхідних полів  
✅ Віджети форм  

### Views
✅ Авторизація (login_required)  
✅ GET запити  
✅ POST запити з валідними даними  
✅ POST запити з невалідними даними  
✅ Редіректи  
✅ Використання правильних шаблонів  
✅ Контекст шаблонів  
✅ Збереження даних в базу  

### Інтеграція
✅ Повний workflow користувача  
✅ Взаємодія між різними компонентами  
✅ Складні сценарії використання  


