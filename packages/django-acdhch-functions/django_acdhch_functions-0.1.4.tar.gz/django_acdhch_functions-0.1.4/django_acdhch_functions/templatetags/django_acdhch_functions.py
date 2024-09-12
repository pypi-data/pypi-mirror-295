from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag("matomo.html")
def matomo():
    project_md = getattr(settings, "PROJECT_METADATA", {})
    matomo_url = project_md.get("matomo_url")
    matomo_id = project_md.get("matomo_id")
    return {
        "matomo_url": matomo_url,
        "matomo_id": matomo_id,
    }
