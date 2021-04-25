#!/usr/bin/env python3

from datetime import datetime, time, timezone

import cwa_qr

# Construct Event-Descriptor
event_description = cwa_qr.CwaEventDescription()
event_description.location_description = 'Zuhause'
event_description.location_address = 'Gau-Odernheim'
event_description.start_date_time = datetime(2021, 4, 25, 8, 0).astimezone(timezone.utc)
event_description.end_date_time = datetime(2021, 4, 25, 18, 0).astimezone(timezone.utc)
event_description.location_type = cwa_qr.lowlevel.LOCATION_TYPE_PERMANENT_WORKPLACE
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

img = qr.make_image(fill_color="black", back_color="white")
img.save('example.png')
print("generated example.png")

# import io
# img_bytes = io.BytesIO()
# img.save(img_bytes)
# print(len(img_bytes.getvalue()), " bytes of png")


# import qrcode.image.svg
# svg = qr.make_image(image_factory=qrcode.image.svg.SvgPathFillImage)
# svg.save('example.svg')

# svg_bytes = io.BytesIO()
# svg.save(svg_bytes)
# print(len(svg_bytes.getvalue()), " bytes of svg")
