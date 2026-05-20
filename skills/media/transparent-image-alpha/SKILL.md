---
name: transparent-image-alpha
description: Generate real-alpha transparent PNG/WebP assets from AI image generation by prompting a flat chroma-key background, removing the key locally, and validating transparency. Use when the user asks for transparent-background generated images, cutouts, stickers, sprites, icons, or product/object PNGs with actual alpha.
---

# Transparent Image Alpha

Create a real-alpha PNG/WebP from a generated image by using a flat chroma-key
background, then removing that key locally.

Do not describe a generated key-color source as transparent. Only the
post-processed PNG/WebP with an alpha channel is the final transparent asset.

## Workflow

1. Pick a chroma key unlikely to appear in the subject.
   - Default: `#00ff00`.
   - Use `#ff00ff` when the subject is green or likely to contain green.
   - Avoid complex transparency such as hair, fur, feathers, smoke, glass,
     liquids, reflections, or soft shadows unless the user accepts edge risk.

2. Prompt image generation for an opaque subject on a perfectly flat key
   background:

```text
Create the requested subject on a perfectly flat solid #00ff00 chroma-key background for background removal.
The background must be one uniform color with no shadows, gradients, texture, reflections, floor plane, or lighting variation.
Keep the subject fully separated from the background with crisp edges and generous padding.
Do not use #00ff00 anywhere in the subject.
No cast shadow, no contact shadow, no reflection, no watermark, and no text unless explicitly requested.
```

Add the actual subject, style, and composition requirements before these
constraints.

3. Copy the generated source image into the workspace or task-local output
   directory.

4. Convert the key to alpha with the bundled helper:

```bash
python3 skills/media/transparent-image-alpha/scripts/make_alpha_from_chroma.py \
  --input <source-keyed.png> \
  --out <final-transparent.png>
```

5. Validate the result:
   - Output must be `.png` or `.webp`.
   - Corners should be transparent.
   - The subject should have a nonempty alpha bounding box.
   - If a key-color fringe remains, retry with `--edge-contract 1`.

6. Report the final path, source path, key color, and validation summary.

## Useful Commands

Retry with a 1 px matte contraction:

```bash
python3 skills/media/transparent-image-alpha/scripts/make_alpha_from_chroma.py \
  --input <source-keyed.png> \
  --out <final-transparent.png> \
  --edge-contract 1
```

Overwrite an existing output only when the user explicitly asked for
replacement:

```bash
python3 skills/media/transparent-image-alpha/scripts/make_alpha_from_chroma.py \
  --input <source-keyed.png> \
  --out <final-transparent.png> \
  --force
```
