from PIL import Image
import qrcode
import numpy as np

# Generate a QR Code from the given URL (9874-5454-4545-45)
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Convert the QR code to an image
    return qr.make_image(fill='black', back_color='white')

# Embed QR code into logo
def embed_qr_in_logo(logo_path, qr_code, output_path):
    # Open the logo
    logo = Image.open(logo_path).convert("RGBA")
    
    # Resize QR code to fit the logo
    qr_code = qr_code.resize(logo.size)

    # Convert both images to numpy arrays
    logo_arr = np.array(logo)
    qr_arr = np.array(qr_code.convert("L"))  # Convert to grayscale

    # Define a threshold to control the visibility
    threshold = 200

    # Encode the QR code into the logo's alpha channel (or slightly adjust pixel values)
    for i in range(logo_arr.shape[0]):
        for j in range(logo_arr.shape[1]):
            if qr_arr[i, j] < threshold:
                # Adjust the pixel's alpha channel to subtly hide the QR code
                logo_arr[i, j, 3] = int(logo_arr[i, j, 3] * 0.9)  # Modify opacity slightly

    # Convert back to image
    result_image = Image.fromarray(logo_arr, "RGBA")

    # Convert to RGB before saving as JPEG (removes alpha)
    result_image = result_image.convert("RGB")
    
    # Save the new logo without the alpha channel as a JPEG
    result_image.save(output_path, "png")

# Input data
qr_data = "9874-5454-4545-45"
logo_path = 'logo.jpg'
output_path = 'output_logo_with_qr.png'

# Generate QR code
qr_code = generate_qr_code(qr_data)

# Embed QR code into the logo
embed_qr_in_logo(logo_path, qr_code, output_path)
