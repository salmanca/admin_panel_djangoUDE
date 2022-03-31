from django.urls import path
from . import views
urlpatterns = [
    path('',views.homepage, name='home'),
    path('view', views.view_user, name="view"),
    path('login-page', views.loginpage, name = 'login_page'),
    path('edit-page/<user_id>', views.editUser, name='edit'),
    path('create-page', views.createUser, name='create'),
    path('delet-user/<user_id>', views.deletUser, name="delet"),
    path('logout', views.logout_user, name="logout"),
    path('search', views.search_user, name="search"),
    ]