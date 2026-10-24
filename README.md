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

From an OPX framework installation with CDN support, run:

- Linux: `bash upload-images.sh`
- Windows: `upload-images.bat`

Install Python 3.10+ first. Enter your Fivemanage token when prompted. The script
fetches this package temporarily when needed, checks the expected SHA-256 hashes,
uploads pictures to your account and installs the public name-to-URL map. Existing
uploads are reused; no token is saved or sent to players. Restart the OPX resource
after publishing. Catalogue entries remain file names such as `water.png`.
Fivemanage setup is required: without it, OPX displays text monograms and no
inventory or garment pictures. There is no local-image mode.

The CDN integration is being introduced in `opx_infinity`; older installations
need that update before using these scripts. Live uploads and rendering need an
in-game check with your own account.

## Custom pictures

Clone this repository next to `opx_infinity` as `opx_images`. Add or replace
pictures under `images/`, using their catalogue names, then run the uploader from OPX again.
The uploader scans all pictures in `images/` and every subdirectory recursively.
Garments live under `images/clothing/`. Relative names are preserved. Images
remain outside `opx_infinity`. Use the same upload script after changing pictures.

Supported formats: PNG, WebP, JPEG, GIF, AVIF; maximum 16 MiB per file. The uploader
never deletes old CDN uploads. Storage and bandwidth follow your Fivemanage plan.

## Contributing

Use a feature branch and pull request. Keep file names stable: the framework's
catalogue references them. Update `images.sha256` when changing assets, and update
the matching `tools/image-catalog.txt` and pinned asset revision in the framework.
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
