from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):

    def test_recipe_home_views_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertTrue(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<div class="center m-y">',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertIn('Recipe Title', content)
        self.assertIn('10 Minutos', content)
        self.assertIn('5 Porções', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template__dont_loads_recipes_not_published(self):
        '''test recipe is_published False dont show'''
        # need a recipe for this test
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')

        self.assertIn('<div class="center m-y">', content)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category test'
        self.make_recipe(title=needed_title)

        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))
        content = response.content.decode('utf-8')

        self.assertIn(needed_title, content)

    def test_recipe_category_template__dont_loads_recipes_not_published(self):
        '''test recipe is_published False dont show'''
        # need a recipe for this test
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse('recipes:category',
                    kwargs={'category_id': recipe.category.id}))

        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = 'This is a detail page - It load one recipe'

        # need a recipe for this test
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:recipe',
                                           kwargs={'id': 1}))
        content = response.content.decode('utf-8')

        # need if one recipe exists
        self.assertIn(needed_title, content)

    def test_recipe_detail_template__dont_loads_recipe_not_published(self):
        '''test recipe is_published False dont show'''
        # need a recipe for this test
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:recipe',
                                           kwargs={'id': recipe.id}))

        self.assertEqual(response.status_code, 404)

    def test_recipe_search_uses_correct_view_function(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertTemplateUsed(response, 'recipes/pages/search.html')
