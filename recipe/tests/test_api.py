from rest_framework import status
from rest_framework.test import APITestCase
from users.models import CustomUser
from recipe.models import Recipe, RecipeCategory, RecipeLike
from rest_framework_simplejwt.tokens import RefreshToken


class RecipeAPITests(APITestCase):

    def setUp(self):
        self.recipe = {}
        self.user_data = {
            'email': 'testuser@gmail.com',
            'username': 'testuser',
            'password': 'securepassword'
        }

        # Create a user
        self.user = CustomUser.objects.create_user(**self.user_data)

        # Obtain JWT token for the user
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # Create a recipe category
        self.category = RecipeCategory.objects.create(name='Sweets')

        # Recipe URL
        self.recipe_url = 'http://127.0.0.1:8000/api/recipe/'

        # Create a recipe for like/dislike tests
        self.recipe = Recipe.objects.create(
            author=self.user,
            category=self.category,
            picture="https://images.unsplash.com/photo-1722925541442-dc863f63a66c?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            title="Barfi",
            desc="A delicious barfi recipe.",
            cook_time="00:45:00",
            ingredients="Flour, Sugar, Cocoa Powder, Eggs, Butter",
            procedure="1. Preheat the oven to 350°F. 2. Mix all ingredients. 3. Bake for 30 minutes."
        )

    def test_create_recipe(self):
        data = {
            "category": {
                "id": self.category.id,
                "name": "Sweets"
            },
            "picture": "https://images.unsplash.com/photo-1722925541442-dc863f63a66c?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            "title": "Barfi",
            "desc": "A delicious barfi cake recipe.",
            "cook_time": "00:45:00",
            "ingredients": "Flour, Sugar, Cocoa Powder, Eggs, Butter",
            "procedure": "1. Preheat the oven to 350°F. 2. Mix all ingredients. 3. Bake for 30 minutes."
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = self.client.post(self.recipe_url + 'create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 2)
        recipe = Recipe.objects.filter(title='Barfi').first()
        self.assertEqual(recipe.title, 'Barfi')
        self.assertEqual(recipe.category.id, self.category.id)

    def test_get_recipe(self):
        # Include the access token in the Authorization header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Access the created recipe by its ID
        response = self.client.get(f'{self.recipe_url}{self.recipe.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Barfi')

    def test_like_recipe(self):
        # Include the access token in the Authorization header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Send POST request to like the recipe
        like_url = f'{self.recipe_url}{self.recipe.id}/like/'
        response = self.client.post(like_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RecipeLike.objects.count(), 1)
        self.assertEqual(RecipeLike.objects.get().recipe.id, self.recipe.id)

    def test_dislike_recipe(self):
        # First, like the recipe
        RecipeLike.objects.create(user=self.user, recipe=self.recipe)

        # Include the access token in the Authorization header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Send DELETE request to dislike the recipe
        like_url = f'{self.recipe_url}{self.recipe.id}/like/'
        response = self.client.delete(like_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(RecipeLike.objects.count(), 0)
