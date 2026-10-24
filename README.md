# OPX images

Image assets for [opx_infinity](https://github.com/opx77-framework/opx_infinity),
hosted separately so the framework ships no inventory or garment pictures.

Run `upload-images.sh` or `upload-images.bat` from your OPX framework installation.
Enter your Fivemanage API key when prompted. The uploader obtains these assets
only when needed and publishes them to your own account. Catalogue names stay
unchanged; no manual CDN URL editing is required.

For custom assets, clone this repository next to `opx_infinity` as `opx_images`,
then replace or add files using their catalogue names. Alternatively pass
`--images-dir /path/to/your/images` to the uploader. Preserve the `clothing/`
subdirectory for garment pictures.

Garment sources and credits: [clothing/ATTRIBUTION.md](clothing/ATTRIBUTION.md).
The images retain their original authors' rights; the framework's code licence
does not relicense third-party game assets.
