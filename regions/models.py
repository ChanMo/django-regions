import json
import urllib.request
import urllib.parse
import logging

from django.conf import settings
from django.contrib.gis.geos import Point
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class RegionManager(models.Manager):

    def _sync_item(self, data, parent=None):
        for row in data:
            res, created = self.update_or_create(
                name = row['name'],
                number = row['adcode'],
                level = row['level'],
                defaults = {
                    'point': Point(float(row['center'].split(',')[0]), float(row['center'].split(',')[1])),
                    'parent': parent,
                }
            )
            logger.debug(res.name)
            if 'districts' in row.keys() and len(row['districts']) > 0:
                self._sync_item(row['districts'], res)


    def sync(self):
        " 从高德接口同步数据 "
        params = {
            'key': settings.AMAP_KEY,
            'keywords': '100000',
            'subdistrict': 3,
            #'extensions': 'all'
        }
        url = 'https://restapi.amap.com/v3/config/district?{}'.format(urllib.parse.urlencode(params))
        logger.debug(url)
        try:
            res = urllib.request.urlopen(url)
            ress = json.loads(res.read().decode('utf8'))
        except Exception as e:
            logger.warning(e)
            return
        self._sync_item(ress['districts'][0]['districts'])


class Region(models.Model):
    name = models.CharField(_('name'), max_length=50)
    fullname = models.CharField(
        _('name'), max_length=200, blank=True, null=True)
    number = models.SlugField(_('number'))
    mpoly = models.MultiPolygonField(blank=True, null=True)
    point = models.PointField(blank=True, null=True)
    level = models.SlugField(blank=True, null=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        related_name='children')
    objects = RegionManager()


    def __str__(self):
        return self.fullname if self.fullname else self.name

    def save(self, *args, **kwargs):
        fullname = [self.name]
        fullname = self._make_fullname(self, fullname)
        fullname.reverse()
        self.fullname = ','.join(fullname)
        return super().save(*args, **kwargs)

    def _make_fullname(self, obj, fullname=[]):
        if obj.parent:
            fullname.append(obj.parent.name)
            self._make_fullname(obj.parent, fullname)
            return fullname
        else:
            return fullname


    class Meta:
        verbose_name = _('region')
        verbose_name_plural = _('region')
        ordering = ['number']
        indexes = [
            models.Index(fields=['fullname', 'number'])
        ]
