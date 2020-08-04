# Django Regions

基于`django`的中国省市区数据模块

数据由高德地图接口获取

## Quick Start

### Install

```
$ pip install django-regions
```

### Update `settings.py`

```
INSTALLED_APPS = [
    ...,
    'regions',
]

...
AMAP_KEY = ''
```

### Migrations

```
$ python manage.py makemigrations regions
$ python manage.py migrate
```

### Sync Data

```
$ python manage.py sync_regions
```
