from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
from tenancy.models import *

__all__ = (
    'SshKeyStatusChoices',
    'SshKey',
    'SshKeyTypeChoices'
)

class SshKeyStatusChoices(ChoiceSet):
    key = 'SshKey.status'
    STATUS_ACTIVE = 'active'
    STATUS_DRAFT = 'draft'
    STATUS_DEPRECATED = 'deprecated'

    CHOICES = [
        (STATUS_ACTIVE, 'Active', 'green'),
        (STATUS_DRAFT, 'Draft', 'cyan'),
        (STATUS_DEPRECATED, 'Deprecated', 'gray'),
    ]


class SshKeyTypeChoices(ChoiceSet):
    key = 'SshKey.keyType'

    TYPE_RSA = 'ssh-rsa'
    TYPE_DSS = 'ssh-dss'
    TYPE_ED25519 = 'ssh-ed25519'
    TYPE_ECDSA256 = 'ecdsa-sha2-nistp256'
    TYPE_ECDSA384 = 'ecdsa-sha2-nistp384'
    TYPE_ECDSA521 = 'ecdsa-sha2-nistp521'

    CHOICES = [
        (TYPE_RSA, 'RSA', 'cyan'),
        (TYPE_DSS, 'DSS', 'cyan'),
        (TYPE_ED25519, 'ED25519', 'cyan'),
        (TYPE_ECDSA256, 'ECDSA-SHA2-NISTP256', 'cyan'),
        (TYPE_ECDSA384, 'ECDSA-SHA2-NISTP384', 'cyan'),
        (TYPE_ECDSA521, 'ECDSA-SHA2-NISTP521', 'cyan'),
    ]


class SshKey(NetBoxModel):

    raw_ssh_key = models.CharField(
        max_length=800,
        verbose_name='SSH Key',
        help_text='SSH Key'
    )

    key_comment = models.CharField(
        max_length=256,
        verbose_name='Key Comment',
        help_text='Key comment of the SSH Key',
        blank=True,
        null=True
    )

    encoded_key = models.CharField(
        max_length=800,
        verbose_name='Encoded Key',
        help_text='Encoded Key',
        blank=True,
        null=True
    )

    key_type = models.CharField(
        max_length=50,
        choices=SshKeyTypeChoices,
        verbose_name='SSH Key Type',
        help_text='SSH Key Type of the Key',
        blank=True,
        null=True
    )

    ssh_key_status = models.CharField(
        max_length=50,
        choices=SshKeyStatusChoices,
        verbose_name='Status',
        help_text='Status of the entry'
    )

    valid_from = models.DateField(
        null=True,
        blank=True,
        verbose_name='Valid from',
        help_text='Start of validity'
    )

    valid_to = models.DateField(
        null=True,
        blank=True,
        verbose_name='Valid to',
        help_text='End of validity'
    )

    contact = models.ForeignKey(
        to='tenancy.Contact',
        on_delete=models.PROTECT,
        related_name='SshKey_contact',
        null=True,
        verbose_name='Contact',
        help_text='Contact that uses the System'
    )

    comments = models.TextField(
        blank=True
    )

    class Meta:
        verbose_name_plural = "SSH Keys"
        verbose_name = 'SSH Key'
        ordering = ('contact',)
        constraints = [
            models.UniqueConstraint(
                fields=['key_type', 'encoded_key'],
                name='%(app_label)s_%(class)s_unique_ssh_key'
            )
        ]

    def __str__(self):
        if self.key_comment:
            return self.key_comment
        else:
            return ""

    def get_absolute_url(self):
        return reverse('plugins:adestis_netbox_plugin_account_management:sshkey', args=[self.pk])

    def get_ssh_key_status_color(self):
        return SshKeyStatusChoices.colors.get(self.ssh_key_status)

    def get_key_type_color(self):
        return SshKeyTypeChoices.colors.get(self.key_type)
