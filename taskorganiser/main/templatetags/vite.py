import json
from pathlib import Path

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


def _load_manifest():
    # manifest is written by Vite to static/frontend/.vite/manifest.json
    manifest_path = Path(settings.BASE_DIR) / 'taskorganiser' / 'static' / 'frontend' / '.vite' / 'manifest.json'
    if not manifest_path.exists():
        return {}
    try:
        return json.loads(manifest_path.read_text())
    except Exception:
        return {}


@register.simple_tag
def vite(entry):
    """Return HTML tags for the Vite-built entry (index.html).

    Usage: {% vite 'index.html' %}
    """
    manifest = _load_manifest()
    data = manifest.get(entry)
    if not data:
        return ''

    static_prefix = settings.STATIC_URL.rstrip('/') + '/frontend/'
    tags = []
    # css
    for css in data.get('css', []):
        href = static_prefix + css
        tags.append(f'<link rel="stylesheet" href="{href}">')

    # entry script
    file = data.get('file')
    if file:
        src = static_prefix + file
        tags.append(f'<script type="module" src="{src}"></script>')

    # any assets could be added if needed
    return mark_safe('\n'.join(tags))
