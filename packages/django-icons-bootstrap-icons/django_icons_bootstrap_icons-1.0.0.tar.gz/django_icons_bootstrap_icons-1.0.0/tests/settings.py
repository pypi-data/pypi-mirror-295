SECRET_KEY = "django-icons-bootstrap-icons"

DEBUG = True

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

INSTALLED_APPS = (
    "django.contrib.contenttypes",
    # Our tests
    "django_icons",
    "tests",
)

ROOT_URLCONF = "tests.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

DJANGO_ICONS = {
    "DEFAULTS": {"renderer": "django_icons_bootstrap_icons.BootstrapIconRenderer"}
}
