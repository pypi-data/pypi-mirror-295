from adestis_netbox_plugin_account_management.models import *
from adestis_netbox_plugin_account_management.filtersets import *
from typing import Annotated, List, Union
import strawberry
import strawberry_django
from netbox.graphql.types import NetBoxObjectType

@strawberry_django.type(
    SshKey,
    fields=['id'],
    filters=SshKeyFilterSet
)
class SshKeyType(NetBoxObjectType):
    @strawberry_django.field
    def contact(self) -> list[Annotated["Contaxt", strawberry.lazy('tenancy.models.Contact')]]:
        return self.contact

@strawberry.type
class SshKeyQuery:
    @strawberry.field
    def ssh_key(self, id: int) -> SshKeyType:
        return SshKey.objects.get(pk=id)
    ssh_key_list: list[SshKeyType] = strawberry_django.field()
