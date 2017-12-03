import qrcode

from web.utils.util import get_config
CON_DICT = get_config()
url = "http://{}:{}".format(CON_DICT.get('WEBSERVER',{}).get("bind", "127.0.0.1"),
                             CON_DICT.get('WEBSERVER',{}).get("port", 8008))

qr = qrcode.QRCode(
    version=2,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=8,
    border=2
)
qr.add_data(url)
qr.make(fit=True)
img = qr.make_image()
image_name = CON_DICT.get('QRNAME',"QR.png")
img.save(image_name)