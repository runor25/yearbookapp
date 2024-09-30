from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.main_view,name='main'),
    path('reg/', views.register_view,name='reg'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view,name='home'),
    path('year/<int:year>/', views.year_view, name='year'),
    path('profile/',views.profile_view,name='profile'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)