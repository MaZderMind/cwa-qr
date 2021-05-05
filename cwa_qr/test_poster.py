from . import cwa, poster

event_description = cwa.CwaEventDescription()
event_description.location_description = 'Zuhause'
event_description.location_address = 'Gau-Odernheim'


def test_generate_qr_code_with_poster_portrait_svg():
    poster_svg = poster.generate_poster(event_description, poster.CwaPoster.POSTER_PORTRAIT)

    svg_str = poster_svg.to_str()
    assert_poster_svg(svg_str)


def test_generate_qr_code_with_poster_landscape_svg():
    poster_svg = poster.generate_poster(event_description, poster.CwaPoster.POSTER_LANDSCAPE)

    svg_str = poster_svg.to_str()
    assert_poster_svg(svg_str)


def assert_poster_svg(svg_str: bytes):
    assert svg_str.startswith(b'<?xml')
    assert b'id="qr-path"' in svg_str
