#!/usr/bin/env python3

import io
from datetime import datetime, time, timezone

import qrcode.image.svg

import cwa_qr

# Construct Event-Descriptor
event_description = cwa_qr.CwaEventDescription()
event_description.location_description = 'Zuhause'
event_description.location_address = 'Gau-Odernheim'
event_description.start_date_time = datetime(2021, 4, 25, 8, 0).astimezone(timezone.utc)
event_description.end_date_time = datetime(2021, 4, 25, 18, 0).astimezone(timezone.utc)
event_description.location_type = cwa_qr.CwaLocation.permanent_workplace
event_description.default_check_in_length_in_minutes = 4 * 60

# Renew QR-Code every night at 4:00
seed_date = event_description.seed = cwa_qr.rollover_date(datetime.now(), time(4, 0))
print("seedDate", seed_date)
event_description.seed = "Some Secret" + str(seed_date)

# Generate URL for Debugging purpose
url = cwa_qr.generate_url(event_description)
print('url', url)

# Generate QR-Code
qr = cwa_qr.generate_qr_code(event_description)

# Save as PNG
img = qr.make_image(fill_color="black", back_color="white")
img.save('example.png')
print("generated example.png")

# Save as PNG to Buffer for further usage
img_bytes = io.BytesIO()
img.save(img_bytes)
print(len(img_bytes.getvalue()), " bytes of png")

# Generate SVG
svg = qr.make_image(image_factory=qrcode.image.svg.SvgPathFillImage)
svg.save('example.svg')

# Save as SVG to Buffer for further usage
svg_bytes = io.BytesIO()
svg.save(svg_bytes)
print(len(svg_bytes.getvalue()), " bytes of svg")

# Generate Poster-SVG
poster = cwa_qr.generate_poster(event_description, cwa_qr.CwaPoster.POSTER_PORTRAIT)
poster.save('poster.svg')
print("generated poster.svg")

# You can use pyrsvg (https://www.cairographics.org/cookbook/pyrsvg/) if you need to convert the poster to a PNG
# or svglib (https://pypi.org/project/svglib/) to convert it to a PDF.

# Save as Poster-SVG to Buffer for further usage
poster_svg_bytes = poster.to_str()
print(len(poster_svg_bytes), " bytes of poster-svg")
