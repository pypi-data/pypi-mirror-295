from adestis_netbox_plugin_account_management.models import LoginCredentials, System
from adestis_netbox_plugin_account_management.models.ssh_key import SshKey
from netbox.filtersets import NetBoxModelFilterSet
from django.db.models import Q
from django import forms
import django_filters
from django.utils.translation import gettext as _
from utilities.forms.fields import DynamicModelMultipleChoiceField, DynamicModelMultipleChoiceField
from utilities.forms.widgets import DatePicker
from tenancy.models import Contact

__all__ = (
    'SshKeyFilterSet',
)

class SshKeyFilterSet(NetBoxModelFilterSet):

    contact_id = DynamicModelMultipleChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        null_option='None',
        label=_('Group')
    )

    contact = DynamicModelMultipleChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        null_option='None',
        label=_('Group')
    )

    valid_from = forms.DateField(
        required=False,
        widget=DatePicker
    )

    valid_to = forms.DateField(
        required=False,
        widget=DatePicker
    )

    class Meta:
        model = SshKey
        fields = ['id',
                  'raw_ssh_key',
                  'key_comment',
                  'encoded_key',
                  'key_type',
                  'ssh_key_status',
                  'contact',
                  'valid_from',
                  'valid_to']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(identifier__icontains=value) |
            Q(contact__name__icontains=value) |
            Q(ssh_key_status__icontains=value)
        )
