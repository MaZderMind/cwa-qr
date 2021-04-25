import base64
from typing import Optional, Union

import qrcode
from datetime import datetime, date

from . import cwa_pb2 as lowlevel
from . import seed

PUBLIC_KEY_STR = 'gwLMzE153tQwAOf2MZoUXXfzWTdlSpfS99iZffmcmxOG9njSK4RTimFOFwDh6t0Tyw8XR01ugDYjtuKwj' \
                 'juK49Oh83FWct6XpefPi9Skjxvvz53i9gaMmUEc96pbtoaA'

PUBLIC_KEY = base64.standard_b64decode(PUBLIC_KEY_STR.encode('ascii'))


class CwaEventDescription(object):
    def __init__(self):
        """Description of the Location, Required, String, max 100 Characters"""
        self.locationDescription: Optional[str] = None

        """Address of the Location, Required, String, max 100 Characters"""
        self.locationAddress: Optional[str] = None

        """Start of the Event, Optional, datetime in UTC"""
        self.startDateTime: Optional[datetime] = None

        """End of the Event, Optional, datetime in UTC"""
        self.endDateTime: Optional[datetime] = None

        """Type of the Location, Optional

        one of
        - cwa.lowlevel.LOCATION_TYPE_UNSPECIFIED = 0
        - cwa.lowlevel.LOCATION_TYPE_PERMANENT_OTHER = 1
        - cwa.lowlevel.LOCATION_TYPE_TEMPORARY_OTHER = 2
        - cwa.lowlevel.LOCATION_TYPE_PERMANENT_RETAIL = 3
        - cwa.lowlevel.LOCATION_TYPE_PERMANENT_FOOD_SERVICE = 4
        - cwa.lowlevel.LOCATION_TYPE_PERMANENT_CRAFT = 5
        - cwa.lowlevel.LOCATION_TYPE_PERMANENT_WORKPLACE = 6
        - cwa.lowlevel.LOCATION_TYPE_PERMANENT_EDUCATIONAL_INSTITUTION = 7
        - cwa.lowlevel.LOCATION_TYPE_PERMANENT_PUBLIC_BUILDING = 8
        - cwa.lowlevel.LOCATION_TYPE_TEMPORARY_CULTURAL_EVENT = 9
        - cwa.lowlevel.LOCATION_TYPE_TEMPORARY_CLUB_ACTIVITY = 10
        - cwa.lowlevel.LOCATION_TYPE_TEMPORARY_PRIVATE_EVENT = 11
        - cwa.lowlevel.LOCATION_TYPE_TEMPORARY_WORSHIP_SERVICE = 12
        """
        self.locationType: Optional[int] = None

        """Default Checkout-Time im Minutes, Optional"""
        self.defaultCheckInLengthInMinutes: Optional[int] = None

        """Specific Seed, Optional"""
        self.seed: Union[str, bytes, int, float, date, datetime, None] = None


def generatePayload(eventDescription: CwaEventDescription) -> lowlevel.QRCodePayload:
    payload = lowlevel.QRCodePayload()
    payload.version = 1

    payload.locationData.version = 1
    payload.locationData.description = eventDescription.locationDescription
    payload.locationData.address = eventDescription.locationAddress
    payload.locationData.startTimestamp = int(eventDescription.startDateTime.timestamp()) if \
        eventDescription.startDateTime else 0
    payload.locationData.endTimestamp = int(eventDescription.endDateTime.timestamp()) if \
        eventDescription.endDateTime else 0

    payload.crowdNotifierData.version = 1
    payload.crowdNotifierData.publicKey = PUBLIC_KEY
    payload.crowdNotifierData.cryptographicSeed = seed.constructSeed(eventDescription.seed)

    cwaLocationData = lowlevel.CWALocationData()
    cwaLocationData.version = 1
    cwaLocationData.type = eventDescription.locationType if \
        eventDescription.locationType is not None else lowlevel.LOCATION_TYPE_UNSPECIFIED
    cwaLocationData.defaultCheckInLengthInMinutes = eventDescription.defaultCheckInLengthInMinutes if \
        eventDescription.defaultCheckInLengthInMinutes is not None else 0

    payload.countryData = cwaLocationData.SerializeToString()
    return payload


def generateUrl(eventDescription: CwaEventDescription) -> str:
    payload = generatePayload(eventDescription)
    serialized = payload.SerializeToString()
    encoded = base64.urlsafe_b64encode(serialized)
    url = 'https://e.coronawarn.app?v=1#' + encoded.decode('ascii')

    return url


def generateQrCode(eventDescription: CwaEventDescription) -> qrcode.QRCode:
    qr = qrcode.QRCode()
    qr.add_data(generateUrl(eventDescription))
    qr.make(fit=True)

    return qr
