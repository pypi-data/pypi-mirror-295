# hotmail_flask_mailer/app.py
from flask import Flask, request, jsonify
from mailer import Mailer

app = Flask(__name__)

class FlaskMailer:
    def __init__(self):
        self.email = None
        self.password = None
        self.mail = None

    def save(self, email, password):
        """Save email credentials."""
        self.email = email
        self.password = password
        self.mail = Mailer(email=self.email, password=self.password)
        self.mail.settings(provider=self.mail.MICROSOFT)

    def send(self, receiver, subject, message):
        """Send an email using the saved credentials."""
        if not self.mail:
            raise ValueError("Email credentials not saved. Call save() first.")
        self.mail.send(receiver=receiver, subject=subject, message=message)
        return self.mail.status


mailer_instance = FlaskMailer()

@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    receiver = data.get('receiver')
    subject = data.get('subject')
    message = data.get('message')

    if not all([email, password, receiver, subject, message]):
        return jsonify({'error': 'Email, password, receiver, subject, and message are required'}), 400

    # Save the email credentials
    mailer_instance.save(email, password)

    # Send the email
    status = mailer_instance.send(receiver, subject, message)

    if status:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)
