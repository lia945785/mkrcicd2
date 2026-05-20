from django.test import TestCase
from django.urls import reverse
from .models import Category, Recipe

class RecipeViewsTestCase(TestCase):
    def setUp(self):
        # Створюємо тестову категорію та рецепт в базі даних для перевірок
        self.category = Category.objects.create(name="Десерти")
        self.recipe = Recipe.objects.create(
            title="Наполеон",
            description="Традиційний десерт",
            ingredients="Крем, тісто",
            instructions="Запекти",
            category=self.category
        )

    def test_main_page(self):
        # Тестуємо головну сторінку з випадковими рецептами
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
        #  чи є на головній кнопка переходу до категорій
        self.assertContains(response, 'Перейти до категорій')

    def test_category_list_page(self):
        # Тестуємо сторінку зі списком усіх категорій
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category_list.html')
        # Чит відображається назва категорії та кнопка переходу
        self.assertContains(response, 'Десерти')
        self.assertContains(response, 'Перейти до:')

    def test_category_detail_page(self):
        # Тестуємо сторінку конкретної категорії за id
        response = self.client.get(reverse('category_detail', args=[self.category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category_detail.html')
        # Перевіряємо, чи вивівся рецепт, що належить цій категорії
        self.assertContains(response, 'Наполеон')

    def test_category_detail_404(self):
        # Перевіряємо, що при неіснуючому id повертається 404 помилка
        response = self.client.get(reverse('category_detail', args=[999]))
        self.assertEqual(response.status_code, 404)