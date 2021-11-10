from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from .validators import validate_year


class Role(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):

    email = models.EmailField('email address', blank=False, unique=True)
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
    )
    confirmation_code = models.CharField(max_length=100, blank=True, )

    def __str__(self):
        return self.email

    @property
    def is_moderator(self):
        return self.role == Role.MODERATOR

    @property
    def is_admin(self):
        return (
            self.role == Role.ADMIN or self.is_staff or self.is_superuser
        )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Categories(models.Model):
    name = models.CharField(db_index=True,
                            max_length=200,
                            verbose_name='категория произведения')
    slug = models.SlugField(max_length=20,
                            unique=True,
                            verbose_name='короткая метка')

    def __str__(self):
        return f'{self.pk} - {self.name} - {self.slug}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genres(models.Model):
    name = models.CharField(db_index=True,
                            max_length=200,
                            verbose_name='жанр произведения')
    slug = models.SlugField(max_length=20,
                            unique=True,
                            verbose_name='короткая метка')

    def __str__(self):
        return f'{self.pk} - {self.name} - {self.slug}'

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Titles(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='название произведения')
    year = models.IntegerField(validators=[validate_year],
                               db_index=True,
                               verbose_name='год выпуска')
    description = models.TextField(blank=True,
                                   verbose_name='описание произведения')
    genre = models.ManyToManyField(Genres,
                                   blank=True,
                                   related_name='genre_titles',
                                   verbose_name='выберите жанр')
    category = models.ForeignKey(Categories,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='category_titles',
                                 verbose_name='выберите категорию')

    def __str__(self):
        return f'{self.pk} - {self.name[:20]} - {self.category}'

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Reviews(models.Model):
    title = models.ForeignKey(Titles,
                              on_delete=models.CASCADE,
                              verbose_name='произведение',
                              related_name='reviews_title')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews',
                               verbose_name='автор отзыва')
    text = models.TextField(verbose_name='текст отзыва')

    score = models.IntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1, message='Оценка не может быть меньше 1'),
            MaxValueValidator(10, message='Оценка не может быть больше 10')
        ])

    pub_date = models.DateTimeField(verbose_name='дата добавления',
                                    auto_now_add=True,
                                    db_index=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ['author', 'title']


class Comment(models.Model):
    review = models.ForeignKey(Reviews,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='отзыв')
    text = models.TextField(verbose_name='текст комментария')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='автор комментария')
    pub_date = models.DateTimeField(verbose_name='Дата добавления',
                                    auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
