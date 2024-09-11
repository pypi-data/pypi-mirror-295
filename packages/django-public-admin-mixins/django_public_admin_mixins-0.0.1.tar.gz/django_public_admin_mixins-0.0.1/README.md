# django-public-admin-mixins

**WARNING**: *Using this app may introduce security issues. We don't
recommend using it in production. Use at you own risk.*

This app helps developers create public interfaces using the django
admin. That is, an interface where no login is required, and all users
only have view permission on models.

There is another app,
[`django-public-admin`](https://github.com/cuducos/django-public-admin),
which implements a similar funcionality, but uses child classes instead
of mixins. For small admin projects it should be quicker to setup, but
these mixins allow for more configurability.

## Installation

1. `$ pip install django-public-admin-mixins`
2. Add `public_admin` to you `INSTALLED_APPS`, before `django.contrib.admin`

## Usage

To make the admin interface public, one must configure both the admin
site and the `ModelAdmin` classes that are registered to that site. For
that, `django-public-admin-mixins` exposes two mixins:
`PublicAdminSiteMixin` and `PulbicModelAdminMixin`. To use the former,
one must use a custom admin site. More details can be found
[here](https://docs.djangoproject.com/en/dev/ref/contrib/admin/#overriding-the-default-admin-site),
but the basic idea for overriding the default admin site is as follows:

```python
# myproject/admin.py

from django.contrib import admin

from django_public_admin.admin import PublicAdminSiteMixin


class PublicAdminSite(PublicAdminSiteMixin, admin.AdminSite):
    pass
```

```python
# myproject/apps.py

from django.contrib.admin.apps import AdminConfig


class PublicAdminConfig(AdminConfig):
    default_site = "myproject.admin.PublicAdminSite"
```

```python
# myproject/settings.py

INSTALLED_APPS = [
    # ...
    "myproject.apps.PublicAdminConfig",  # replaces 'django.contrib.admin'
    # ...
]
```

When registering a model to this admin site, use a custom model admin
which uses our mixin:

```python
# myapp/admin.py

from django.contrib import admin

from django_public_admin.admin import PublicModelAdminMixin

from .models import MyModel

class PublicModelAdmin(PublicModelAdminMixin, admin.ModelAdmin):
    pass

admin.site.register(MyModel, PublicModelAdmin)
```

## Templates

This app ships with templates to override links in the head of the site
that aren't suited to a public admin, like the ones for login and
logout. If you decide to use your own, there is no need to add the app
to the `INSTALLED_APPS` list.
