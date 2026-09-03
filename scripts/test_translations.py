import os
import sys
import django

# Set UTF-8 encoding for standard output
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.utils.translation import activate, gettext as _

activate('ur')
test_keys = [
    'Dashboard',
    'Total Scans',
    'Healthy Plants',
    'Diseases Detected',
    'High Confidence',
    'Scan New Leaf',
    'Crop Identification',
    'Disease Detection',
    'Onion',
    'Mango',
    'Sugarcane',
    'Evidence & 7-Day Plan',
    'AI Crop Health & Disease Scanner',
]

print("--- Translation Verification in Django (Urdu) ---")
for k in test_keys:
    res = _(k)
    print(f"{k:35} -> {res}")
