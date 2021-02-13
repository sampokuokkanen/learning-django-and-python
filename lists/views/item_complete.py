from django.views.generic.base import TemplateView


class ItemCompleteView(TemplateView):
    template_name = 'item_complete.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = 0
        return context
