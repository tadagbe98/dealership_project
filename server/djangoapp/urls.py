from django.urls import path
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # Dealer endpoints
    path('get_dealers', views.get_dealerships, name='get_dealers'),
    path('get_dealers/<str:state>', views.get_dealerships, name='get_dealers_by_state'),
    path('dealer/<int:dealer_id>', views.get_dealer_details, name='dealer_details'),
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='dealer_reviews'),
    path('add_review', views.add_review, name='add_review'),
    
    # Car endpoints
    path('get_cars', views.get_cars, name='get_cars'),
    
    # Auth endpoints
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('register', views.registration, name='register'),
    
    # Sentiment analysis
    path('analyze_review', views.analyze_review, name='analyze_review'),
]
