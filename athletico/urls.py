"""notifire URL Configuration
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

from athletico import views
from athletico.connector import send_message, make_as_read

urlpatterns = [
    path('', views.home, name='home'),
    path('exercise/', views.add_exercise, name='new_exercise'),
    path('stats/<str:exercise_type>/', views.show_stats, name='show_stats'),
    path('ajax/send-message/', send_message, name='send_message'),
    path('ajax/make-as-read/', make_as_read, name='make_as_read')
]