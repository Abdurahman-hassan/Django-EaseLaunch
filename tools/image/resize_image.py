import random
import string
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


def generate():
    characters = string.ascii_letters + string.digits + "{0:9}"
    name = "".join(random.choice(characters) for _ in range(20))
    return name


def exif_transpose(img):
    exif_orientation_tag = 274
    if hasattr(img, "_getexif"):
        exif_data = img._getexif()
        if exif_data is not None:
            orientation = exif_data.get(exif_orientation_tag, 1)
            orientation_transpose_map = {
                2: Image.FLIP_LEFT_RIGHT,
                3: Image.ROTATE_180,
                4: Image.FLIP_TOP_BOTTOM,
                5: Image.TRANSPOSE,
                6: Image.ROTATE_270,
                7: Image.TRANSVERSE,
                8: Image.ROTATE_90,
            }
            if orientation in orientation_transpose_map:
                img = img.transpose(orientation_transpose_map[orientation])
    return img


def ReSizeImages(avatar, w, h):
    image = Image.open(avatar)

    image = exif_transpose(image)

    size_avatar = (w, h)
    avatar_new_size = image.resize(size_avatar)
    image.close()
    avatar_new = BytesIO()
    avatar_new_size.save(avatar_new, format="PNG")
    avatar_new.seek(0)
    namefile = generate() + ".png"
    return InMemoryUploadedFile(
        avatar_new, None, namefile, "image/png", len(avatar_new.getvalue()), None
    )
