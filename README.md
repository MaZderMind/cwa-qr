Python implementation of the Corona-Warn-App (CWA) Event Registration
===================================================================

This is an implementation of the Protocol used to generate event and location QR codes for the Corona-Warn-App (CWA) as described in [
Corona-Warn-App: Documentation – Event Registration - Summary](https://github.com/corona-warn-app/cwa-documentation/blob/c0e2829/event_registration.md).

**This is not an official implementation – use it at your own risk** (as far as that's possible, these days…).

State
-----
The Interface described in the Document is implemented, the undocumented pieces (Public Key Value, Seed Length, Versions etc.) have been taken from the Open Source iOS Client Application. As far as I know the interface has been fully implemented, but without an actual positive Corona Test there is no way to do an End-to-End verification.

Usage
-----
The Library is not yet packaged as pip and so cwa-directory should be copied over to your project manually.

Use as follows:
```py
#!/usr/bin/env python3

import io
from datetime import datetime, timedelta, timezone

import cwa
import qrcode.image.svg

eventDescription = cwa.CwaEventDescription()
eventDescription.locationDescription = 'Zuhause'
eventDescription.locationAddress = 'Gau-Odernheim'
eventDescription.startDateTime = datetime.now(timezone.utc)
eventDescription.endDateTime = datetime.now(timezone.utc) + timedelta(days=2)
eventDescription.locationType = cwa.lowlevel.LOCATION_TYPE_PERMANENT_WORKPLACE
eventDescription.defaultCheckInLengthInMinutes = 4 * 60
qr = cwa.generateQrCode(eventDescription)

# Render QR-Code to PNG-File
img = qr.make_image(fill_color="black", back_color="white")
img.save('example.png')
print("generated example.png")

# Render QR-Code to PNG BytesIO-Object for further usage
img_bytes = io.BytesIO()
img.save(img_bytes)
print(len(img_bytes.getvalue()), " bytes of png")


# Render QR-Code to SVG-File
svg = qr.make_image(image_factory=qrcode.image.svg.SvgPathFillImage)
svg.save('example.svg')

# Render QR-Code to SVG BytesIO-Object for further usage
svg_bytes = io.BytesIO()
svg.save(svg_bytes)
print(len(svg_bytes.getvalue()), " bytes of svg")
```

CwaEventDescription
-------------------
- `locationDescription`: Description of the Location, Optional, String, max 100 Characters
- `locationAddress`: Address of the Location, Optional, String, max 100 Characters
- `startDateTime`: Start of the Event, Optional, datetime in UTC
- `endDateTime`: End of the Event, Optional, datetime in UTC
- `locationType`: Type of the Location, Optional, one of
	- `cwa.lowlevel.LOCATION_TYPE_UNSPECIFIED` = 0
	- `cwa.lowlevel.LOCATION_TYPE_PERMANENT_OTHER` = 1
	- `cwa.lowlevel.LOCATION_TYPE_TEMPORARY_OTHER` = 2
	- `cwa.lowlevel.LOCATION_TYPE_PERMANENT_RETAIL` = 3
	- `cwa.lowlevel.LOCATION_TYPE_PERMANENT_FOOD_SERVICE` = 4
	- `cwa.lowlevel.LOCATION_TYPE_PERMANENT_CRAFT` = 5
	- `cwa.lowlevel.LOCATION_TYPE_PERMANENT_WORKPLACE` = 6
	- `cwa.lowlevel.LOCATION_TYPE_PERMANENT_EDUCATIONAL_INSTITUTION` = 7
	- `cwa.lowlevel.LOCATION_TYPE_PERMANENT_PUBLIC_BUILDING` = 8
	- `cwa.lowlevel.LOCATION_TYPE_TEMPORARY_CULTURAL_EVENT` = 9
	- `cwa.lowlevel.LOCATION_TYPE_TEMPORARY_CLUB_ACTIVITY `= 10
	- `cwa.lowlevel.LOCATION_TYPE_TEMPORARY_PRIVATE_EVENT `= 11
	- `cwa.lowlevel.LOCATION_TYPE_TEMPORARY_WORSHIP_SERVICE `= 12
- `defaultCheckInLengthInMinutes`: Default Check-out time in minutes, Optional
- `randomSeed`: Specific Seed, 16 Bytes, Optional, leave Empty if unsure, see Below for Explanation

Random Seed
-----------
To mitigate [Profiling of Venues](https://github.com/corona-warn-app/cwa-documentation/blob/c0e2829/event_registration.md#profiling-of-venues), each QR-Code contains a 16 Bytes long random Seed Value, that makes each code even with the same data unique. This way a location can generate a fresh QR-Code each day and avoid the risk of being tracked.

But sometimes it is important to be able to re-generate exactly the same code, e.g. from a database or other deterministic sources. If this is important to you, you can specify your own 16 bytes in the `randomSeed` Parameter of the `CwaEventDescription` object. You can easily generate it with [`secrets.token_bytes(16)`](https://docs.python.org/3/library/secrets.html#secrets.token_bytes).

Python 2/3
----------
This library supports Python 3.6+, however there is a backport to Python 2 available at https://github.com/MaZderMind/cwa-qr/tree/py2
