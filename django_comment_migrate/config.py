from django.conf import settings


class DCMConfig:
    defaults = {"DCM_COMMENT_KEY": "help_text", "DCM_TABLE_COMMENT_KEY": "verbose_name"}

    def __getattr__(self, name):
        if name in self.defaults:
            return getattr(settings, name, self.defaults[name])


dcm_config = DCMConfig()
