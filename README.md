Python implementation of the Corona-Warn-App (CWA) Event Registration
===================================================================

[![GitHub](https://img.shields.io/github/license/MaZderMind/cwa-qr)](https://github.com/MaZderMind/cwa-qr/blob/main/LICENSE.txt)
[![PyPI](https://img.shields.io/pypi/v/cwa-qr)](https://pypi.org/project/cwa-qr/)

This is an implementation of the Protocol used to generate event and location QR codes for the Corona-Warn-App (CWA) as described in [
Corona-Warn-App: Documentation – Event Registration - Summary](https://github.com/corona-warn-app/cwa-documentation/blob/master/event_registration.md).

**This is not an official implementation – use it at your own risk** (as far as that's possible, these days…).

State
-----
The Interface described in the Document is implemented, the undocumented pieces (Public Key Value, Seed Length, Versions etc.) have been taken from the Open Source iOS Client Application. As far as I know the interface has been fully implemented, but without an actual positive Corona Test there is no way to do an End-to-End verification.

Usage
-----
Use as follows:

```py
#!/usr/bin/env python3

from datetime import datetime, time, timezone

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

# Generate QR-Code
qr = cwa_qr.generate_qr_code(event_description)

# Save as PNG
img = qr.make_image(fill_color="black", back_color="white")
img.save('example.png')
print("generated example.png")
```

See [example_full.py](example_full.py) for an example using all features.

CwaEventDescription
-------------------
- `location_description`: Description of the Location, Optional, String, max 100 Characters
- `location_address`: Address of the Location, Optional, String, max 100 Characters
- `start_date_time`: Start of the Event, Optional, datetime in UTC
- `end_date_time`: End of the Event, Optional, datetime in UTC
  **Caution**, QR-Codes generated with different start/end times will have different Event-IDs and not warn users that
  have checked in with the other Code. **Do not use `datetime.now()`** for start/end-date. For repeating Events use
  `cwa_qr.rollover_date` to get a defined rollover.
- `location_type`: Type of the Location, Optional, one of
  - `cwa.CwaLocation.unspecified`
  - `cwa.CwaLocation.permanent_other`
  - `cwa.CwaLocation.temporary_other`
  - `cwa.CwaLocation.permanent_retail`
  - `cwa.CwaLocation.permanent_food_service`
  - `cwa.CwaLocation.permanent_craft`
  - `cwa.CwaLocation.permanent_workplace`
  - `cwa.CwaLocation.permanent_educational_institution`
  - `cwa.CwaLocation.permanent_public_building`
  - `cwa.CwaLocation.temporary_cultural_event`
  - `cwa.CwaLocation.temporary_club_activity`
  - `cwa.CwaLocation.temporary_private_event`
  - `cwa.CwaLocation.temporary_worship_service`
- `default_check_in_length_in_minutes`: Default Check-out time in minutes, Optional
- `seed`: Seed to rotate the QR-Code, Optional, `[str, bytes, int, float, date, datetime]` or `None` (Default).
  **Use with caution & read below!** If unsure, leave blank.

Rotating QR-Codes
-----------------
From the [Documentation](https://github.com/corona-warn-app/cwa-documentation/blob/master/event_registration.md):
> Profiling of Venues
>
> An adversary can collect this information for a single venue by scanning the QR code and extracting and storing the
> data. To mitigate the risk, CWA encourages owners to regularly generate new QR codes for their venues. The more
> frequent QR codes are updated, the more difficult it is to keep a central database with venue data up-to-date.
> **However**, a new QR code should only be generated **when no visitor is at the event or location**, because
> visitors can only warn each other **with the same QR code**.

From an Application-Developers point of view, special care must be taken to decide if and when QR codes should be
changed. A naive approach, i.e. changing the QR-Code on every call, would render the complete Warning-Chain totally
useless **without anyone noticing**. Therefore, the Default of this Library as of 2021/04/26 is to **not seed the
QR-Codes with random values**. This results in every QR-Code being generated without an explicit Seed to be identical,
which minimizes the Risk of having QR-Codes that do not warn users as expected at the increased risk of profiling of
Venues.

As an Application-Developer you are encouraged to **ask you user if and when they want their QR-Codes to change** and
explain to them that they should only rotate their Codes **when they are sure that nobody is at the location or in the
venue** for at least 30 Minutes, to allow airborne particles to settle or get filtered out. Do **not make assumptions**
regarding a good time to rotate QR-Codes (i.e. always at 4:00 am) because they will fail so warn people in some
important Situations (nightclubs, hotels, night-shift working) **without anyone noticing**.

To disable rotation of QR-Codes, specify None as the Seed (Default behaviour).

The Library also gives you a utility to allow rotating QR-Codes at a given time of the day. Please make
sure to also integrate some kind of Secret into the seed, to prevent an adversary from calculating  future QR-Codes.
The Secret *must stay constant* over time, or the resulting QR-Codes will not correctly trigger warnings.

```py
import io
from datetime import datetime, time

import cwa_qr

# Construct Event-Descriptor
event_description = cwa_qr.CwaEventDescription()
# …
seed_date = cwa_qr.rollover_date(datetime.now(), time(4, 0))
event_description.seed = "Some Secret" + str(seed_date)
```

this will keep the date-based seed until 4:00 am on the next day and only then roll over to the next day.
See [test_rollover.py](cwa_qr/test_rollover.py) for an in-depth look at the rollover code.

Posters
-------
This Library has Support for compositing the QR-Code with a Poster, explaining its usage:
"Checken Sie ein, stoppen Sie das Virus". The Poster-Functionality works by composing the QR-Code SVG with the
Poster-SVG and thus only supports SVG-Output. Both Landscape and Portrait-Posters are supported.

You can use [pyrsvg](https://www.cairographics.org/cookbook/pyrsvg/) if you need to convert the poster to a PNG
or [svglib](https://pypi.org/project/svglib/) to convert it to a PDF.

See [example_full.py](example_full.py) for an Example on how to use the Poster-Functionality.

Python 2/3
----------
This library supports Python 3.7+, however there is a backport to Python 2 available at https://github.com/MaZderMind/cwa-qr/tree/py2
