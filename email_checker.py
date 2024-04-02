from flask import Flask, render_template, request
import csv

app = Flask(__name__)

# Function to check if an email is spam
def check_spam(email, allowed_domains):
    domain = email.split('@')[-1]
    if domain in allowed_domains:
        return False  # Not a spam email
    else:
        return True   # Spam email

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    spam_emails = []
    allowed_domains = set()
    with open('domains.txt', 'r') as f:
        allowed_domains = set(f.read().splitlines())

    if 'file' in request.files:
        csv_file = request.files['file']
        if csv_file.filename != '':
            # Read the CSV file as text
            csv_text = csv_file.stream.read().decode('utf-8')
            # Create a CSV reader from the text
            reader = csv.reader(csv_text.splitlines())
            next(reader)  # Skip header
            for row in reader:
                email = row[0]
                if check_spam(email, allowed_domains):
                    spam_emails.append(email)

    return render_template('index.html', spam_emails=spam_emails, total_spam=len(spam_emails))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
