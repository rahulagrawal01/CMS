from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout_user/',views.logout_user,name='logout_user'),
    path('upload_article/',views.upload_article,name='upload_article'),
    path('my_article/',views.my_article,name='my_article'),
    path('all_article/',views.all_article,name='all_article'),
    path('delete_article/<int:id>/',views.delete_article,name='delete_article'),
    path('update_article/<int:id>/',views.update_article,name='update_article'),
    path('about_us/',views.about_us,name='about_us'),
    path('contact_us/',views.contact_us,name='contact_us'),
]