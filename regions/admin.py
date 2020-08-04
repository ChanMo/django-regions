from django.contrib.gis import admin
from .models import *

@admin.register(Region)
class RegionAdmin(admin.OSMGeoAdmin):
    list_display = ('fullname', 'number')
    list_filter = ('level',)
    list_per_page = 50
    search_fields = ('fullname', 'number')
    default_lon = 117
    default_lat = 36
    default_zoom = 4
    point_zoom = 11
    openlayers_url = 'https://cdn.bootcss.com/openlayers/2.13.1/OpenLayers.js'

    fields = ('parent', 'name', 'number', 'point', 'level')
    autocomplete_fields = ('parent',)
    exclude = ('fullname',)
