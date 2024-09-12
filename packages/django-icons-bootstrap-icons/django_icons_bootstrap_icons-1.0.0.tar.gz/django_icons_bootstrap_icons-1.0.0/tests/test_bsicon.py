import unittest

from django.template import Context, Template

# This function is taken from django-icons tests, in the test_template_tags.py file.
def render_template(content, **context_args):
    """Create a template with content ``content``."""
    template = Template("{% load icons %}" + content)
    return template.render(Context(context_args))

def render_icon(icon:str, extra_content:str = ""):
    return render_template(f'{{% icon "{icon}" {extra_content} %}}')

class TestBootstrapIcons(unittest.TestCase):

    # Ensure using no extra attributes gives us plain output.
    def test_plain(self):
        self.assertEqual(
            render_icon("person"),
            '<i class="bi bi-person"></i>'
        )

    # Ensure tabindex works properly.
    def test_with_tabindex(self):
        self.assertEqual(
            render_icon("person", 'tabindex="-1"'),
            '<i class="bi bi-person" tabindex="-1"></i>'
        )

    # Ensure aria_* attributes are properly rendered to aria-* attributes.
    def test_with_aria(self):
        self.assertEqual(
            render_icon("person", 'aria_label="person icon"'),
            '<i aria-label="person icon" class="bi bi-person"></i>'
        )

    # Ensure renderer is not passed through
    def test_with_renderer(self):
        self.assertEqual(
            render_icon('person', 'renderer="django_icons_bootstrap_icons.BootstrapIconRenderer"'),
            '<i class="bi bi-person"></i>'
        )

    # Ensure tag is not passed through and tag is properly updated.
    def test_with_tag(self):
        self.assertEqual(
            render_icon('person', 'tag="p"'),
            '<p class="bi bi-person"></p>'
        )

    # ensure data-* attributes are rendered correctly.
    # Because of python limitations, we have to write them as data_* and then replace _ with - when rendering.
    def test_with_data(self):
        self.assertEqual(
            render_icon("person", 'data_label="label"'),
            '<i class="bi bi-person" data-label="label"></i>'
        )
