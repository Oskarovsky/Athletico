"""Athletico URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.views.generic import TemplateView

from athletico import views
from athletico.connector import send_message, make_as_read

urlpatterns = [
    path(
        '',
        TemplateView.as_view(template_name='home.html'),
        name='home'
    ),
    path(
        'exercise/',
        views.AddExerciseView.add_exercise,
        name='add_exercise'
    ),
    path(
        'exercise2/',
        views.AddExerciseView.as_view(),
        name='add_exercise2'
    ),
    path('stats/<str:exercise_type>/', views.show_stats, name='show_stats'),
    path('ajax/send-message/', send_message, name='send_message'),
    path('ajax/make-as-read/', make_as_read, name='make_as_read')
]