from django.views.generic import TemplateView
from .models import Page


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = Page.objects.get(title='Home')

        context['title'] = page.title
        context['content'] = page.content
        return context


class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = Page.objects.get(title='About')

        context['title'] = page.title
        context['content'] = page.content
        context['text_on_page'] = page.text_on_page
        return context
