#!/usr/bin/env python3

from datetime import datetime, time, timedelta, timezone

import cwa

# Construct Event-Descriptor
eventDescription = cwa.CwaEventDescription()
eventDescription.locationDescription = 'Zuhause'
eventDescription.locationAddress = 'Gau-Odernheim'
eventDescription.startDateTime = datetime.now(timezone.utc)
eventDescription.endDateTime = datetime.now(timezone.utc) + timedelta(days=2)
eventDescription.locationType = cwa.lowlevel.LOCATION_TYPE_PERMANENT_WORKPLACE
eventDescription.defaultCheckInLengthInMinutes = 4 * 60

# Renew QR-Code every night at 4:00
seedDate = eventDescription.seed = cwa.rolloverDate(datetime.now(), time(4, 0))
print("seedDate", seedDate)
eventDescription.seed = "Some Secret" + str(seedDate)

# Generate URL for Debugging purpose
url = cwa.generateUrl(eventDescription)
print('url', url)

# Generate QR-Code
qr = cwa.generateQrCode(eventDescription)

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
