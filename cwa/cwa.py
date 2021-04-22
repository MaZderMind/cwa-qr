import base64
import qrcode
import os
from datetime import datetime

from . import cwa_pb2 as lowlevel

PUBLIC_KEY_STR = 'gwLMzE153tQwAOf2MZoUXXfzWTdlSpfS99iZffmcmxOG9njSK4RTimFOFwDh6t0Tyw8XR01ugDYjtuKwjjuK49Oh83FWct6XpefPi9Skjxvvz53i9gaMmUEc96pbtoaA'
PUBLIC_KEY = base64.standard_b64decode(PUBLIC_KEY_STR.encode('ascii'))

class CwaEventDescription(object):
	def __init__(self):
		"""Description of the Location, Required, String, max 100 Characters"""
		self.locationDescription = None;

		"""Address of the Location, Required, String, max 100 Characters"""
		self.locationAddress = None;

		"""Start of the Event, Optional, datetime in UTC"""
		self.startDateTime = None;

		"""End of the Event, Optional, datetime in UTC"""
		self.endDateTime = None;

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
		self.locationType = None

		"""Default Checkout-Time im Minutes, Optional"""
		self.defaultCheckInLengthInMinutes = None

		"""Specific Seed, 16 Bytes, Optional, leave Empty if unsure

		To Mitigate [Profiling of Venues](https://github.com/corona-warn-app/cwa-documentation/blob/c0e2829/event_registration.md#profiling-of-venues), each QR-Code contains a 16 Bytes long random Seed Value, that makes each Code even with the same Data unique. This Way a Location can generate a fresh QR-Code each day and avoid the Risk of being tracked.

		But sometimes it is Important to be able to re-generate the exact same Code ie. from a Database or other deterministic Sourcers. If this is important to you, you can specify your own 16-Bytes in the `randomSeed` Parameter of the `CwaEventDescription` Object. You can easily generate it with [`secrets.token_bytes(16)`](https://docs.python.org/3/library/secrets.html#secrets.token_bytes).
		"""
		self.randomSeed = None


def generatePayload(eventDescription):
	payload = lowlevel.QRCodePayload()
	payload.version = 1

	payload.locationData.version = 1
	payload.locationData.description = eventDescription.locationDescription
	payload.locationData.address = eventDescription.locationAddress
	payload.locationData.startTimestamp = int(eventDescription.startDateTime.strftime('%s')) if eventDescription.startDateTime else None
	payload.locationData.endTimestamp = int(eventDescription.endDateTime.strftime('%s')) if eventDescription.endDateTime else None

	payload.crowdNotifierData.version = 1
	payload.crowdNotifierData.publicKey = PUBLIC_KEY
	payload.crowdNotifierData.cryptographicSeed = eventDescription.randomSeed if eventDescription.randomSeed is not None else os.urandom(16)

	cwaLocationData = lowlevel.CWALocationData()
	cwaLocationData.version = 1
	cwaLocationData.type = eventDescription.locationType
	cwaLocationData.defaultCheckInLengthInMinutes = eventDescription.defaultCheckInLengthInMinutes

	payload.countryData = cwaLocationData.SerializeToString()
	return payload

def generateUrl(eventDescription):
	payload = generatePayload(eventDescription)
	serialized = payload.SerializeToString()
	encoded = base64.urlsafe_b64encode(serialized)
	url = 'https://e.coronawarn.app?v=1#' + encoded.decode('ascii')

	return url

def generateQrCode(eventDescription):
	qr = qrcode.QRCode()
	qr.add_data(generateUrl(eventDescription))
	qr.make(fit=True)

	return qr
