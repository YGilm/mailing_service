from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from mailing.forms import MailingForm, ClientForm, MailingMessageForm
from .models import MailingSettings, Client, MailingMessage, MailingLog
from .services import send_mailing


def home_view(request):
    all_mailings = MailingSettings.objects.all()
    active_mailings = MailingSettings.objects.filter(status='R')
    clients_list = Client.objects.all().distinct()

    context = {
        'object_list': all_mailings,
        'active_mailings': active_mailings,
        'clients_list': clients_list
    }
    return render(request, 'mailing/home_page.html', context)


class MailingListView(ListView):
    model = MailingSettings
    template_name = 'mailing/mailing_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_mailings'] = MailingSettings.objects.filter(status='R').count()
        return context


class MailingCreateView(CreateView):
    model = MailingSettings
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message_form'] = MailingMessageForm(self.request.POST or None)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        message_form = context['message_form']

        if message_form.is_valid():
            mailing = form.save()

            message = message_form.save(commit=False)
            message.mailing_settings = mailing
            message.save()

            if mailing.time <= timezone.now():
                send_mailing()

            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class MailingDetailView(DetailView):
    model = MailingSettings
    template_name = 'mailing/mailing_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing_logs = MailingLog.objects.filter(mailing_settings=self.object)
        context['clients'] = [log.client for log in mailing_logs]
        return context


class MailingDeleteView(DeleteView):
    model = MailingSettings
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')


class MailingUpdateView(UpdateView):
    model = MailingSettings
    form_class = MailingForm
    template_name = 'mailing/mailing_update.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        self.object = form.save()
        selected_recipients = form.cleaned_data.get('recipients')
        self.object.recipients.set(selected_recipients)

        # Логика на основе статуса
        if self.object.status == 'R':  # Если меняем статус на R (запущена) запускается рассылка.
            print("Рассылка запущена")
            send_mailing()
        elif self.object.status == 'C':  # Создана
            pass
        elif self.object.status == 'E':  # Закончена
            pass

        return super().form_valid(form)


class MailingMessageCreateView(CreateView):
    model = MailingMessage
    form_class = MailingMessageForm
    template_name = 'mailing/mailing_message_create.html'
    success_url = reverse_lazy('mailing:mailing_update')

    def form_valid(self, form):
        mailing = get_object_or_404(MailingSettings, pk=self.kwargs['pk'])
        message = form.save(commit=False)
        message.mailing_settings = mailing
        message.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing_id'] = self.kwargs.get('pk')
        return context


class MailingMessageUpdateView(UpdateView):
    model = MailingMessage
    form_class = MailingMessageForm
    template_name = 'mailing/mailing_message_update.html'

    def get_success_url(self):
        return reverse('mailing:mailing_update', args=[self.object.mailing_settings.pk])


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list')


class ClientListView(ListView):
    model = Client
    template_name = 'mailing/client_list'


class ClientDetailView(DetailView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_detail.html'
    success_url = reverse_lazy('mailing:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_update.html'

    def get_success_url(self):
        return reverse_lazy('mailing:client_detail', kwargs={'pk': self.object.pk})


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'mailing/client_confirm_delete.html'
    success_url = reverse_lazy('mailing:client_list')


def view_mailing_logs(request, pk):
    logs = MailingLog.objects.filter(mailing_settings_id=pk).order_by('-id')
    return render(request, 'mailing/mailing_logs.html', {'logs': logs})
