"""
URL configuration for JobPortal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from . import views


urlpatterns = [
    path('', views.landingPage, name='landingPage'),

    path('home', views.home, name='home'),
    path('post-job', views.create_post, name='post-job'),
    path('my-post', views.my_post, name='my-post'),

    path('update-post/<int:post_id>', views.update_post, name='update-post'),
    path('delete-post/<int:post_id>', views.delete_post, name='delete-post'),
    path('view-post/<int:post_id>', views.post_view, name='view-post'),

    path('view-saved-post', views.view_saved_post, name='view-saved-post'),
    path('applied-job', views.applied_job, name='applied-job'),
    path('apply/<int:post_id>', views.apply_job, name='apply-job'),

    path('find-job', views.find_job, name='find-job'),

    path('save_unsave_post/<int:post_id>', views.save_unsave_post, name='save_unsave_post'),

    path('profile/<str:username>', views.view_profile, name='view_profile'),

    path('get_location_suggestions', views.get_location_suggestions, name='get_location_suggestions'),

    path('recommendations', views.job_recommendations, name='recommendations'),

    path('mark_notification_as_read/<int:notification_id>', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('delete_notification/<int:notification_id>', views.delete_notification, name='delete_notification'),

]
