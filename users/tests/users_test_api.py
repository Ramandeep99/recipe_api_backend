from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import Profile  # Use absolute import
from recipe.models import Recipe, RecipeCategory  # Use absolute import

User = get_user_model()


class UserAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpass123')
        # Ensure the Profile is created automatically with the user
        self.profile, created = Profile.objects.get_or_create(user=self.user)
        self.category = RecipeCategory.objects.create(name='Sweets')

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

    def test_user_registration(self):
        url = reverse('users:create-user')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)

    def test_user_login(self):
        url = reverse('users:login-user')
        data = {
            'email': self.user.email,
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)

    def test_user_logout(self):
        refresh = RefreshToken.for_user(self.user)
        url = reverse('users:logout-user')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, {'refresh': str(refresh)})
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_get_user_info(self):
        url = reverse('users:user-info')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_update_user_profile(self):
        url = reverse('users:user-profile')
        data = {
            'bio': 'Updated bio'
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bio'], 'Updated bio')

    def test_user_bookmark_recipe(self):
        url = reverse('users:user-bookmark', kwargs={'pk': self.user.pk})
        data = {
            'id': self.recipe.id
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.recipe, self.user.profile.bookmarks.all())

    def test_user_remove_bookmark(self):
        # First, add the bookmark
        self.profile.bookmarks.add(self.recipe)

        url = reverse('users:user-bookmark', kwargs={'pk': self.user.pk})
        data = {
            'id': self.recipe.id
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.recipe, self.user.profile.bookmarks.all())

    def test_change_password(self):
        url = reverse('users:change-password')
        data = {
            'old_password': 'testpass123',
            'new_password': 'newtestpass123'
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.check_password('newtestpass123'))
