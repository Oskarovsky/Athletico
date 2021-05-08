from django.test import TestCase
from django.urls import reverse


class TestPage(TestCase):
    def test_add_exercise_page_works(self):
        response = self.client.get(reverse('add_exercise'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_exercise.html')
        self.assertContains(response, 'Athletico')

    def test_home_page_works(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'Athletico')
