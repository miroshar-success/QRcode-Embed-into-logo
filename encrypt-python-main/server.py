from flask import Flask, request, jsonify, send_file
import cv2
import numpy as np
import qrcode
from io import BytesIO
from PIL import Image
from pyzbar.pyzbar import decode as pyzbar_decode

app = Flask(__name__)

def create_qr_code(data, size):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img_qr = qr.make_image(fill='black', back_color='white').convert('L')
    img_qr = img_qr.resize((size, size))
    qr_array = np.array(img_qr, dtype=np.uint8)
    return qr_array

def embed_qr_in_logo(img, qr_img):
    h, w, _ = img.shape
    qr_h, qr_w = qr_img.shape
    if qr_h > h or qr_w > w:
        raise ValueError("QR code is too large to fit in the image")
    for i in range(qr_h):
        for j in range(qr_w):
            pixel = img[i, j, 0]
            qr_bit = qr_img[i, j] // 255
            img[i, j, 0] = (pixel & 0xFE) | qr_bit
    return img

def extract_qr_from_logo(img, size):

    qr_img = np.zeros((size, size), dtype=np.uint8)
    for i in range(size):
        for j in range(size):
            pixel = img[i, j, 0]
            qr_bit = pixel & 0x1
            qr_img[i, j] = 255 * qr_bit
    
    return qr_img

def decode_qr_code(image):
    image = Image.fromarray(image)
    image = image.convert('RGB')  
    
    decoded_objects = pyzbar_decode(image)
    
    decoded_message = None
    for obj in decoded_objects:
        decoded_message = obj.data.decode('utf-8')
        break  
    
    return decoded_message

@app.route('/encode', methods=['POST'])
def encode():
    data = request.form['message']
    
    img_file = request.files['image'].read()
    
    img_array = np.frombuffer(img_file, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    qr_img = create_qr_code(data, min(img.shape[:2]))
    img_with_qr = embed_qr_in_logo(img, qr_img)
    _, buffer = cv2.imencode('.png', img_with_qr)
    io_buf = BytesIO(buffer)
    return send_file(io_buf, mimetype='image/png', as_attachment=True, download_name='encoded_image.png')


@app.route('/decode', methods=['POST'])
def decode():
    img_file = request.files['image'].read()
    img_array = np.frombuffer(img_file, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    qr_img = extract_qr_from_logo(img, min(img.shape[:2]))
    decoded_message = decode_qr_code(qr_img)

    return jsonify({'message': decoded_message})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)