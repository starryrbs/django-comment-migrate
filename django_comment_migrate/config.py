from django.conf import settings


COMMENT_KEY = getattr(settings, "DCM_COMMENT_KEY", "help_text")
