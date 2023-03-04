from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator


class Categories(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название жанра')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название произведения')
    year = models.IntegerField(verbose_name='Год создания произведения',
                               validators=[MinValueValidator(1895),
                                           MaxValueValidator(datetime.now().year)])
    description = models.TextField(verbose_name='Описание произведения')
    genre = models.ManyToManyField(
        Genres,
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Categories,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    class Meta:
        verbose_name = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    score = models.IntegerField()