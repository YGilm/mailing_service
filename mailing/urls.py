from django.urls import path
from mailing.views import *
from .apps import MailingConfig

app_name = MailingConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('mailings/<int:mailing_id>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/new/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/update/<int:mailing_id>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/delete/<int:mailing_id>/', MailingDeleteView.as_view(), name='mailing_delete'),
]
