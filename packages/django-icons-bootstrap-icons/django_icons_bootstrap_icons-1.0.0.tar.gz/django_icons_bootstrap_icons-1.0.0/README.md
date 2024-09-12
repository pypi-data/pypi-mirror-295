# django-icons-bootstrap-icons

This project provides a renderer for [Bootstrap Icons](https://icons.getbootstrap.com) utilizing [django-icons](https://django-icons.readthedocs.io/en/latest/index.html).

## Installation

Just run:

```
pip install django-icons-bootstrap-icons
```

## To use

In your settings.py file:

```py

DJANGO_ICONS = {
  "DEFAULT": {
    "renderer": "django_icons_bootstrap_icons.BootstrapIconRenderer"
  }
}
```

Then just use the `{% icon %}` tag as normal!

## Extra features

This renderer includes a very neat feature over the default `IconRenderer`, which is support for custom attributes.

For instance, to add an aria-label to your icon, you can do the following:

`{% icon "person" aria_label="person icon" %}`

Note that while attributes in HTML are `-`, separated, this isn't possible in Django templates due to Python. Therefore, write the keys with `_` instead, and the renderer will autoconvert them for you.

This also works with attributes that do not have `-`es in them, such as `tabindex`.

Aside from this, `BootstrapIconRenderer` supports all features of the default renderer as it is just a superclass of `IconRenderer`.

## Contributing

I welcome all contributions! Just fork and then send a PR.

## License

This work is licensed under the MIT license.
