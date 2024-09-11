from adestis_netbox_plugin_account_management.models import *
from adestis_netbox_plugin_account_management.filtersets import *
from typing import Annotated, List, Union
import strawberry
import strawberry_django
from netbox.graphql.types import NetBoxObjectType

@strawberry_django.type(
    LoginCredentials,
    fields=['id', 'logon_name', 'login_credentials_status', 'contact', 'system', 'valid_from',
                  'valid_to'],
    filters=LoginCredentialsFilterSet
)
class LoginCredentialsType(NetBoxObjectType):
    @strawberry_django.field
    def systems(self) -> list[Annotated["System", strawberry.lazy('adestis_netbox_plugin_account_management.graphql.system')]]:
        return self.systems.all()

@strawberry.type
class LoginCredentialsQuery:
    @strawberry.field
    def login_credentials(self, id: int) -> LoginCredentialsType:
        return LoginCredentials.objects.get(pk=id)
    login_credentials_list: list[LoginCredentialsType] = strawberry_django.field()
