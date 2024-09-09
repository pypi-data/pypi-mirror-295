from django.db import models


class MileaAppInfo(models.Model):

    app_name = models.CharField(max_length=50)
    installed_version = models.CharField(max_length=50, null=True)
    appconfig_version = models.CharField(max_length=50, null=True)
    pypi_version = models.CharField(max_length=50, null=True)

    @property
    def is_current(self):
        if self.installed_version == self.appconfig_version and self.installed_version == self.pypi_version:
            return True
        else:
            return False

    class Meta:
        verbose_name = "App"
