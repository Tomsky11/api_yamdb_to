# API для проекта YaMDb
Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий может быть расширен администратором.

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

В каждой категории есть произведения: книги, фильмы или музыка.

Произведению может быть присвоен жанр из списка предустановленных. Новые жанры может создавать только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.

### Запуск проекта локально

Клонируем репозиторий

```https://github.com/Tomsky11/api_yamdb```

Устанавливаем зависимости (предварительно установив и активировав виртуальное окружение)

```pip install -r requirements.txt```

Применяем миграции

```python manage.py migrate```

Запускаем проект

```python manage.py runserver```

Документация по API будет доступна по адресу

```http://127.0.0.1:8000/redoc/```
