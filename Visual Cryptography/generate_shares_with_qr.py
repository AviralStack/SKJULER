import cv2
import numpy as np
from PIL import Image
import qrcode
import os

def generate_shares(image_path, out_prefix="share"):

    img = cv2.imread(image_path, 0)
    img = cv2.resize(img, (500, 500))
    _, img_binary = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)

    noise = np.random.randint(0, 2, img_binary.shape) * 255
    share1 = noise.astype(np.uint8)


    share2 = cv2.bitwise_xor(img_binary, share1)

    qr_data = "VC-DEMO-ID-001"
    qr = qrcode.QRCode(border=0)
    qr.add_data(qr_data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("L")


    qr_size = 80
    qr_img = qr_img.resize((qr_size, qr_size), Image.NEAREST)
    qr_np = np.array(qr_img)

    h, w = share1.shape
    x0, y0 = w - qr_size - 10, h - qr_size - 10

    share1_with_qr = share1.copy()
    share2_with_qr = share2.copy()
    orig_with_qr = img_binary.copy()

    share1_with_qr[y0:y0+qr_size, x0:x0+qr_size] = qr_np
    share2_with_qr[y0:y0+qr_size, x0:x0+qr_size] = qr_np
    orig_with_qr[y0:y0+qr_size, x0:x0+qr_size] = qr_np


    os.makedirs("out", exist_ok=True)
    cv2.imwrite("out/share1.png", share1_with_qr)
    cv2.imwrite("out/share2.png", share2_with_qr)
    cv2.imwrite("out/original_reference.png", orig_with_qr)

    print("✔ Saved share1.png and share2.png in /out")

if __name__ == "__main__":
    img = input("Enter image name: ")
    src = img
    if not os.path.exists(src):
        print("❌ ERROR: Put Test1.png next to this script.")
    else:
        generate_shares(src)
