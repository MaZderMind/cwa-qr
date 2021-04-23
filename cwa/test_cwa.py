import io
from datetime import datetime, timedelta, timezone

import qrcode

from . import cwa

fullEventDescription = cwa.CwaEventDescription()
fullEventDescription.locationDescription = 'Zuhause'
fullEventDescription.locationAddress = 'Gau-Odernheim'
fullEventDescription.startDateTime = datetime.now(timezone.utc)
fullEventDescription.endDateTime = datetime.now(timezone.utc) + timedelta(days=2)
fullEventDescription.locationType = cwa.lowlevel.LOCATION_TYPE_PERMANENT_WORKPLACE
fullEventDescription.defaultCheckInLengthInMinutes = 4 * 60


def test_generate_with_minimal_parameters():
    minimalEventDescription = cwa.CwaEventDescription()
    minimalEventDescription.locationDescription = 'Zuhause'
    minimalEventDescription.locationAddress = 'Gau-Odernheim'
    url = cwa.generateUrl(minimalEventDescription)
    assert url != ''


def test_generate_with_all_parameters():
    url = cwa.generateUrl(fullEventDescription)
    assert url != ''


def test_generate_without_seed_creates_same_results():
    urlA = cwa.generateUrl(fullEventDescription)
    urlB = cwa.generateUrl(fullEventDescription)
    assert urlA == urlB


def test_generate_with_same_seed_creates_same_result():
    fullEventDescription.seed = 'a'
    urlA = cwa.generateUrl(fullEventDescription)
    urlB = cwa.generateUrl(fullEventDescription)
    assert urlA == urlB


def test_generate_with_different_seeds_creates_different_results():
    fullEventDescription.seed = 'a'
    urlA = cwa.generateUrl(fullEventDescription)

    fullEventDescription.seed = 'b'
    urlB = cwa.generateUrl(fullEventDescription)

    assert urlA != urlB


def assert_accepts_seed(seed):
    seedA = cwa.constructSeed(seed)
    seedB = cwa.constructSeed(seed)
    assert len(seedA) == 16
    assert seedA == seedB


def test_accepts_int_seed():
    assert_accepts_seed(42)


def test_accepts_float_seed():
    assert_accepts_seed(3.1415)


def test_accepts_str_seed():
    assert_accepts_seed('foo')


def test_accepts_datetime_seed():
    assert_accepts_seed(datetime(2021, 4, 21, 10, 0))


def test_accepts_bytes_seed():
    assert_accepts_seed(b'\xDE\xAD\xBE\xEF')


def test_accepts_none_seed():
    assert_accepts_seed(None)


def test_generate_url():
    url = cwa.generateUrl(fullEventDescription)
    assert url is not None
    assert isinstance(url, str)


def test_generate_payload_object():
    payload = cwa.generatePayload(fullEventDescription)
    assert payload is not None
    assert isinstance(payload, cwa.lowlevel.QRCodePayload)


def test_generate_qr_code():
    qr = cwa.generateQrCode(fullEventDescription)
    assert qr is not None
    assert isinstance(qr, qrcode.QRCode)


def test_generate_qr_code_png():
    qr = cwa.generateQrCode(fullEventDescription)
    img = qr.make_image(fill_color="black", back_color="white")

    img_bytes = io.BytesIO()
    img.save(img_bytes)

    assert img_bytes.getvalue().startswith(b'\x89PNG\r\n\x1a\n')


def test_generate_qr_code_svg():
    import qrcode.image.svg

    qr = cwa.generateQrCode(fullEventDescription)
    svg = qr.make_image(image_factory=qrcode.image.svg.SvgPathFillImage)

    svg_bytes = io.BytesIO()
    svg.save(svg_bytes)

    assert svg_bytes.getvalue().startswith(b'<?xml')
