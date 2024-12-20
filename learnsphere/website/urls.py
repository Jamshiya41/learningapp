from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.base, name="base"),
    path('', views.home, name="home"),
    path('courses', views.courses, name="courses"),
    path('course_details/<int:course_id>/', views.course_details, name='course_details'),
    path('trainers', views.trainers, name="trainers"),
    path('events', views.events, name="events"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('checkout/<int:plan_id>/', views.checkout_session, name='checkout'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_cancel/', views.payment_cancel, name='payment_cancel'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)