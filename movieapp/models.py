from datetime import datetime
from django.contrib.auth.models import User as VisitOf
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    url = models.URLField(verbose_name='Ссылка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class User(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    age = models.IntegerField(verbose_name='Возраст')
    about = models.TextField(verbose_name='О себе')
    image = models.ImageField(upload_to='actors/%Y/%m/%d/', verbose_name='Изображение')
    url = models.URLField(verbose_name='Ссылка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Актер'
        verbose_name_plural = 'Актеры'


class Genre(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    url = models.URLField(verbose_name='Ссылка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Movie(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='movie/%Y/%m/%d/', verbose_name='Постер')
    year = models.DateField(auto_now=False)
    country = CountryField()
    directors = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='directors', verbose_name='Режиссер')
    actors = models.ManyToManyField(User, verbose_name='Актеры')
    genres = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='genre')
    world_premiere = models.DateField(auto_now=False,
                                      default=datetime.today().strftime('%Y-%m-%d'),
                                      verbose_name='Примьера в мире')
    budget = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Бюджет')
    fees_on_country = models.PositiveIntegerField(verbose_name='Сборы в городах')
    fees_on_world = models.PositiveIntegerField(verbose_name='Сборы по миру')
    slug = models.SlugField(unique=True, max_length=100)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = self.title
        super(Movie, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ['-year']
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class MovieShots(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movies_shots')
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='movie_shots', verbose_name='Изображение')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Кадры из фильма'


class Review(models.Model):
    visitOf = models.ForeignKey(VisitOf, on_delete=models.CASCADE, related_name='visits')
    text = models.TextField(verbose_name='Отзыв')
    reply = models.ForeignKey('self', verbose_name='Ответить',
                              on_delete=models.SET_NULL, null=True, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='review_movie')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = 'Отзывы'


class Votes(models.Model):
    visits = models.ForeignKey(VisitOf,
                               on_delete=models.CASCADE,
                               related_name='votes',
                               verbose_name='Пользователь')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='vote_movie')

    def __str__(self):
        return self.visits.username

    class Meta:
        verbose_name_plural = 'Голоса'