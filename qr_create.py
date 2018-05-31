import pyqrcode


def create_qrcode(id):
    qr = pyqrcode.create(id)
    qr.png(('QRCodes/' +id+'.png'), scale=6)