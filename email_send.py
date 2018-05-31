import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def send_email(to, img_file):
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'Ticket Details'
    # msgRoot['From'] = <sender_email>

    # Create the body of the message.
    html = """\
        <p>Hello,</p>
        <p> Attached below is the qr code for the ticket </p>
        <p>
            <img src="cid:image1">
        </p>
    """

    # Record the MIME types.
    msgHtml = MIMEText(html, 'html')
    img = open(img_file, 'rb').read()

    msgImg = MIMEImage(img, 'png')
    msgImg.add_header('Content-ID', '<image1>')
    msgImg.add_header('Content-Disposition', 'inline', filename=img_file)

    msgRoot.attach(msgHtml)
    msgRoot.attach(msgImg)
    smtp = smtplib.SMTP('smtp.gmail.com: 587')
    smtp.starttls()
    # smtp.login(<sneder_email>, <sneder_pass>)
    # smtp.sendmail(<sender_email>, to, msgRoot.as_string())
    smtp.quit()
