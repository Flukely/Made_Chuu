from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered

app_models = apps.get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass  # ถ้าลงทะเบียนแล้ว ให้ข้ามไป
