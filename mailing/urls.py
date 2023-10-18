from django.urls import path
from django.views.decorators.cache import cache_page, never_cache

from mailing.views import *
from .apps import MailingConfig

app_name = MailingConfig.name

urlpatterns = [
    # Home
    path('', home_view, name='home_page'),
    # MailingSettings
    path('mailings', MailingListView.as_view(), name='mailing_list'),
    path('mailings/<int:pk>/', cache_page(60)(MailingDetailView.as_view()), name='mailing_detail'),
    path('mailings/create/', never_cache(MailingCreateView.as_view()), name='mailing_form'),
    path('mailings/update/<int:pk>/', never_cache(MailingUpdateView.as_view()), name='mailing_update'),
    path('mailings/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    # Manager status Ended
    path('end_mailing/<int:pk>/', EndMailingView.as_view(), name='end_mailing'),
    # Client
    path('clients/create/', never_cache(ClientCreateView.as_view()), name='client_form'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/update/<int:pk>/', never_cache(ClientUpdateView.as_view()), name='client_update'),
    path('clients/detail/<int:pk>/', cache_page(60)(ClientDetailView.as_view()), name='client_detail'),
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    # Logs
    path('logs/<int:pk>/', view_mailing_logs, name='mailing_logs'),
    # Message
    path('mailing/message/update/<int:pk>/', never_cache(MailingMessageUpdateView.as_view()), name='mailing_message_update'),
    path('mailing/message/create/<int:pk>/', never_cache(MailingMessageCreateView.as_view()), name='mailing_message_create'),
]
