import cv2
import numpy as np
import qrcode
import argparse
from pyzbar.pyzbar import decode

# Generate a QR code from the string
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
    
    # Resize the QR code to match the size of the logo (if needed)
    img_qr = img_qr.resize((size, size))
    qr_array = np.array(img_qr, dtype=np.uint8)
    
    return qr_array

# Embed the QR code using the least significant bits (LSB) method
def embed_qr_in_logo(img, qr_img):
    print(f"Before shape: {img}")
    h, w, _ = img.shape
    qr_h, qr_w = qr_img.shape
    
    if qr_h > h or qr_w > w:
        raise ValueError("QR code is too large to fit in the image")
    
    # Embed QR code in the LSB of the blue channel of the image
    for i in range(qr_h):
        for j in range(qr_w):
            # Only embed into the blue channel to keep the overall color unchanged
            pixel = img[i, j, 0]  # Get the blue channel
            qr_bit = qr_img[i, j] // 255  # Convert the QR pixel to a binary bit (0 or 1)
            img[i, j, 0] = (pixel & 0xFE) | qr_bit  # Modify only the least significant bit

    return img

# Extract QR code from the image (decoding process)
def extract_qr_from_logo(img, size):
    qr_img = np.zeros((size, size), dtype=np.uint8)
    
    for i in range(size):
        for j in range(size):
            pixel = img[i, j, 0]  # Get the blue channel
            qr_bit = pixel & 0x1  # Extract the least significant bit
            qr_img[i, j] = 255 * qr_bit  # Scale to full black/white (0 or 255)
    
    return qr_img

def decode_qr_code(image_path):
    img = cv2.imread(image_path)
    decoded_objects = decode(img)

    for obj in decoded_objects:
        # obj.data contains the message as bytes
        print("Decoded QR Code Message:", obj.data.decode('utf-8')) 

def main(wm="9876-0954-4545-45", image="input.jpg", mode="encode"):
    img = cv2.imread(image)
    h, w, _ = img.shape

    # Define output filename with PNG extension
    output = "output.png"

    if mode == "encode":
        # Create QR code from the watermark text, with size matching the logo
        qr_code = create_qr_code(wm, min(h, w))

        # Embed the QR code invisibly into the logo using LSB steganography
        img_with_qr = embed_qr_in_logo(img, qr_code)
        
        # Save the output image as PNG
        cv2.imwrite(output, img_with_qr)
        print(f"QR code hidden and saved to {output}")

    elif mode == "decode":
        # Extract the hidden QR code from the image
        qr_extracted = extract_qr_from_logo(img, min(h, w))
        
        # Save the extracted QR code image as PNG
        cv2.imwrite(output, qr_extracted)
        print(f"Hidden QR code extracted and saved to {output}")
        decode_qr_code(output)

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--wm', type=str, default='9876-0954-4545-45')
    parser.add_argument('--image', type=str, default='input.jpg')
    parser.add_argument('--mode', type=str, default='encode', help="encode or decode")
    opt = parser.parse_args()
    return opt

if __name__ == '__main__':
    opt = parse_opt()
    main(**vars(opt))
