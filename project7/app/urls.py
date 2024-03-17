from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('404/',views.page404,name='404page'),
    path('about/',views.about,name='about'),
    path('author/<int:id>/',views.author,name='author'),
    path('contact/',views.contact,name='contact'),
    path('post-list/<int:id>/',views.post_list,name='post-list'),
    path('cat-post-list/<int:id>/',views.sub_post_list,name='sub-post-list'),
    path('post-details/<int:id>',views.post_details,name='post-details'),
    path('privacy-policy/',views.privacy,name='privacy'),
    path('search/',views.search,name='search'),
    path('maintenance/',views.maintenance,name='maintenance'),
    path('registration/', views.register_user, name='registration'),
    path('user-login/', views.author_login, name='login'),
    path('user-logout/', views.user_logout, name='logout'),
    path('create-post/', views.create_post, name='create-post'),

]
