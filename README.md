# WhatsApp script channel

This branch publishes the WhatsApp Web script (`js.abr`, WA-JS) that KFZMeister and mecMeister
inject through our WPP4Delphi fork. It contains no Delphi code.

The apps read [manifest.json](manifest.json) from this branch. Each entry belongs to one
compatibility version, `TWPPConnectCompatVersion` in `Source/Model/uTWPPConnect.Constant.pas` on
`fix/remove-compiler-warnings`:

- `active`: `url` and `sha256` name the newest script that works with that Delphi code. The app
  downloads it, checks the hash and caches it.
- `retired`: that Delphi code no longer works with WhatsApp Web. The app shows an update notice
  and does not connect.

Without a usable entry, or when the download fails, the app uses its last verified download and
then the script built into the exe. A failed download never retires a version.

## Publishing

```text
python publish.py publish --compat 1 --script <path to js.abr>
python publish.py retire --compat 0
```

Commit and push afterwards. Published script files are never changed or deleted, because
installed apps may still reference them.

- A script change that needs no Delphi change: publish it for the current compatibility version.
- A script change that needs Delphi changes: increase `TWPPConnectCompatVersion` in the fork,
  publish the new script for the new value, and keep the old entry until the old Delphi code
  stops working. Then retire it.
- When the fork's `Source/JS/js.abr` changes, publish it too, so apps built earlier with the
  same compatibility version get it.

## Testing

`test/manifest-compat-1-retired.json` retires compatibility version 1. Apps never read it on their
own; set `MEC_WHATSAPP_SCRIPT_MANIFEST` to its raw URL before starting the app to see the
retirement notice.
