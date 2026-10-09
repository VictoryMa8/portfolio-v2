# Restore the archived portfolio, saving current files before replacing them
from pathlib import Path
from datetime import datetime
import argparse, hashlib, json, shutil

def restore(root, dry_run=False):
    archive = root / 'archive' / 'portfolio-v2'
    manifest = json.loads((archive / 'archive-manifest.json').read_text())
    for name, expected in manifest.items():
        path = archive / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise SystemExit(f'Archive integrity check failed: {name}')
    extra = ['tailwind.css', 'tailwind-input.css', 'script.js', 'art-study.html',
             'verify.cjs', 'verify-reader.cjs', 'verification.json']
    current = {Path(name) for name in list(manifest) + extra if (root / name).is_file()}
    for directory in ['assets', 'screenshots']:
        current.update(path.relative_to(root) for path in (root / directory).rglob('*') if path.is_file())
    if dry_run:
        print(f'Verified {len(manifest)} archive files. Would save {len(current)} current files and restore the original site.')
        return
    backup = root / 'archive' / ('redesign-backup-' + datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
    backup.mkdir(parents=True)
    for relative in sorted(current):
        target = backup / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / relative, target)
    for name in manifest:
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(archive / name, target)
    print(f'Restored the original site. The redesign was saved in {backup}.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    restore(Path(__file__).resolve().parent.parent, args.dry_run)
