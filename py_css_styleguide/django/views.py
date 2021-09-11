"""
View
****

"""
from django.views.generic import TemplateView

from .mixin import StyleguideMixin


class StyleguideViewMixin(StyleguideMixin, TemplateView):
    """
    Display styleguide from a manifest.

    Note than template from ``template_name`` is not shipped in this application. This
    is just a recommended template path you may use or not, it is at your
    responsability.
    """
    template_name = "styleguide/index.html"
    manifest_css_filepath = None
    manifest_json_filepath = None
    save_dump = True
    development_mode = True

    def get_context_data(self, **kwargs):
        """
        Include styleguide in template context.
        """
        context = super().get_context_data(**kwargs)

        context.update({
            "styleguide": self.get_manifest(
                self.manifest_css_filepath,
                json_filepath=self.manifest_json_filepath,
                save_dump=self.save_dump,
                development_mode=self.development_mode,
            ),
        })

        return context
