import io
from datetime import datetime, timedelta, timezone

import qrcode

from . import cwa

full_event_description = cwa.CwaEventDescription()
full_event_description.location_description = 'Zuhause'
full_event_description.location_address = 'Gau-Odernheim'
full_event_description.start_date_time = datetime.now(timezone.utc)
full_event_description.end_date_time = datetime.now(timezone.utc) + timedelta(days=2)
full_event_description.location_type = cwa.lowlevel.LOCATION_TYPE_PERMANENT_WORKPLACE
full_event_description.default_check_in_length_in_minutes = 4 * 60


def test_generate_with_minimal_parameters():
    minimal_event_description = cwa.CwaEventDescription()
    minimal_event_description.location_description = 'Zuhause'
    minimal_event_description.location_address = 'Gau-Odernheim'
    url = cwa.generate_url(minimal_event_description)
    assert url != ''


def test_generate_with_all_parameters():
    url = cwa.generate_url(full_event_description)
    assert url != ''


def test_generate_without_seed_creates_same_results():
    url_a = cwa.generate_url(full_event_description)
    url_b = cwa.generate_url(full_event_description)
    assert url_a == url_b


def test_generate_with_same_seed_creates_same_result():
    full_event_description.seed = 'a'
    url_a = cwa.generate_url(full_event_description)
    url_b = cwa.generate_url(full_event_description)
    assert url_a == url_b


def test_generate_with_different_seeds_creates_different_results():
    full_event_description.seed = 'a'
    url_a = cwa.generate_url(full_event_description)

    full_event_description.seed = 'b'
    url_b = cwa.generate_url(full_event_description)

    assert url_a != url_b


def test_generate_url():
    url = cwa.generate_url(full_event_description)
    assert url is not None
    assert isinstance(url, str)


def test_generate_payload_object():
    payload = cwa.generate_payload(full_event_description)
    assert payload is not None
    assert isinstance(payload, cwa.lowlevel.QRCodePayload)


def test_generate_qr_code():
    qr = cwa.generate_qr_code(full_event_description)
    assert qr is not None
    assert isinstance(qr, qrcode.QRCode)


def test_generate_qr_code_png():
    qr = cwa.generate_qr_code(full_event_description)
    img = qr.make_image(fill_color="black", back_color="white")

    img_bytes = io.BytesIO()
    img.save(img_bytes)

    assert img_bytes.getvalue().startswith(b'\x89PNG\r\n\x1a\n')


def test_generate_qr_code_svg():
    import qrcode.image.svg

    qr = cwa.generate_qr_code(full_event_description)
    svg = qr.make_image(image_factory=qrcode.image.svg.SvgPathFillImage)

    svg_bytes = io.BytesIO()
    svg.save(svg_bytes)

    assert svg_bytes.getvalue().startswith(b'<?xml')
