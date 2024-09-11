from netbox.plugins import PluginMenuItem, PluginMenuButton, PluginMenu
from netbox.choices import ButtonColorChoices
from django.conf import settings

_menu_items = [
    PluginMenuItem(
        link='plugins:adestis_netbox_plugin_account_management:logincredentials_list',
        link_text='Login Credentials',
        permissions=["adestis_netbox_plugin_account_management.logincredentials_list"],
        buttons=(
            PluginMenuButton('plugins:adestis_netbox_plugin_account_management:logincredentials_add', 'Add', 'mdi mdi-plus-thick', ButtonColorChoices.GREEN, ["adestis_netbox_plugin_account_management.logincredentials_add"]),
        )
    ),    
        PluginMenuItem(
        link='plugins:adestis_netbox_plugin_account_management:system_list',
        link_text='Systems',
        permissions=["adestis_netbox_plugin_account_management.system_list"],
        buttons=(
            PluginMenuButton('plugins:adestis_netbox_plugin_account_management:system_add', 'Add', 'mdi mdi-plus-thick', ButtonColorChoices.GREEN, ["adestis_netbox_plugin_account_management.system_add"]),
        )
    ),
    PluginMenuItem(
        link='plugins:adestis_netbox_plugin_account_management:sshkey_list',
        link_text='SSH Keys',
        permissions=["adestis_netbox_plugin_account_management.sshkey_list"],
        buttons=(
            PluginMenuButton('plugins:adestis_netbox_plugin_account_management:sshkey_add', 'Add', 'mdi mdi-plus-thick', ButtonColorChoices.GREEN, ["adestis_netbox_plugin_account_management.sshkey_add"]),
        )
    )
]

plugin_settings = settings.PLUGINS_CONFIG.get('adestis_netbox_plugin_account_management', {})

if plugin_settings.get('top_level_menu'):
    menu = PluginMenu(  
        label="Account Management",
        groups=(("Login Credentials", _menu_items),),
        icon_class="mdi mdi-key",
    )
else:
    menu_items = _menu_items