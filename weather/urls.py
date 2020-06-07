from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('city/', views.IndexView.as_view(), name='city_weather'),
    path('mood/', views.moodview, name='register_mood'),
    path('moods/', views.moodlist, name='mood_page'),
    
    
]