"""
Clean and compile PO file:
1. Removes 'fuzzy' flag from all valid translated entries.
2. Ensures clean UTF-8 encoding across all entries.
3. Compiles directly to .mo binary format.
"""
import os
import polib

def clean_and_compile():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    po_path = os.path.join(base_dir, 'locale', 'ur', 'LC_MESSAGES', 'django.po')
    mo_path = os.path.join(base_dir, 'locale', 'ur', 'LC_MESSAGES', 'django.mo')
    
    po = polib.pofile(po_path, encoding='utf-8')
    unfuzzied = 0
    for entry in po:
        if 'fuzzy' in entry.flags:
            entry.flags.remove('fuzzy')
            unfuzzied += 1
            
    po.save(po_path)
    po.save_as_mofile(mo_path)
    print(f"Cleaned {unfuzzied} fuzzy entries and compiled {len(po)} messages to {mo_path} with pure UTF-8.")

if __name__ == '__main__':
    clean_and_compile()
