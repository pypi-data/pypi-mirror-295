from netbox.views import generic
from adestis_netbox_plugin_account_management.forms import *
from adestis_netbox_plugin_account_management.models import *
from adestis_netbox_plugin_account_management.filtersets import *
from adestis_netbox_plugin_account_management.tables import *
from tenancy.models import Contact
from netbox.views import generic
from utilities.views import ViewTab, register_model_view
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.db import transaction
from django.db.models import Q

__all__ = (
    'LoginCredentialsView',
    'LoginCredentialsListView',
    'LoginCredentialsEditView',
    'LoginCredentialsDeleteView',
    'ContactLoginCredentials',
    'LoginCredentialsBulkDeleteView',
    'LoginCredentialsBulkEditView',
    'LoginCredentialsBulkImportView',
    'LoginCredentialsAssignSshKey',
    'LoginCredentialsSshKeysView'
)

class LoginCredentialsView(generic.ObjectView):
    queryset = LoginCredentials.objects.all()


class LoginCredentialsListView(generic.ObjectListView):
    queryset = LoginCredentials.objects.all()
    table = LoginCredentialsTable
    filterset = LoginCredentialsFilterSet
    filterset_form = LoginCredentialsFilterForm

class LoginCredentialsEditView(generic.ObjectEditView):
    queryset = LoginCredentials.objects.all()
    form = LoginCredentialsForm


class LoginCredentialsDeleteView(generic.ObjectDeleteView):
    queryset = LoginCredentials.objects.all()


@register_model_view(Contact, name='contactlogincredentials', path='login-credentials')
class ContactLoginCredentials(generic.ObjectView):

    queryset = Contact.objects.all()
    template_name = "adestis_netbox_plugin_account_management/contacts/contact_login_credentials.html"
    
    tab = ViewTab(
        label='Login Credentials',
        badge=None,
        hide_if_empty=False
    )

    def get_extra_context(self, request, instance):
        query = Q(contact=instance) | Q(ssh_keys__contact=instance)
        assets = LoginCredentials.objects.filter(query)
        table = LoginCredentialsTable(assets)
        data = {
            "table": table,
        }
        return data

class LoginCredentialsBulkDeleteView(generic.BulkDeleteView):
    queryset = LoginCredentials.objects.all()
    table = LoginCredentialsTable
    
    
class LoginCredentialsBulkEditView(generic.BulkEditView):
    queryset = LoginCredentials.objects.all()
    filterset = LoginCredentialsFilterSet
    table = LoginCredentialsTable
    form =  LoginCredentialsBulkEditForm
    

class LoginCredentialsBulkImportView(generic.BulkImportView):
    queryset = LoginCredentials.objects.all()
    model_form = LoginCredentialsCSVForm
    table = LoginCredentialsTable
    


@register_model_view(LoginCredentials, 'assign_ssh_key')
class LoginCredentialsAssignSshKey(generic.ObjectEditView):
    queryset = LoginCredentials.objects.prefetch_related(
        'ssh_keys', 'tags'
    ).all()

    form = LoginCredentialsAssignSshKeyForm
    template_name = 'adestis_netbox_plugin_account_management/login_credentials/assign_ssh_key.html'

    def get(self, request, pk):
        loginCredentials = get_object_or_404(self.queryset, pk=pk)
        form = self.form(loginCredentials ,initial=request.GET)

        return render(request, self.template_name, {
            'loginCredentials': loginCredentials,
            'form': form,
            'return_url': reverse('plugins:adestis_netbox_plugin_account_management:logincredentials', kwargs={'pk': pk}),
            'edit_url': reverse('plugins:adestis_netbox_plugin_account_management:logincredentials_assign_ssh_key', kwargs={'pk': pk}),
         })

    def post(self, request, pk):
        loginCredentials = get_object_or_404(self.queryset, pk=pk)
        form = self.form(loginCredentials, request.POST)

        if form.is_valid():

            device_pks = form.cleaned_data['sshkeys']
            with transaction.atomic():

                # Assign the selected Devices to the Cluster
                for sshKey in SshKey.objects.filter(pk__in=device_pks):
                    loginCredentials.ssh_keys.add(sshKey)

            loginCredentials.save()

            return redirect(loginCredentials.get_absolute_url())
        

        return render(request, self.template_name, {
            'loginCredentials': loginCredentials,
            'form': form,
            'return_url': loginCredentials.get_absolute_url(),
            'edit_url': reverse('plugins:adestis_netbox_plugin_account_management:logincredentials_assign_ssh_key', kwargs={'pk': pk}),
        })    
    
@register_model_view(SshKey, 'new_login_credential')
class LoginCredentialWithSelectedSshKeyEdit(generic.ObjectEditView):
    queryset = SshKey.objects.prefetch_related(
        'tags',
        'contact'
    ).all()

    form = LoginCredentialWithSelectedSshKeyForm
    template_name = 'adestis_netbox_plugin_account_management/ssh_keys/new_login_credential.html'

    def get(self, request, pk):
        sshKey = get_object_or_404(self.queryset, pk=pk)
        form = self.form(sshKey ,initial=request.GET)

        return render(request, self.template_name, {
            'sshkey': sshKey,
            'form': form,
            'return_url': reverse('plugins:adestis_netbox_plugin_account_management:sshkey', kwargs={'pk': pk}),
            'edit_url': reverse('plugins:adestis_netbox_plugin_account_management:sshkey_new_login_credential', kwargs={'pk': pk}),
         })

    def post(self, request, pk):
        sshkey = get_object_or_404(self.queryset, pk=pk)
        form = self.form(sshkey, request.POST)

        # save a new login credential
        if form.is_valid() and sshkey:

            # add a login credential
            loginCredentials = LoginCredentials()
            loginCredentials.logon_name = form.cleaned_data['logon_name']
            loginCredentials.contact = form.cleaned_data['contact']
            loginCredentials.system = form.cleaned_data['system']
            loginCredentials.login_credentials_status = form.cleaned_data['login_credentials_status']
            loginCredentials.valid_from = form.cleaned_data['valid_from']
            loginCredentials.valid_to = form.cleaned_data['valid_to']
            loginCredentials.tags = form.cleaned_data['tags']
            loginCredentials.save()
            
            # try to assign the login credenial
            loginCredentials.ssh_keys.add(sshkey)
            loginCredentials.save()            

            return redirect(loginCredentials.get_absolute_url())        

        return render(request, self.template_name, {
            'sshkey': sshkey,
            'form': form,
            'return_url': sshkey.get_absolute_url(),
            'edit_url': reverse('plugins:adestis_netbox_plugin_account_management:sshkey_new_login_credential', kwargs={'pk': pk}),
        })       
    

@register_model_view(LoginCredentials, 'ssh_keys')
class LoginCredentialsSshKeysView(generic.ObjectChildrenView):
    queryset = LoginCredentials.objects.all()
    child_model = LoginCredentials
    table = LoginCredentialsSshKeysTable
    filterset = SshKeyFilterSet
    filterset_form = SshKeyFilterForm
    template_name = 'adestis_netbox_plugin_account_management/login_credentials/ssh_keys.html'
    tab = ViewTab(
        label='SSH Keys',
        badge=None,
        hide_if_empty=False
    )

    def get_children(self, request, parent):
        return parent.ssh_keys.all()
    
