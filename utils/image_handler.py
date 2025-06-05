from PIL import Image
import io

def image_to_bytes(image):
    with io.BytesIO() as output:
        image.save(output, format='PNG')
        data = output.getvalue()
    return data

def bytes_to_image(byte_data):
    return Image.open(io.BytesIO(byte_data))
