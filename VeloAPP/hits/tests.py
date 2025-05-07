from django.test import TestCase, Client
from django.urls import reverse
from hits.models import Artist, Hit
from django.utils.text import slugify
import json

# Create your tests here.

class HitAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Tworzenie przykładowych artystów
        self.artist1 = Artist.objects.create(first_name='Jan', last_name='Kowalski')
        self.artist2 = Artist.objects.create(first_name='Anna', last_name='Nowak')
        # Tworzenie przykładowych hitów
        self.hit1 = Hit.objects.create(title='Hit One', artist=self.artist1, title_url=slugify('Hit One'))
        self.hit2 = Hit.objects.create(title='Hit Two', artist=self.artist2, title_url=slugify('Hit Two'))

    def test_get_hits_list(self):
        url = reverse('hit-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) <= 20)

    def test_get_hit_detail(self):
        url = reverse('hit-detail', kwargs={'title_url': self.hit1.title_url})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], self.hit1.title)

    def test_get_hit_detail_not_found(self):
        url = reverse('hit-detail', kwargs={'title_url': 'non-existent'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_post_create_hit(self):
        url = reverse('hit-create')
        data = {
            'title': 'New Hit',
            'artist': self.artist1.id
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['title'], 'New Hit')
        self.assertEqual(response.json()['artist'], self.artist1.id)

    def test_post_create_hit_invalid(self):
        url = reverse('hit-create')
        data = {
            'artist': self.artist1.id
        }  # Brak tytułu
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_put_update_hit(self):
        url = reverse('hit-update', kwargs={'title_url': self.hit1.title_url})
        data = {
            'title': 'Updated Hit',
            'artist': self.artist2.id
        }
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Updated Hit')
        self.assertEqual(response.json()['artist'], self.artist2.id)

    def test_put_update_hit_not_found(self):
        url = reverse('hit-update', kwargs={'title_url': 'non-existent'})
        data = {'title': 'Updated Hit'}
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_delete_hit(self):
        url = reverse('hit-delete', kwargs={'title_url': self.hit1.title_url})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        # Sprawdzenie, czy został usunięty
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_hit_not_found(self):
        url = reverse('hit-delete', kwargs={'title_url': 'non-existent'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)