Django ACDH-CH functionality
============================

Provide some default functionality for ACDH-CH Django instances.

# Howto use

Install the app using your personal choice of Python package manager. Add the app to your Django's `settings.py`
```
INSTALLED_APPS += ["django_acdhch_functions"]
```

Call the `django_acdhch_functions` views from your `urls.py`:

```
urlpatterns += [path("", include("django_acdhch_functions.urls")),]
```

# Functionality

## Imprint

Provides an imprint route on `/imprint`. You have to set a `REDMINE_ID` in `settings`.

## Matomo

Provides a `{% matomo %}` templatetag. You have to `{% load django_adchch_functions %}` to use it. It requires the variables `matomo_url` and `matomo_id` to be set in the `PROJECT_METADATA` dict:
```
PROJECT_METADATA = {
    "matmom_url": "https://my.matomo.instance.tld",
    "matmo_id": 23,
}
```
