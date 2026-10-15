# Embedded WA-JS

`js.abr` contains the WPP4Delphi wrapper and the official WA-JS 4.7.1 bundle.
The wrapper remains compatible with script compatibility version 1.

- Bundle: https://github.com/wppconnect-team/wa-js/releases/download/v4.7.1/wppconnect-wa.js
- Original bundle SHA-256: `ed4cc6b17ce18d726b0bd89c0b30021c5b8266f823f13509c08170b7ace96126`
- License notices: https://unpkg.com/@wppconnect/wa-js@4.7.1/dist/wppconnect-wa.js.LICENSE.txt
- License notices SHA-256: `5a2448a164170355f95e2e7c7a88b48c73ec7fe2dd07162d4a201f2b06257525`.

The bundle's line endings are normalized to CRLF inside `js.abr`. The wrapper
before and after the bundle is preserved, apart from its version marker.

Version 4.7.1 repairs discovery of `WAWebMediaPrep` and the moved
`WAWebPrepRawMedia.prepRawMedia` export used when sending documents with recent
WhatsApp Web versions. This source update does not publish the runtime script
channel; channel publication is a separate operation.
