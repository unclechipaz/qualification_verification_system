"""CI-only synthetic persistence checks; execute through manage.py shell."""

import os
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model

from verification.models import VerificationLog

query = 'CI-PERSISTENCE-PROBE'
marker = Path(settings.MEDIA_ROOT) / 'ci-persistence.txt'
mode = os.environ['PERSISTENCE_PROBE_MODE']
if get_user_model().objects.exists():
    raise SystemExit('Disposable deployment unexpectedly contains pre-created users')
if mode == 'write':
    VerificationLog.objects.create(search_query=query, search_type='UNKNOWN', result_status='INVALID')
    marker.write_text('synthetic media persistence probe')
elif mode == 'check':
    if not VerificationLog.objects.filter(search_query=query).exists():
        raise SystemExit('Database record was lost when containers were recreated')
    if marker.read_text() != 'synthetic media persistence probe':
        raise SystemExit('Media volume was lost when containers were recreated')
else:
    raise SystemExit('Unknown persistence probe mode')
print(f'Persistence probe {mode}: passed; no seeded users')
