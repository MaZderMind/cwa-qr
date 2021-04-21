import base64
import cwa_pb2 as lowlevel
import qrcode
import secrets
from datetime import datetime

PUBLIC_KEY_STR = 'gwLMzE153tQwAOf2MZoUXXfzWTdlSpfS99iZffmcmxOG9njSK4RTimFOFwDh6t0Tyw8XR01ugDYjtuKwjjuK49Oh83FWct6XpefPi9Skjxvvz53i9gaMmUEc96pbtoaA'
PUBLIC_KEY = base64.standard_b64decode(PUBLIC_KEY_STR.encode('ascii'))

class CwaEventDescription(object):
	def __init__(self):
		self.locationDescription = None;
		self.locationAddress = None;
		self.startDateTime = None;
		self.endDateTime = None;
		self.locationType = None
		self.defaultCheckInLengthInMinutes = None

def generatePayload(eventDescription):
	payload = lowlevel.QRCodePayload()
	payload.version = 1

	payload.locationData.version = 1
	payload.locationData.description = eventDescription.locationDescription
	payload.locationData.address = eventDescription.locationAddress
	payload.locationData.startTimestamp = int(eventDescription.startDateTime.timestamp()) if eventDescription.startDateTime else None
	payload.locationData.endTimestamp = int(eventDescription.endDateTime.timestamp()) if eventDescription.endDateTime else None

	payload.crowdNotifierData.version = 1
	payload.crowdNotifierData.publicKey = PUBLIC_KEY
	payload.crowdNotifierData.cryptographicSeed = secrets.token_bytes(16)

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
