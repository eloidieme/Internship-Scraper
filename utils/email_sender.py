import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

SENDER = os.getenv('SENDER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')


class EmailEngine:
    def __init__(self, receiver_email, data):
        self.sender_email = SENDER
        self.password = EMAIL_PASSWORD
        self.receiver_email = receiver_email
        self.subject = "Rapport Quotidien - Stages Finance"
        self.data = data

    def parse_entry(self, entry):
        html_string = f"""\
            <li>
                <p>Titre: "{entry["titre"]}"</p>
                <ul>
                    <li>Date de début: "{entry["debut"]}"</li>
                    <li>Lien: "{entry["lien"]}"</li>
                    <li>Catégorie: "{entry["categorie"]}"</li>
                </ul>
            </li>
        """
        return html_string

    def parse_data(self):
        html_string = """\
            <html>
                <body>
                    <p>Voici votre rapport quotidien de stages en finance:</p>
                    <ul>
        """

        for (key, value) in self.data.items():
            head = f"""<li>
                                <p>{key}</p>
                                <ul>
            """

            if len(value) == 0:
                head += "Pas de nouvelles offres aujourd'hui."

            for dic in value:
                head += self.parse_entry(dic)
            
            head += """\
                            </ul>
                        </li>
            """

            html_string += head 

        html_string += """\
                    </ul>
                    <p>Bonne journée.</p>
                </body>
            </html>
        """

        return html_string

    def create_message(self):
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email
        msg['Subject'] = self.subject
        body = self.parse_data()
        msg.attach(MIMEText(body, 'html'))
        return msg

    def smtp_config(self):
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        return smtplib.SMTP(smtp_server, smtp_port)

    def send_email(self):
        server = self.smtp_config()
        server.starttls()
        # Log in to the email account
        server.login(self.sender_email, self.password)
        # Send the email
        server.sendmail(self.sender_email, self.receiver_email,
                        self.create_message().as_string())
        # Quit the server
        server.quit()
