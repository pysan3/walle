from PIL import Image
import io


def compressImage(data_img: Image.Image, quality: int = 30):
    out = io.BytesIO()
    data_img.save(out, 'JPEG', quality=quality)
    return out.getvalue()


def compressPNG(data: bytes, quality: int = 30):
    return compressImage(Image.open(io.BytesIO(data)).convert('RGB'), quality)


def compressJPG(data: bytes, quality: int = 30):
    return compressImage(Image.open(io.BytesIO(data)), quality)
