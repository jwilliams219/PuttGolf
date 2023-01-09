from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('tournament/<str:tournamentName>/', views.tournamentInfo, name='tournamentInfo'),
    path('tournament/<str:tournamentName>/edit', views.tournamentEdit, name='tournamentEdit'),
    path('tournament/<str:tournamentName>/play', views.tournament, name='tournament'),
    path('error/', views.error, name='error'),
    path('createAccount/', views.accountCreation, name='accountCreation'),
    path('drinks/', views.drinks, name='drinks'),
    path('home/', views.homeRedirect, name='homeRedirect'),
    path('index/', views.homeRedirect, name='homeRedirect'),
    path('bank/', views.bank, name='bank'),
    path('editDrinks/', views.drinksEdit, name='editDrinks'),
    path('orderConfirmation/', views.orderConfirmation, name='orderConfirmation'),
    path('account/', views.account, name='account'),
    path('drinkMeister', views.drinkMeister, name='drinkMeister'),
    path('events', views.events, name='events'),
    path('manager', views.manager, name='manager'),
    path('verification', views.verification, name='verification'),
    path('createAccount', views.createAccount, name='createAccount'),
    path('addHoles', views.addHoles, name='addHoles'),

    # Django Auth
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="logout.html"), name='logout'),
]
