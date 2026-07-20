# Urdu translations

The language switcher (English/اردو) and RTL layout are already wired up (see
`config/settings/base.py` LANGUAGES/LOCALE_PATHS, and `templates/base/base.html`).
Templates use `{% trans "..." %}` tags for their user-facing strings.

To actually produce Urdu translations for those strings:

```bash
django-admin makemessages -l ur
# This creates locale/ur/LC_MESSAGES/django.po with every {% trans %} string found.
# Fill in each msgstr "" with its Urdu translation, then:
django-admin compilemessages
```

Until this is done, switching to Urdu will change the layout to RTL and use the
Noto Nastaliq Urdu font, but text will still display in English (Django falls
back to the original string when no translation is compiled yet). The
RAG-generated disease recommendations (recommendation/rag.py) are a separate
system — those already generate real Urdu text via the LLM regardless of this
file, since that's dynamic content, not template strings.
