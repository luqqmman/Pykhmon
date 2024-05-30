import qrcode

def generate_qr(login_address, hot_user, hot_password, save_path):
    url = f"http://{login_address}/login?username={hot_user}&password={hot_password}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img.save(save_path)
