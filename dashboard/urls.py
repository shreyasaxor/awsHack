"""awshack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from .views import save_file,dashboard,convert_voice,get_test_case
urlpatterns = [
    path('api/', view=save_file),
    path('dashboard/', view=dashboard),
    path('get-text/<str:filename>', view=convert_voice),
    # path('convert-utility/', view=convert_voice),
    path('get-test-case/', view=get_test_case),
]
