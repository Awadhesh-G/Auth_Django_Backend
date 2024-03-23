from django.shortcuts import render, redirect
from .models import Item, Review
from .forms import ReviewForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.helpers import complete_social_login
from django.contrib.auth import login
from django.conf import settings
from allauth.socialaccount import signals
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.models import SocialApp , SocialToken

def profile(request):
    return render(request, 'profile.html')

def get_username(request):
    if request.user.is_authenticated:
        return JsonResponse({'username': request.user.username})
    else:
        return JsonResponse({'username': None})

# views.py


def item_detail(request, item_id):
    item = Item.objects.get(pk=item_id)
    reviews = Review.objects.filter(item=item)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.item = item
            review.save()
            return redirect('item_detail', item_id=item_id)
    else:
        form = ReviewForm()
    return render(request, 'item_detail.html', {'item': item, 'reviews': reviews, 'form': form})


@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        print("here")
        print("here")
        print("here")
        print("here")
        # Extract signup data from request
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Create new user
        user = User.objects.create_user(username=username, password=password , email=email)

        # Optionally, authenticate and login the user
        # authenticate_user = authenticate(request, username=username, password=password)
        # login(request, authenticate_user)

        return JsonResponse({'message': 'Signup successful'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def login_view(request):
    if request.method == 'POST':
        # Extract login data from request
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login user
            login(request, user)
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    

@csrf_exempt
def google_signup_view(request):
    adapter = GoogleOAuth2Adapter(request)
    
    try:
        # Retrieve the access token from the query parameters
        access_token = request.GET.get('access_token')
        
        # Retrieve the SocialApp for Google provider
        app = SocialApp.objects.get(provider='google')
        
        # Create a SocialToken instance with the access token
        social_token = SocialToken(app=app, token=access_token)
        
        # Complete the social login process
        login_request = adapter.complete_login(request, app, social_token)
        
        # Log in the user
        login(request, login_request.user)
        
        return JsonResponse({'message': 'Google signup successful'})

    except SocialApp.DoesNotExist:
        return JsonResponse({'error': 'SocialApp for Google provider does not exist'}, status=400)
    
    except OAuth2Error as e:
        return JsonResponse({'error': 'Failed to authenticate with Google'}, status=400)

    except Exception as e:
        return JsonResponse({'error': 'An error occurred during Google signup'}, status=500)