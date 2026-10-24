<h1 align="center">OPX//77 · opx_images</h1>

<p align="center">
  <strong>Inventory and garment pictures for <a href="https://github.com/opx77-framework/opx_infinity">OPX//77</a>, hosted separately from the Open77 framework.</strong>
</p>

<p align="center">
  <a href="https://github.com/opx77-framework/opx_images/actions/workflows/check.yml"><img alt="check" src="https://github.com/opx77-framework/opx_images/actions/workflows/check.yml/badge.svg?branch=main"></a>
  <img alt="Status: alpha" src="https://img.shields.io/badge/status-alpha-orange">
  <a href="https://opx77-framework.github.io/opx77_doc/"><img alt="Documentation" src="https://img.shields.io/badge/docs-opx77__doc-c5003c"></a>
  <a href="https://discord.gg/xpSuYgEYsU"><img alt="Discord" src="https://img.shields.io/badge/discord-join-5865F2?logo=discord&logoColor=white"></a>
</p>

---

## What it is

This repository holds OPX inventory and garment pictures. It is an asset source,
not an Open77 resource: do not add it to `resources.load`. The framework ships
only picture names and public CDN URLs. No inventory or garment images are copied
into the game resource.

## Quick start

1. Clone `opx_images` separately from `opx_infinity`. All pictures live under
   `images/`, including garments under `images/clothing/`.
2. Install Python 3.10+, then run **from this repository**:
   - Linux: `bash upload-images.sh`
   - Windows: `upload-images.bat`
3. Enter your Fivemanage API key when prompted. The script scans **every file in
   `images/` and its subdirectories**, uploads new or changed content, and reuses
   unchanged uploads. It never saves the key. Automation may supply
   `FIVEMANAGE_API_KEY` in the environment.
4. In the framework, set the same account's key in the **server-only**
   `config/images.lua`. Enable Open77's HTTP bridge and allow `api.fivemanage.com`
   in `server.jsonc` (see the framework manual), then restart OPX.

Both components use a key: this repository uses it to upload; the framework uses
it to read the account catalogue. Players receive public URLs only. There is no
local-image mode: without this setup, OPX shows text monograms and no inventory
or garment pictures. Catalogue entries remain names such as `water.png`; no URL
editing or framework rebuild is needed.

OPX refreshes the public catalogue at startup and every five minutes. Re-run the
uploader after changing images. Duplicate names use the latest upload timestamp;
reverting a picture uploads it again so the correct version is selected. Old CDN
files are never automatically deleted. Storage and bandwidth follow your plan.

## Custom pictures

Add or replace files **inside `images/`**, preserving their relative names.
The uploader walks all subdirectories recursively: `images/clothing/a.webp`
becomes `clothing/a.webp` in the OPX lookup table. File names may contain letters,
numbers, underscores, dots and hyphens. Put only image files in this directory;
files larger than 16 MiB are refused. Images stay outside `opx_infinity`.

Actual account uploads and rendering still require an in-game check with your own
key; automated checks cover recursive uploads, resuming, content reuse and V3 metadata.

## Contributing

Use a feature branch and pull request. Keep file names stable: the framework's
catalogue references them. Update `images.sha256` when changing assets, and update
the matching `tools/image-catalog.txt` in the framework when catalogue references change.
Only contribute pictures you are entitled to share, retaining their credits.

The organization's [contributing guide](https://github.com/opx77-framework/.github/blob/main/CONTRIBUTING.md),
[code of conduct](https://github.com/opx77-framework/.github/blob/main/CODE_OF_CONDUCT.md),
[support](https://github.com/opx77-framework/.github/blob/main/SUPPORT.md) and
[security policy](https://github.com/opx77-framework/.github/blob/main/SECURITY.md) apply.

## Licence and credits

Repository documentation and original tooling are MIT licensed, copyright
(c) 2026 Luís MOUTA; see [LICENSE](LICENSE). **Third-party images are excluded.**
Cyberpunk 2077 images remain copyright CD PROJEKT RED; Cyberpunk 2077 is a
trademark of CD PROJEKT S.A. This is an unofficial fan project, not affiliated
with CD PROJEKT RED. See [NOTICE.md](NOTICE.md) and
[garment attribution](docs/ATTRIBUTION.md) for sources and rights.
