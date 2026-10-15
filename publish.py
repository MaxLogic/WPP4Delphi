"""Publish or retire WhatsApp scripts (js.abr) in the MaxLogic WPP4Delphi script channel.

Run from the root of the script-channel branch:

    python publish.py publish --compat 1 --script ..\\Source\\JS\\js.abr
    python publish.py retire --compat 0

publish copies the script to scripts/compat-<n>/js-<version>.abr, records its SHA-256 and makes it
the active entry for that compatibility version. retire marks a version as no longer working.
Commit and push the result; apps read manifest.json from this branch.
"""

import argparse
import datetime
import hashlib
import json
import pathlib
import shutil
import sys

CHANNEL = 'maxlogic-wpp4delphi-script'
SCHEMA = 1
RAW_BASE = 'https://raw.githubusercontent.com/MaxLogic/WPP4Delphi/script-channel/'
ROOT = pathlib.Path(__file__).resolve().parent
MANIFEST = ROOT / 'manifest.json'


def load_manifest():
    if not MANIFEST.exists():
        return {'channel': CHANNEL, 'schema': SCHEMA, 'entries': []}
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    if manifest.get('channel') != CHANNEL or manifest.get('schema') != SCHEMA:
        sys.exit('manifest.json has an unexpected channel or schema')
    return manifest


def save_manifest(manifest, compat, entry):
    entries = [e for e in manifest['entries'] if e.get('compat') != compat]
    entries.append(entry)
    manifest['entries'] = sorted(entries, key=lambda e: e['compat'])
    MANIFEST.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(entry, indent=2))


def next_version(compat):
    today = datetime.date.today().strftime('%Y.%m.%d')
    folder = ROOT / 'scripts' / f'compat-{compat}'
    number = 1
    while (folder / f'js-{today}.{number}.abr').exists():
        number += 1
    return f'{today}.{number}'


def publish(args):
    source = pathlib.Path(args.script)
    data = source.read_bytes()
    version = args.version or next_version(args.compat)
    relative = f'scripts/compat-{args.compat}/js-{version}.abr'
    target = ROOT / relative
    if target.exists():
        sys.exit(f'{relative} already exists')
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    entry = {
        'compat': args.compat,
        'status': 'active',
        'scriptVersion': version,
        'url': RAW_BASE + relative,
        'sha256': hashlib.sha256(data).hexdigest(),
    }
    save_manifest(load_manifest(), args.compat, entry)


def retire(args):
    save_manifest(load_manifest(), args.compat, {'compat': args.compat, 'status': 'retired'})


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest='command', required=True)
    publish_parser = commands.add_parser('publish')
    publish_parser.add_argument('--compat', type=int, required=True)
    publish_parser.add_argument('--script', required=True)
    publish_parser.add_argument('--version', help='default: <today>.<n>')
    publish_parser.set_defaults(handler=publish)
    retire_parser = commands.add_parser('retire')
    retire_parser.add_argument('--compat', type=int, required=True)
    retire_parser.set_defaults(handler=retire)
    args = parser.parse_args()
    args.handler(args)


if __name__ == '__main__':
    main()
