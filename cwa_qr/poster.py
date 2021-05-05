import io
import os

from svgutils import transform as svg_utils
import qrcode.image.svg

from cwa_qr import generate_qr_code, CwaEventDescription


class CwaPoster(object):
    POSTER_PORTRAIT = 'portrait'
    POSTER_LANDSCAPE = 'landscape'

    TRANSLATIONS = {
        POSTER_PORTRAIT: {
            'file': 'poster/portrait.svg',
            'x': 80,
            'y': 60,
            'scale': 6
        },
        POSTER_LANDSCAPE: {
            'file': 'poster/landscape.svg',
            'x': 42,
            'y': 120,
            'scale': 4.8
        }
    }


def generate_poster(event_description: CwaEventDescription, template: CwaPoster) -> svg_utils.SVGFigure:
    qr = generate_qr_code(event_description)
    svg = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)
    svg_bytes = io.BytesIO()
    svg.save(svg_bytes)

    poster = svg_utils.fromfile('{}/{}'.format(
        os.path.dirname(os.path.abspath(__file__)),
        CwaPoster.TRANSLATIONS[template]['file']
    ))
    overlay = svg_utils.fromstring(svg_bytes.getvalue().decode('UTF-8')).getroot()
    overlay.moveto(
        CwaPoster.TRANSLATIONS[template]['x'],
        CwaPoster.TRANSLATIONS[template]['y'],
        CwaPoster.TRANSLATIONS[template]['scale']
    )
    poster.append([overlay])
    return poster
