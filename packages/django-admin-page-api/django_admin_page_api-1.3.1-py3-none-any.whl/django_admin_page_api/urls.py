
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('signin', views.signin),
    path('signout', views.signout),
    path('info', views.info),
    path('logs', views.logs),
    path('csrf', views.csrf),
    path('<app_label>/<model_name>/', views.ModelView.as_view()),
    path('<app_label>/<model_name>/<field_name>/autocomplete/', views.autocomplete_new),
    path('<app_label>/<model_name>/items/', views.ItemsView.as_view()),
    path('<app_label>/<model_name>/<pk>/', views.ItemView.as_view()),
    path('<app_label>/<model_name>/<pk>/<field_name>/autocomplete/', views.autocomplete),
    path('<app_label>/<model_name>/action/<action_code>/', views.action),
]

