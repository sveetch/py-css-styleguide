from django.views.generic import TemplateView

from .mixin import StyleguideMixin


class StyleguideViewMixin(StyleguideMixin, TemplateView):
    """
    Display styleguide from CSS manifest
    """
    template_name = "styleguide/index.html"
    manifest_css_filepath = None
    manifest_json_filepath = None
    save_dump = True # May be related to settings.DEBUG

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "styleguide": self.get_manifest(
                self.manifest_css_filepath,
                self.manifest_json_filepath,
            ),
        })

        return context
