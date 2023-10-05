from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from mailing.forms import MailingForm
from .models import MailingSettings, Client, MailingMessage, MailingLog
from .services import send_mailing


class MailingListView(ListView):
    model = MailingSettings
    template_name = 'mailing_list.html'

    def get_queryset(self):
        return MailingSettings.objects.all()


class MailingCreateView(CreateView):
    model = MailingSettings
    form_class = MailingForm
    template_name = 'mailing_form.html'
    success_url = reverse_lazy('mailing_list')

    def form_valid(self, form):
        mailing = form.save()
        if mailing.time <= timezone.now():
            send_mailing()

        return super().form_valid(form)


class MailingDetailView(DetailView):
    model = MailingSettings
    template_name = 'mailing_detail.html'


class MailingDeleteView(DeleteView):
    model = MailingSettings
    template_name = 'mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_list')


class MailingUpdateView(UpdateView):
    model = MailingSettings
    form_class = MailingForm
    template_name = 'mailing_form.html'
    success_url = reverse_lazy('mailing_list')
