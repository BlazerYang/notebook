# django

## 如何重装uwsgi，不使用已编译的缓存
`pip install uwsgi -I --no-cache-dir`

## django-axes does not work properly with locmemcache as the default cache backend' ?
在 settings.py中增加如下配置
```python
CACHES = {
  'default': {
    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
  },
  'axes_cache': {
    'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
  }
}
AXES_CACHE = 'axes_cache'
```

## no module named middleware
As of 2.0.0, django-axes has default_app_config so you can just use axes in INSTALLED_APPS without installing middleware. Hence, delete the relevant MIDDLEWARE_CLASSES line in settings.py
[link](https://stackoverflow.com/questions/38786393/django-axes-installed-but-axes-middleware-module-not-available)