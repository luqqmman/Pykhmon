from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import qrcode
import os


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




def create_voucher_pdf(vouchers, qr_path, pdf_path):
    template_path = 'dashboard/static/voucher_template/neetnoox.png'
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    margin = 10 * mm
    qr_size = 30 * mm
    ad_height = 20 * mm
    title_height = 10 * mm
    box_height = qr_size + title_height + ad_height + (2 * margin)
    box_width = (width - 3 * margin) / 2
    x_positions = [margin, margin + box_width + margin]
    y_position = height - margin - box_height
    num_vouchers = len(vouchers)
    vouchers_per_page = 6  # 3 rows x 2 columns

    for i, voucher in enumerate(vouchers):
        if i % vouchers_per_page == 0 and i > 0:
            c.showPage()
            y_position = height - margin - box_height

        col = (i % vouchers_per_page) % 2
        row = (i % vouchers_per_page) // 2

        x_position = x_positions[col]
        y_position = height - margin - box_height - (row * (box_height + margin))

        # Draw border around the voucher box
        c.drawImage(template_path, x_position, y_position, width=box_width, height=box_height)
        c.rect(x_position, y_position, box_width, box_height)

        # Draw title
        # c.drawString(x_position + margin, y_position + box_height - title_height, f"Voucher")

        # Draw username, password, and profile
        c.setFont("Courier", 9)
        c.drawString(x_position + margin + qr_size + 0.5*margin, y_position + 0.5*box_height + 30, f"username: {voucher['username']}")
        c.drawString(x_position + margin + qr_size + 0.5*margin, y_position + 0.5*box_height + 10, f"password: {voucher['password']}")
        c.drawString(x_position + margin + qr_size + 0.5*margin, y_position + 0.5*box_height - 10, f"profile: {voucher['profile']}")

        # Draw QR code with border
        qr_x = x_position + margin
        qr_y = y_position + margin + ad_height
        c.rect(qr_x, qr_y, qr_size, qr_size)
        img_path = os.path.join(qr_path, f"{voucher['username']}.png")
        c.drawImage(img_path, qr_x, qr_y, width=qr_size, height=qr_size)

        # Draw ad space as a rectangle
        ad_x = x_position + margin
        ad_y = y_position + margin
        # c.rect(ad_x, ad_y, box_width - 2 * margin, 0.75*ad_height)
        # c.drawString(ad_x + 2 * mm, ad_y + 6 * mm, "Ad space")

    c.save()
    return pdf_path
