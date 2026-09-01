# Character sheet prompts (three-panel)

In Cinema Studio this runs as a two-node graph: a prompt node feeding an image-generation
node, which returns the three panels — full-body front, full-body back, close-up portrait —
side by side on a flat mid-grey background.

Two variants. Pick before generating.

---

## Variant A — full preserve (face + wardrobe + hair from the reference)

Use when the reference person is already dressed and styled for the scene. Attach the
reference images. The only line to adapt is the "omitted element" sentence (here: the bag) —
change it to whatever must not appear, or delete it if nothing needs removing.

Create a professional photorealistic three-panel film character sheet based strictly on the uploaded reference images. Preserve the exact facial identity, facial structure, age, skin tone, hairstyle, body proportions, wardrobe, footwear, wearable accessories, grooming and distinctive physical features of the referenced person. Preserve the clothing exactly as shown in the reference, including its design, colours, materials, fit and natural fabric folds. Preserve all worn jewellery and other wearable accessories. The only reference element that must be omitted is the bag. Both hands remain completely empty, and no handbag, shoulder bag, clutch, briefcase or other bag appears anywhere in the image. Arrange three vertical photographs side by side: Left panel: a complete full-body front view. The character stands straight in a relaxed neutral pose, facing forward, with both empty arms resting naturally at the sides. Both empty hands and the entire figure from head to feet are clearly visible. Middle panel: a complete full-body back view of the same character in the same neutral standing pose, with both empty arms resting naturally at the sides. Clearly show the hairstyle, back of the original clothing, body proportions and footwear. Right panel: a large close-up head-and-shoulders portrait of the same character from a subtle three-quarter angle. The face is clearly visible, with relaxed closed lips, a calm neutral expression and natural catchlights in the eyes. Preserve the visible upper section of the original clothing and all wearable accessories exactly as shown in the reference. The exact same real person must appear in all three panels. Maintain perfect consistency of facial identity, hairstyle, body shape, original clothing, colours, materials, footwear, wearable accessories and grooming. Do not redesign, beautify or reinterpret the character. Use the same flat neutral mid-grey studio background across all three panels. Keep the surrounding space completely empty and uncluttered. Soft, even studio lighting, subtle natural shadow falloff, realistic unretouched skin with visible natural texture, detailed fabric and restrained neutral colours. Clean contemporary casting photography with no decorative elements, captions or text.


---

## Variant B — facial identity only (re-cast into new wardrobe)

Use when the character keeps the reference face but needs different hair, wardrobe or
styling. Same structure, but the preserve-list is cut down to the face and the new styling
is specified explicitly. Change the bracketed parts:

> Create a professional photorealistic three-panel film character sheet based strictly on
> the uploaded reference image for facial identity only. Preserve the exact facial identity,
> facial structure, age and skin tone of the referenced person. [HAIR: e.g. dreadlocks —
> state length, texture and styling.] [WARDROBE: e.g. a charcoal two-piece suit, white
> shirt, patterned tie, black leather shoes — state design, colours, materials and fit.]
> Both hands remain completely empty, and no bag appears anywhere in the image.
> Arrange three vertical photographs side by side: Left panel: a complete full-body front
> view, standing straight in a relaxed neutral pose, facing forward, both empty arms resting
> naturally at the sides, entire figure from head to feet clearly visible. Middle panel: a
> complete full-body back view of the same character in the same neutral standing pose,
> clearly showing the hairstyle, back of the clothing, body proportions and footwear. Right
> panel: a large close-up head-and-shoulders portrait from a subtle three-quarter angle,
> face clearly visible, relaxed closed lips, calm neutral expression, natural catchlights in
> the eyes. The exact same real person must appear in all three panels. Maintain perfect
> consistency of facial identity, hairstyle, body shape, clothing, colours, materials,
> footwear and grooming. Do not redesign, beautify or reinterpret the face. Use the same
> flat neutral mid-grey studio background across all three panels, surrounding space
> completely empty and uncluttered. Soft, even studio lighting, subtle natural shadow
> falloff, realistic unretouched skin with visible natural texture, detailed fabric and
> restrained neutral colours. Clean contemporary casting photography with no decorative
> elements, captions or text.

---

## Why they are written this way

- **"based strictly on the uploaded reference images"** + the long preserve-list is what
  stops the model beautifying or redesigning the person. In Variant B the same phrase is
  narrowed to "facial identity only" so wardrobe instructions are free to override.
- **Three panels — front, back, close-up** — the back view is what makes hair and clothing
  hold up when the character turns in a scene; the close-up is what video generation reads
  the face from.
- **Empty hands, no bag** — anything held in the sheet gets inherited into scenes where it
  makes no sense.
- **Flat neutral mid-grey background, soft even studio lighting** — no environment leaks
  into the character reference.
- **"realistic unretouched skin with visible natural texture"** — the counter to plastic
  AI skin in every downstream generation.
