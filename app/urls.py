from django.urls import path
from . import views


urlpatterns = [

    path('user_login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('', views.Dashboard, name='index'),
    path('blog_writing/', views.blog_writing, name='blog_writing'),
    path('email_writing/', views.email_writing, name='email'),
    path('custom_content/', views.custom_writing, name='custom'),
    path('logout/', views.logout_view, name='logout'),
    path('saved_templates/', views.saved_templates, name='saved_templates'),
    path('saved_templates/<str:template_id>/', views.update_template, name='update_templates'),
    path('get_template_details/<str:template_id>/', views.get_template_details, name='get_template_details'),


    path('delete_template_blog/<str:template_id>/', views.delete_template_blog, name='delete_template_blog'),
    path('delete_template_email/<str:template_id>/', views.delete_template_email, name='delete_template_email'),
    path('delete_template_custom/<str:template_id>/', views.delete_template_custom, name='delete_template_custom'),



    path('email_templates/', views.email_templates, name='email_templates'),
    path('get_email_template_details/<str:template_id>/', views.get_email_template_details, name='get_email_template_details'),
    path('saved_email/', views.save_email, name='saved_email'),
    path('update_email/<str:email_id>/', views.update_email, name='update_email'),

    path('get_custom_content_details/<str:custom_content_id>/', views.get_custom_content_details, name='get_custom_content_details'),
    path('saved_custom_content/', views.saved_custom_content, name='saved_custom_content'),
    path('update_custom_content/<str:custom_content_id>/', views.update_custom_content, name='update_custom_email'),

]
