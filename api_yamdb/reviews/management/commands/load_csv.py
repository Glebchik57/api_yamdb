import os
from csv import DictReader

from django.conf import settings
from django.core.management import BaseCommand
from reviews.models import Categories, Comment, Genres, Review, Title, User

MODEL_LST = {
    'category.csv': Categories,
    'genre.csv': Genres,
    'titles.csv': Title,
    'comments.csv': Comment,
    'review.csv': Review,
    'users.csv': User
}


class Command(BaseCommand):
    help = 'Читает csv файл и заносит в базу данных'

    def handle(self, *args, **options):
        for csvname, mod in MODEL_LST.items():
            path = os.path.join(settings.BASE_DIR, f"static/data/{csvname}")
            with open(path, encoding='utf-8') as file:
                reader = DictReader(file)
                mod.objects.all().delete()
                header = [i for i in reader]
                for row in reader:
                    _object_dict = {key: value for key, value in zip(header,
                                                                     row)}
                    mod.objects.bulk_create([mod(**_object_dict)])
