from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

import users

_PATIENT_GROUP = 'patient'
_COUNSELOR_GROUP = 'counselor'
_t_str = {'a': 'add', 'v': 'view', 'd': 'delete', 'c': 'change'}


class UserGroups:
    @property
    def patient_group(self):
        return Group.objects.get_or_create(name=_PATIENT_GROUP)[0]

    @property
    def counselor_group(self):
        return Group.objects.get_or_create(name=_COUNSELOR_GROUP)[0]


def add_iff_not_exists(group, permissions):
    for permission in permissions:
        if not group.permissions.filter(pk=permission.pk).exists():
            group.permissions.add(permission)
    group.save()


def get_permissions(content_type, permission_types):
    content_name = content_type.name
    return [
        Permission.objects.get_or_create(
            codename=f'{_t_str[t]}_{content_name}',
            name=f'Can {_t_str[t]} {content_name}',
            content_type=content_type)[0]
        for t in permission_types
    ]


def set_permission(**kwargs):
    article_type = ContentType.objects.get(app_label='board', model='article')
    comment_type = ContentType.objects.get(app_label='board', model='comment')
    communication_type = ContentType.objects.get(app_label='board', model='communication')
    counselorreview_type = ContentType.objects.get(app_label='board', model='counselorreview')

    patient_permissions = []
    patient_permissions.extend(get_permissions(article_type, 'avdc'))
    patient_permissions.extend(get_permissions(comment_type, 'avdc'))
    patient_permissions.extend(get_permissions(communication_type, 'avdc'))
    patient_permissions.extend(get_permissions(counselorreview_type, 'avdc'))
    counselor_permissions = []
    counselor_permissions.extend(get_permissions(article_type, 'v'))
    counselor_permissions.extend(get_permissions(comment_type, 'avdc'))
    counselor_permissions.extend(get_permissions(counselorreview_type, 'v'))

    add_iff_not_exists(UserGroups.patient_group, patient_permissions)
    add_iff_not_exists(UserGroups.counselor_group, counselor_permissions)

# yourapp.models 대신 실제 앱의 models 모듈 참조를 사용하세요
# post_migrate.connect(set_permission, sender=users.models)
