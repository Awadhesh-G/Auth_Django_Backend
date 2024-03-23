from django.contrib import admin
from django.urls import path, include
from dashboard import views , api_views
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', views.profile, name="profile"),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('api/signup/', csrf_exempt(views.signup_view), name='signup'),
    path('api/login/', csrf_exempt(views.login_view), name='login'),
    path('api/google-signup/', views.google_signup_view, name='google_signup'),  # Custom URL for Google signup
    # path('api/items/', api_views.ItemListAPIView.as_view(), name='item-list'),
    # path('api/items/<int:pk>/', api_views.ItemDetailAPIView.as_view(), name='item-detail'),
    # path('api/reviews/', api_views.ReviewListCreateAPIView.as_view(), name='review-list'),
    path('api/reviews/<int:pk>/', api_views.ReviewDetailAPIView.as_view(), name='review-detail'),
    path('api/reviews/', csrf_exempt(api_views.review_create_api_view), name='review_create_api'),
    # path('api/reviews_get/', csrf_exempt(api_views.review_list_api_view), name='review_list_api'),
    # path('api/usernames/', api_views.username_list_api_view, name='username_list_api'),
    path('api/get-username/', views.get_username, name='get_username'),
]
