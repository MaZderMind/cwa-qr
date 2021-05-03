import io
from datetime import datetime, timedelta, timezone

import qrcode

from . import cwa

full_event_description = cwa.CwaEventDescription()
full_event_description.location_description = 'Zuhause'
full_event_description.location_address = 'Gau-Odernheim'
full_event_description.start_date_time = datetime.now(timezone.utc)
full_event_description.end_date_time = datetime.now(timezone.utc) + timedelta(days=2)
full_event_description.location_type = cwa.CwaLocation.permanent_workplace
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


def test_matches_code_generated_by_app():
    from_app = "https://e.coronawarn.app?v=1#" \
               "CAESJAgBEglLaW5vYWJlbmQaCUltIEtlbGxlciiQ2MCEBjDArMGEBhp2CAESYIMCzMxNed7UMADn9jGaFF1381k3ZUqX0vfYmX35" \
               "nJsThvZ40iuEU4phThcA4erdE8sPF0dNboA2I7bisI47iuPTofNxVnLel6Xnz4vUpI8b78-d4vYGjJlBHPeqW7aGgBoQ_85sw48P" \
               "riq3uzwjcOzBdiIHCAEQCRi0AQ"

    e = cwa.CwaEventDescription()
    e.location_description = 'Kinoabend'
    e.location_address = 'Im Keller'

    timezone_offset = timezone(timedelta(hours=2))
    e.start_date_time = datetime(2021, 5, 3, 19, 0, 0, tzinfo=timezone_offset).astimezone(timezone.utc)
    e.end_date_time = datetime(2021, 5, 3, 22, 0, 0, tzinfo=timezone_offset).astimezone(timezone.utc)
    e.location_type = cwa.CwaLocation.temporary_cultural_event
    e.default_check_in_length_in_minutes = 3 * 60

    e.seed = b'\xff\xcel\xc3\x8f\x0f\xae*\xb7\xbb<#p\xec\xc1v'

    from_lib = cwa.generate_url(e)
    assert from_lib == from_app


def test_location_enum():
    # from String
    assert cwa.CwaLocation['permanent_workplace'] == cwa.lowlevel.LOCATION_TYPE_PERMANENT_WORKPLACE

    # from Int
    assert cwa.CwaLocation(cwa.lowlevel.LOCATION_TYPE_PERMANENT_WORKPLACE) == cwa.CwaLocation.permanent_workplace

    # to String
    assert cwa.CwaLocation.permanent_workplace.name == 'permanent_workplace'

    # iteration
    for location in cwa.CwaLocation:
        assert cwa.CwaLocation[location.name] == location

    # counting
    assert len(cwa.CwaLocation) == 13
