from django_icons.renderers.icon import IconRenderer

class BootstrapIconRenderer(IconRenderer):
    """Render a Bootstrap Icons icon."""

    def get_class(self):  # noqa
        return f"bi bi-{self.name}"

    def get_attrs(self):  # noqa
        attrs = super().get_attrs()

        for key,value in self.kwargs.items():
            if key == "renderer":
                continue
            elif key == "tag":
                continue

            key = key.replace("_", "-")
            attrs[f"{key}"] = value

        return attrs
