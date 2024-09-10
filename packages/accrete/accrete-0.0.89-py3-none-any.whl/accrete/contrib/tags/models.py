from django.db import models
from django.utils.translation import gettext_lazy as _
from accrete.models import TenantModel
from accrete.managers import TenantManager
from accrete.tenant import get_tenant


class TagManager(TenantManager):

    def get_queryset(self):
        queryset = super().get_queryset()
        if group := not getattr(self.model, 'tag_group', None):
            print(group)
        if group := getattr(self.model, 'tag_group', False) and get_tenant():
            return queryset.filter(tag_group=group)
        return queryset


class Tag(TenantModel):

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        db_table = 'accrete_tag'
        default_related_name = 'tags'
        constraints= [
            models.UniqueConstraint(
                fields=['tenant', 'name'], name='unique_tag_name_per_tenant'
            ),
            models.UniqueConstraint(
                fields=['tenant', 'tag_group'], name='unique_tag_group_per_tenant'
            )
        ]

    objects = TagManager()

    name = models.CharField(
        verbose_name=_('Name'),
        max_length=50
    )

    color = models.CharField(
        verbose_name=_('Color'),
        max_length=7
    )

    tag_group = models.CharField(
        verbose_name=_('Group'),
        max_length=255
    )
