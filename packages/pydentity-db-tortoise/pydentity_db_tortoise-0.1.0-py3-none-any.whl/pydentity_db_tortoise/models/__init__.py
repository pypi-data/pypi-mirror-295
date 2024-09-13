from typing import Optional
from uuid import uuid4

from pydentity import DefaultPersonalDataProtector
from pydentity.abc import IPersonalDataProtector
from pydentity.utils import get_device_uuid
from tortoise import fields, indexes

from pydentity_db_tortoise.models.abstract import (
    Model,
    AbstractIdentityUser,
    AbstractIdentityRole,
    AbstractIdentityUserRole,
    AbstractIdentityUserClaim,
    AbstractIdentityUserLogin,
    AbstractIdentityUserToken,
    AbstractIdentityRoleClaim
)

__all__ = (
    'Model',
    'IdentityUser',
    'IdentityRole',
    'IdentityUserRole',
    'IdentityUserClaim',
    'IdentityUserLogin',
    'IdentityUserToken',
    'IdentityRoleClaim',
    'use_personal_data_protector',
)

from pydentity_db_tortoise.models.types import ProtectedPersonalDataField


def use_personal_data_protector(protector: Optional[IPersonalDataProtector] = None):
    if not protector:
        protector = DefaultPersonalDataProtector(get_device_uuid())
    ProtectedPersonalDataField.protector = protector


class UniqueIndex(indexes.Index):
    INDEX_TYPE = 'UNIQUE'


class IdentityUser(AbstractIdentityUser):
    id = fields.CharField(450, primary_key=True)
    roles: fields.ManyToManyRelation['IdentityRole'] = fields.ManyToManyField(
        'models.IdentityRole',
        related_name='users',
        through='pydentity_user_roles',
        forward_key='role_id',
        backward_key='user_id'
    )
    claims: fields.ReverseRelation['IdentityUserClaim']
    logins: fields.ReverseRelation['IdentityUserLogin']
    tokens: fields.ReverseRelation['IdentityUserToken']

    def __init__(
            self,
            email: str,
            username: str | None = None,
            **kwargs
    ):
        super().__init__(
            id=str(uuid4()),
            email=email,
            username=username,
            security_stamp=str(uuid4()),
            **kwargs
        )

    class Meta:
        table = 'pydentity_users'
        unique_together = (('normalized_email',), ('normalized_username',),)
        indexes = (
            UniqueIndex(fields=('normalized_email',), name='idx_pydentity_users_normalized_email'),
            UniqueIndex(fields=('normalized_username',), name='idx_pydentity_users_normalized_username'),
        )


class IdentityRole(AbstractIdentityRole):
    id = fields.CharField(450, primary_key=True)
    claims: fields.ReverseRelation['IdentityRoleClaim']
    users: fields.ReverseRelation['IdentityUser']

    def __init__(self, name: str, **kwargs):
        super().__init__(
            id=str(uuid4()),
            name=name,
            **kwargs
        )

    class Meta:
        table = 'pydentity_roles'
        unique_together = (('normalized_name',),)
        indexes = (
            UniqueIndex(fields=('normalized_name',), name='idx_pydentity_roles_normalized_name'),
        )


class IdentityUserRole(AbstractIdentityUserRole):
    user = fields.ForeignKeyField(
        'models.IdentityUser',
        to_field='id',
        on_delete=fields.CASCADE
    )
    role = fields.ForeignKeyField(
        'models.IdentityRole',
        to_field='id',
        on_delete=fields.CASCADE
    )

    class Meta:
        table = 'pydentity_user_roles'
        unique_together = (('user_id', 'role_id'),)


class IdentityUserClaim(AbstractIdentityUserClaim):
    user = fields.ForeignKeyField(
        'models.IdentityUser',
        to_field='id',
        on_delete=fields.CASCADE,
        related_name='claims'
    )

    class Meta:
        table = 'pydentity_user_claims'


class IdentityUserLogin(AbstractIdentityUserLogin):
    user = fields.ForeignKeyField(
        'models.IdentityUser',
        to_field='id',
        on_delete=fields.CASCADE,
        related_name='logins'
    )

    class Meta:
        table = 'pydentity_user_logins'
        unique_together = (('login_provider', 'provider_key'),)
        indexes = (
            UniqueIndex(fields=('login_provider', 'provider_key'), name='idx_pydentity_user_logins_lp_pk'),
        )


class IdentityUserToken(AbstractIdentityUserToken):
    user = fields.ForeignKeyField(
        'models.IdentityUser',
        to_field='id',
        on_delete=fields.CASCADE,
        related_name='tokens'
    )

    class Meta:
        table = 'pydentity_user_tokens'
        unique_together = (('user_id', 'login_provider', 'name'),)
        indexes = (
            UniqueIndex(fields=('user_id', 'login_provider', 'name'), name='idx_pydentity_user_tokens_user_lp_name'),
        )


class IdentityRoleClaim(AbstractIdentityRoleClaim):
    role = fields.ForeignKeyField(
        'models.IdentityRole',
        to_field='id',
        on_delete=fields.CASCADE,
        related_name='claims'
    )

    class Meta:
        table = 'pydentity_role_claims'
