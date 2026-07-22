# Official Parish Photo Replacement Checklist

The current parish-building images are placeholders until approved photographs arrive. Replace each image in its existing location so all pages update from the same shared record.

## Photographs to collect for each parish

- Straight, recognizable exterior view showing the main entrance
- Sanctuary/interior view taken reverently when the church is empty
- Accessible entrance and ramp, if a separate practical photo would help visitors
- Parish hall or family-access detail only when genuinely useful

## Photo standards

- Use original files, not social-media screenshots.
- Prefer horizontal images at least 2000 pixels wide.
- Avoid license plates, private paperwork, children, and identifiable people unless explicit permission is documented.
- Avoid photographing during Mass, Confession, Adoration, or private pastoral moments.
- Keep the altar, tabernacle, crucifix, and sacred images presented reverently.
- Record the photographer and permission/ownership at the time the photo is received.

## One-place replacement

The parish images are referenced in `data/locations.yaml`:

- St. Ann: `/images/parishes/st-ann.jpg`
- Our Lady of Perpetual Help: `/images/parishes/olph.jpg`
- Mother of Sorrows: `/images/parishes/mother-of-sorrows.jpg`

Replace the corresponding file while keeping the approved filename, or update the single `image` field in `data/locations.yaml`. Do not paste the same image path into individual templates.

## Before publishing a replacement

1. Confirm parish and building identity.
2. Confirm photographer permission and credit.
3. Crop a copy for web use; preserve the original separately.
4. Write literal alt text naming the parish and city.
5. Check desktop, phone, and 200% zoom crops.
6. Confirm the image does not imply an entrance or accessibility feature that is not shown accurately.
7. Run the image-dimension, internal-link, SEO, and accessibility checks.
