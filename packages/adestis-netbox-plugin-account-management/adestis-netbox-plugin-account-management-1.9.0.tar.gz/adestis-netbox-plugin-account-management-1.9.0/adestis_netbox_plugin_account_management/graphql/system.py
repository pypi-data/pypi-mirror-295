from adestis_netbox_plugin_account_management.models import *
from adestis_netbox_plugin_account_management.filtersets import *
from typing import Annotated
import strawberry
import strawberry_django
from netbox.graphql.types import NetBoxObjectType

@strawberry_django.type(
    System,
    fields=('id', 'tenant', 'group', 'cluster_group_id', 'cluster_id', 'device', 'virtual_machine_id', 'name', 'system_url', 'system_status'),
    filters=SystemFilterSet
)
class SystemType(NetBoxObjectType):
    @strawberry_django.field
    def logincredentials(self) -> list[Annotated["LoginCredentials", strawberry.lazy('adestis_netbox_plugin_account_management.graphql.login_credentials')]]:
        return self.logincredentials.all()

@strawberry.type
class SystemsQuery:
    @strawberry.field
    def system(self, id: int) -> SystemType:
        return System.objects.get(pk=id)
    system_list: list[SystemType] = strawberry_django.field()