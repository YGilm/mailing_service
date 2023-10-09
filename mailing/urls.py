from django.urls import path
from mailing.views import *
from .apps import MailingConfig

app_name = MailingConfig.name

urlpatterns = [
    # Home
    path('', home_view, name='home_page'),
    # MailingSettings
    path('mailings', MailingListView.as_view(), name='mailing_list'),
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_form'),
    path('mailings/update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    # Client
    path('clients/create/', ClientCreateView.as_view(), name='client_form'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/detail/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    # Logs
    path('logs/<int:pk>/', view_mailing_logs, name='mailing_logs'),
    # Message
    path('mailing/message/update/<int:pk>/', MailingMessageUpdateView.as_view(), name='mailing_message_update'),
    path('mailing/message/create/<int:pk>/', MailingMessageCreateView.as_view(), name='mailing_message_create'),
]
