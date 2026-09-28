from PIL import Image


def validate_image(image):

    try:
        img = Image.open(image)

        img.verify()

        return True

    except Exception:
        return False