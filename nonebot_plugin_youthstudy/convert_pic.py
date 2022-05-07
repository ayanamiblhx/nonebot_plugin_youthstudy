from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import base64
from os.path import dirname

font_path = dirname(__file__) + '/resource/font/font.otf'
icon_path = dirname(__file__) + '/resource/bac/bac.png'


def size(fontsize: int) -> ImageFont:
    return ImageFont.truetype(font_path, fontsize)


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
    j = 0
    for i in text["answer"]:
        draw.multiline_text((200 + j * 150, 40 if j == 0 else 90), i, fill='gold', font=size(40))
        j += 1
    draw.multiline_text((200, 700), text["end_time"], fill='gold', font=size(40))
    buf = BytesIO()
    img.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    return "base64://" + base64_str
