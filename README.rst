=====
gitlean
=====

gitlean is a simple Django app to get and store data from Gitlab.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "gitlean" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'gitlean',
    ]

2. Include the gitlean URLconf in your project urls.py like this::

    url(r'^gitlean/', include('gitlean.urls')),