from django.core.management.base import BaseCommand
from hits.models import Artist, Hit
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Wypełnia bazę przykładowymi danymi'

    def handle(self, *args, **kwargs):
        artists = [
            Artist.objects.create(first_name='Jan', last_name='Kowalski'),
            Artist.objects.create(first_name='Anna', last_name='Nowak'),
            Artist.objects.create(first_name='Piotr', last_name='Zieliński'),
        ]
        for i in range(1, 21):
            title = f'Hit numer {i}'
            Hit.objects.create(
                title=title,
                artist=artists[i % 3],
                title_url=slugify(title)
            )
        self.stdout.write(self.style.SUCCESS('Dodano przykładowe dane!'))
