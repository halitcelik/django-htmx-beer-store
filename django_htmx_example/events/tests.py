from django.test import TestCase
class HomePageTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()
        
    def test_root_url_resolves_to_index_view(self):
        response = self.client.get("/", follow=True)
        self.assertTemplateUsed(response, "pages/home.html")

    def test_article_is_displayed(self):
        response = self.client.get(self.article.get_absolute_url())
        self.assertIn(self.article.title, response.content.decode())
        self.assertTemplateUsed(response, "blog/includes/article.html")
    
    def test_article_has_a_tag(self):
        self.assertIsNotNone(self.article.tags.first())
