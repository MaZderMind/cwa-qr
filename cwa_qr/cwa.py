import base64
import io
import os
from datetime import date, datetime
from typing import Optional, Union

import qrcode
from svgutils import transform as svgut

from . import cwa_pb2 as lowlevel
from . import seed

PUBLIC_KEY_STR = 'gwLMzE153tQwAOf2MZoUXXfzWTdlSpfS99iZffmcmxOG9njSK4RTimFOFwDh6t0Tyw8XR01ugDYjtuKwj' \
                 'juK49Oh83FWct6XpefPi9Skjxvvz53i9gaMmUEc96pbtoaA'

PUBLIC_KEY = base64.standard_b64decode(PUBLIC_KEY_STR.encode('ascii'))


class CwaEventDescription(object):
    def __init__(self):
        """Description of the Location, Required, String, max 100 Characters"""
        self.location_description: Optional[str] = None

        """Address of the Location, Required, String, max 100 Characters"""
        self.location_address: Optional[str] = None

        """Start of the Event, Optional, datetime in UTC"""
        self.start_date_time: Optional[datetime] = None

        """End of the Event, Optional, datetime in UTC"""
        self.end_date_time: Optional[datetime] = None

        """Type of the Location, Optional

        one of
        - cwa_qr.lowlevel.LOCATION_TYPE_UNSPECIFIED = 0
        - cwa_qr.lowlevel.LOCATION_TYPE_PERMANENT_OTHER = 1
        - cwa_qr.lowlevel.LOCATION_TYPE_TEMPORARY_OTHER = 2
        - cwa_qr.lowlevel.LOCATION_TYPE_PERMANENT_RETAIL = 3
        - cwa_qr.lowlevel.LOCATION_TYPE_PERMANENT_FOOD_SERVICE = 4
        - cwa_qr.lowlevel.LOCATION_TYPE_PERMANENT_CRAFT = 5
        - cwa_qr.lowlevel.LOCATION_TYPE_PERMANENT_WORKPLACE = 6
        - cwa_qr.lowlevel.LOCATION_TYPE_PERMANENT_EDUCATIONAL_INSTITUTION = 7
        - cwa_qr.lowlevel.LOCATION_TYPE_PERMANENT_PUBLIC_BUILDING = 8
        - cwa_qr.lowlevel.LOCATION_TYPE_TEMPORARY_CULTURAL_EVENT = 9
        - cwa_qr.lowlevel.LOCATION_TYPE_TEMPORARY_CLUB_ACTIVITY = 10
        - cwa_qr.lowlevel.LOCATION_TYPE_TEMPORARY_PRIVATE_EVENT = 11
        - cwa_qr.lowlevel.LOCATION_TYPE_TEMPORARY_WORSHIP_SERVICE = 12
        """
        self.location_type: Optional[int] = None

        """Default Checkout-Time im Minutes, Optional"""
        self.default_check_in_length_in_minutes: Optional[int] = None

        """Seed to rotate the QR-Code, Optional, [str, bytes, int, float, date, datetime] or None (Default)

        Use with caution & read the Section about *Rotating QR-Codes* in the README first! If unsure, leave blank.
        """
        self.seed: Union[str, bytes, int, float, date, datetime, None] = None


class CwaPoster(object):
    POSTER_PORTRAIT = 'portrait'
    POSTER_LANDSCAPE = 'landscape'

    TRANSLATIONS = {
        POSTER_PORTRAIT: {
            'file': 'poster_portrait.svg',
            'x': 80,
            'y': 60,
            'scale': 6
        },
        POSTER_LANDSCAPE: {
            'file': 'poster_landscape.svg',
            'x': 42,
            'y': 120,
            'scale': 4.8
        }
    }


def generate_payload(event_description: CwaEventDescription) -> lowlevel.QRCodePayload:
    payload = lowlevel.QRCodePayload()
    payload.version = 1

    payload.locationData.version = 1
    payload.locationData.description = event_description.location_description
    payload.locationData.address = event_description.location_address
    payload.locationData.startTimestamp = int(event_description.start_date_time.timestamp()) if \
        event_description.start_date_time else 0
    payload.locationData.endTimestamp = int(event_description.end_date_time.timestamp()) if \
        event_description.end_date_time else 0

    payload.crowdNotifierData.version = 1
    payload.crowdNotifierData.publicKey = PUBLIC_KEY
    payload.crowdNotifierData.cryptographicSeed = seed.construct_seed(event_description.seed)

    cwa_location_data = lowlevel.CWALocationData()
    cwa_location_data.version = 1
    cwa_location_data.type = event_description.location_type if \
        event_description.location_type is not None else lowlevel.LOCATION_TYPE_UNSPECIFIED
    cwa_location_data.defaultCheckInLengthInMinutes = event_description.default_check_in_length_in_minutes if \
        event_description.default_check_in_length_in_minutes is not None else 0

    payload.countryData = cwa_location_data.SerializeToString()
    return payload


def generate_url(event_description: CwaEventDescription) -> str:
    payload = generate_payload(event_description)
    serialized = payload.SerializeToString()
    encoded = base64.urlsafe_b64encode(serialized)
    url = 'https://e.coronawarn.app?v=1#' + encoded.decode('ascii')

    return url


def generate_qr_code(event_description: CwaEventDescription) -> qrcode.QRCode:
    qr = qrcode.QRCode()
    qr.add_data(generate_url(event_description))
    qr.make(fit=True)

    return qr


def generate_poster(event_description: CwaEventDescription, template: CwaPoster) -> svgut.SVGFigure:
    qr = generate_qr_code(event_description)
    svg = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)
    svg_bytes = io.BytesIO()
    svg.save(svg_bytes)

    poster = svgut.fromfile('{}/{}'.format(
        os.path.dirname(os.path.abspath(__file__)),
        CwaPoster.TRANSLATIONS[template]['file']
    ))
    overlay = svgut.fromstring(svg_bytes.getvalue().decode('UTF-8')).getroot()
    overlay.moveto(
        CwaPoster.TRANSLATIONS[template]['x'],
        CwaPoster.TRANSLATIONS[template]['y'],
        CwaPoster.TRANSLATIONS[template]['scale']
    )
    poster.append([overlay])
    return poster
