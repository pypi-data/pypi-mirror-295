from django.urls import path

from . import views

app_name = "django_acdhch_functions"

urlpatterns = [path("imprint", views.Imprint.as_view(), name="imprint")]
