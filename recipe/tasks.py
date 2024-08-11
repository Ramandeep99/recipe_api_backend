from celery import shared_task
from django.core.mail import send_mail
from .models import RecipeLike
from django.contrib.auth import get_user_model
from datetime import date
from collections import defaultdict

User = get_user_model()

@shared_task
def send_daily_likes_summary():
    today = date.today()
    users = User.objects.all()

    # Create a dictionary to store likes by user and recipe
    user_likes = defaultdict(lambda: defaultdict(int))

    # Populate the dictionary with the count of likes per recipe for each user
    liked_recipes = RecipeLike.objects.filter(created__date=today)
    for like in liked_recipes:
        user_likes[like.user][like.recipe.title] += 1

    # Send an email to each user with the summary of likes
    for user, recipes in user_likes.items():
        if recipes:
            # Prepare the email content
            recipe_summary = '\n'.join(f'{recipe_title}: {count} likes' for recipe_title, count in recipes.items())
            email_content = f'Your recipes received the following likes today:\n\n{recipe_summary}'

            send_mail(
                subject='Daily Likes Summary',
                message=email_content,
                from_email='ramandeep@repup.co',
                recipient_list=[user.email],
                fail_silently=False
            )
