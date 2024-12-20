from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import LogoutView

urlpatterns = [
    path('register_admin', views.register_admin, name='register_admin'),
    path('register_instructor/', views.register_instructor, name='register_instructor'),
    path('register_student/', views.register_student, name='register_student'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-only/', views.admin_only_view, name='admin_only'),
    path('instructor_list/', views.instructor_list, name='instructor_list'),
    path('instructors/edit/<int:instructor_id>/', views.edit_instructor, name='edit_instructor'),  # Edit instructor
    path('instructors/delete/<int:instructor_id>/', views.delete_instructor, name='delete_instructor'),  # Delete instructor
    # Course URLs
    path('course_list/', views.course_list, name="course_list"),
    path('add_course/', views.add_course, name='add_course'),
    path('courses/edit/<int:course_id>/', views.edit_course, name='edit_course'),  # Edit course
    path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),  # Delete course
    # Event URLs
    path('event_list/', views.event_list, name='event_list'),
    path('add_event/', views.add_event, name='add_event'),
    path('events/edit/<int:event_id>/', views.edit_event, name='edit_event'),  # Edit event
    path('events/delete/<int:event_id>/', views.delete_event, name='delete_event'),  # Delete event
    # Banner URLs
    path('banner_list/', views.banner_list, name='banner_list'),
    path('add_banner/', views.add_banner, name='add_banner'),
    path('banners/edit/<int:banner_id>/', views.edit_banner, name='edit_banner'),  # Edit event
    path('banners/delete/<int:banner_id>/', views.delete_banner, name='delete_banner'),  # Delete event

    path('payment_list/', views.payment_list, name='payment_list'),
]
# Add this line to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)