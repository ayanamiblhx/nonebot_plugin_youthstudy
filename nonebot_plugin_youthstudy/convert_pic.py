from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import base64
from os.path import dirname

font_path = dirname(__file__) + '/resource/font/font.otf'
icon_path = dirname(__file__) + '/resource/bac/bac.png'


def size(size: int) -> ImageFont:
    return ImageFont.truetype(font_path, size)


async def convert_pic(text):
    img = Image.new('RGB', (902, 987), (255, 255, 255))
    icon = Image.open(icon_path)
    img.paste(icon, (0, 0))
    draw = ImageDraw.Draw(img)
    title = ""
    period = ""
    for i in text["title"]:
        title += i + f"\n"
    for i in text["period"]:
        period += i + f"\n"
    draw.multiline_text((10, 10), title, fill='gold', font=size(55))
    draw.multiline_text((100, 80), period, fill='gold', font=size(50))
    draw.multiline_text((250, 40), text["answer"], fill='gold', font=size(40))
    draw.multiline_text((250, 700), text["end_time"], fill='gold', font=size(40))
    buf = BytesIO()
    img.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    return "base64://" + base64_str
