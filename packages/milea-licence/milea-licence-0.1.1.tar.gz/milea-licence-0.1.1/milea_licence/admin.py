import json

import requests
from django.conf import settings
from django.contrib import admin

from milea_base.utils import get_setting

from .models import MileaAppInfo


@admin.register(MileaAppInfo)
class MileaAppInfoAdmin(admin.ModelAdmin):

    list_display = ('app_name', 'installed_version', 'appconfig_version', 'pypi_version', 'is_current')

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):

        self.list_display_links = None

        # Get all installed miela apps
        MileaAppInfo.objects.all().delete()
        for app in settings.INSTALLED_APPS:
            if app.startswith('milea_'):

                # Installed Version
                current_version = get_setting(f"{app}.VERSION")

                # App Config last version
                try:
                    f = open(f"{settings.BASE_DIR}/{app}/app.json")
                    json_data = json.load(f)
                    app_config_version = json_data['changelog'][-1]['version']
                except Exception:
                    app_config_version = None
                else:
                    f.close()

                # PyPi Version
                try:
                    response = requests.get(f"https://pypi.org/pypi/{app}/json")
                    data = response.json()
                    pypi_version = data["info"]["version"]
                except Exception:
                    pypi_version = None

                MileaAppInfo.objects.create(
                    app_name=app,
                    installed_version=current_version,
                    appconfig_version=app_config_version,
                    pypi_version=pypi_version,
                )

        return super().changelist_view(request, extra_context=extra_context)
