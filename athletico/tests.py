from django.test import TestCase


class TestPage(TestCase):
    def test_base_page_works(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertContains(response, 'Athletico')
