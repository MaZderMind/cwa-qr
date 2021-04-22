#!/usr/bin/env python3

import io
from datetime import datetime, timedelta, timezone

from cwa import cwa
import qrcode.image.svg

eventDescription = cwa.CwaEventDescription()
eventDescription.locationDescription = 'Zuhause'
eventDescription.locationAddress = 'Gau-Odernheim'
eventDescription.startDateTime = datetime.now(timezone.utc)
eventDescription.endDateTime = datetime.now(timezone.utc) + timedelta(days=2)
eventDescription.locationType = cwa.lowlevel.LOCATION_TYPE_PERMANENT_WORKPLACE
eventDescription.defaultCheckInLengthInMinutes = 4 * 60
qr = cwa.generateQrCode(eventDescription)

img = qr.make_image(fill_color="black", back_color="white")
img.save('example.png')
print("generated example.png")

# img_bytes = io.BytesIO()
# img.save(img_bytes)
# print(len(img_bytes.getvalue()), " bytes of png")


# svg = qr.make_image(image_factory=qrcode.image.svg.SvgPathFillImage)
# svg.save('example.svg')

# svg_bytes = io.BytesIO()
# svg.save(svg_bytes)
# print(len(svg_bytes.getvalue()), " bytes of svg")
