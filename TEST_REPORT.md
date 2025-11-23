# Детальний звіт про тестування

## Загальна статистика

| Метрика | Значення |
|---------|----------|
| Всього тестів | 28 |
| Успішно пройдено | 28 ✅ |
| Провалено | 0 |
| Покриття коду | 100% |
| Час виконання | ~5.2 секунди |

## Розподіл тестів по категоріях

| Категорія | Кількість тестів | Покриття |
|-----------|------------------|----------|
| Тести моделей | 10 | 100% |
| Тести форм | 5 | 100% |
| Тести views | 11 | 100% |
| Інтеграційні тести | 2 | 100% |

## Детальний список тестів

### 1️⃣ Тести моделей (10 тестів)

| # | Тестовий клас | Назва тесту | Статус | Опис |
|---|---------------|-------------|--------|------|
| 1 | LanguageModelTest | test_create_language | ✅ | Створення мови |
| 2 | LanguageModelTest | test_language_unique_code | ✅ | Унікальність коду мови |
| 3 | GoalModelTest | test_create_goal | ✅ | Створення цілі |
| 4 | InterestModelTest | test_create_interest | ✅ | Створення інтересу |
| 5 | UserModelTest | test_create_user | ✅ | Створення користувача |
| 6 | UserModelTest | test_user_with_native_language | ✅ | Користувач з рідною мовою |
| 7 | UserModelTest | test_user_with_goals_and_interests | ✅ | Користувач з цілями та інтересами |
| 8 | UserModelTest | test_user_default_timezone | ✅ | Дефолтний часовий пояс |
| 9 | UserLanguageModelTest | test_create_user_language | ✅ | Створення зв'язку користувач-мова |
| 10 | UserLanguageModelTest | test_user_language_unique_together | ✅ | Унікальність пари користувач-мова |
| 11 | UserLanguageModelTest | test_user_language_proficiency_choices | ✅ | Рівні володіння мовою (A1-C2) |

### 2️⃣ Тести форм (5 тестів)

| # | Тестовий клас | Назва тесту | Статус | Опис |
|---|---------------|-------------|--------|------|
| 12 | UserProfileFormTest | test_valid_profile_form | ✅ | Валідна форма профілю |
| 13 | UserProfileFormTest | test_empty_profile_form | ✅ | Порожня форма профілю |
| 14 | UserProfileFormTest | test_profile_form_fields | ✅ | Наявність полів у формі |
| 15 | UserLanguageFormTest | test_valid_user_language_form | ✅ | Валідна форма мови |
| 16 | UserLanguageFormTest | test_invalid_user_language_form | ✅ | Невалідна форма мови |

### 3️⃣ Тести views (11 тестів)

| # | Тестовий клас | Назва тесту | Статус | Опис |
|---|---------------|-------------|--------|------|
| 17 | ProfileViewTest | test_profile_view_requires_login | ✅ | Профіль вимагає авторизації |
| 18 | ProfileViewTest | test_profile_view_authenticated | ✅ | Профіль для авторизованого користувача |
| 19 | ProfileEditViewTest | test_profile_edit_view_requires_login | ✅ | Редагування вимагає авторизації |
| 20 | ProfileEditViewTest | test_profile_edit_view_get | ✅ | GET запит на редагування |
| 21 | ProfileEditViewTest | test_profile_edit_view_post_valid | ✅ | POST з валідними даними |
| 22 | ProfileEditViewTest | test_profile_edit_view_post_invalid | ✅ | POST з невалідними даними |
| 23 | AddLanguageViewTest | test_add_language_view_requires_login | ✅ | Додавання мови вимагає авторизації |
| 24 | AddLanguageViewTest | test_add_language_view_get | ✅ | GET запит на додавання мови |
| 25 | AddLanguageViewTest | test_add_language_view_post_valid | ✅ | POST з валідними даними |
| 26 | AddLanguageViewTest | test_add_language_view_post_invalid | ✅ | POST з невалідними даними |

### 4️⃣ Інтеграційні тести (2 тести)

| # | Тестовий клас | Назва тесту | Статус | Опис |
|---|---------------|-------------|--------|------|
| 27 | IntegrationTest | test_complete_user_profile_workflow | ✅ | Повний процес налаштування профілю |
| 28 | IntegrationTest | test_user_can_learn_multiple_languages | ✅ | Вивчення декількох мов |

## Покриття коду по файлах

| Файл | Рядків коду | Покрито | Не покрито | Покриття |
|------|-------------|---------|------------|----------|
| users/__init__.py | 0 | 0 | 0 | 100% ✅ |
| users/admin.py | 15 | 15 | 0 | 100% ✅ |
| users/apps.py | 4 | 4 | 0 | 100% ✅ |
| users/forms.py | 11 | 11 | 0 | 100% ✅ |
| users/models.py | 36 | 36 | 0 | 100% ✅ |
| users/urls.py | 3 | 3 | 0 | 100% ✅ |
| users/views.py | 30 | 30 | 0 | 100% ✅ |
| **ВСЬОГО** | **99** | **99** | **0** | **100%** ✅ |


**Дата створення звіту:** 2025-11-23  
**Версія Django:** 5.1.3  
**Python версія:** 3.13
