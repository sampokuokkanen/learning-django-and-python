from django.views.generic.base import TemplateView


class DeleteListView(TemplateView):
    template_name = 'delete_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = 0
        return context
