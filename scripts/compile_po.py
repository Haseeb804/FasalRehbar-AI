"""
Official polib-based compiler for Django .po -> .mo files with 100% pure UTF-8 integrity.
"""
import os
import polib

def compile_catalog():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    po_path = os.path.join(base_dir, 'locale', 'ur', 'LC_MESSAGES', 'django.po')
    mo_path = os.path.join(base_dir, 'locale', 'ur', 'LC_MESSAGES', 'django.mo')
    
    po = polib.pofile(po_path, encoding='utf-8')
    po.save_as_mofile(mo_path)
    print(f"Successfully compiled {len(po)} entries into {mo_path} using polib with pure UTF-8.")

if __name__ == '__main__':
    compile_catalog()
