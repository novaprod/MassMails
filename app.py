import os
import smtplib
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, FileField, MultipleFileField
from wtforms.validators import DataRequired, Email, Optional, ValidationError
from datetime import datetime
import re
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'  


UPLOAD_FOLDER_CSV = os.path.join('static', 'uploads', 'csv')
UPLOAD_FOLDER_ATTACHMENTS = os.path.join('static', 'uploads', 'attachments')
LOGS_FOLDER = os.path.join('logs')
os.makedirs(UPLOAD_FOLDER_CSV, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_ATTACHMENTS, exist_ok=True)
os.makedirs(LOGS_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER_CSV'] = UPLOAD_FOLDER_CSV
app.config['UPLOAD_FOLDER_ATTACHMENTS'] = UPLOAD_FOLDER_ATTACHMENTS
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


GMAIL_ACCOUNTS_CSV = os.path.join('static', 'uploads', 'gmail_accounts.csv')


if not os.path.exists(GMAIL_ACCOUNTS_CSV):
    
    df_accounts = pd.DataFrame(columns=['email', 'password', 'sent_today', 'last_sent_date'])
    df_accounts.to_csv(GMAIL_ACCOUNTS_CSV, index=False)


class EmailForm(FlaskForm):
    subject = StringField('Oggetto', validators=[DataRequired()])
    body = TextAreaField('Corpo del Messaggio', validators=[DataRequired()])
    csv_file = FileField('File CSV', validators=[Optional()])
    attachments = MultipleFileField('Allegati')
    html = BooleanField('Invia come HTML')
    manual_emails = TextAreaField('Email Manuali', validators=[Optional()])  

    def validate(self, *args, **kwargs):
        
        if not super(EmailForm, self).validate(*args, **kwargs):
            return False

        
        if not self.csv_file.data and not self.manual_emails.data.strip():
            self.csv_file.errors.append('Devi fornire un file CSV o inserire email manualmente.')
            self.manual_emails.errors.append('Devi fornire un file CSV o inserire email manualmente.')
            return False

        return True


def load_gmail_accounts():
    df = pd.read_csv(GMAIL_ACCOUNTS_CSV)
    today_str = datetime.now().strftime('%Y-%m-%d')
    
    df['sent_today'] = df.apply(lambda row: 0 if row['last_sent_date'] != today_str else row['sent_today'], axis=1)
    df['last_sent_date'] = today_str
    df.to_csv(GMAIL_ACCOUNTS_CSV, index=False)
    return df

def save_gmail_accounts(df):
    df.to_csv(GMAIL_ACCOUNTS_CSV, index=False)


def get_available_account(df, email_limit):
    for idx, row in df.iterrows():
        if row['sent_today'] < email_limit:
            return idx, row
    return None, None


@app.route('/', methods=['GET', 'POST'])
def index():
    form = EmailForm()
    if form.validate_on_submit():
        logger.info("Ricevuta richiesta di invio email.")
        subject = form.subject.data
        body = form.body.data
        html = form.html.data
        csv_file = form.csv_file.data
        attachments = form.attachments.data
        manual_emails = form.manual_emails.data  

        
        recipients = []
        if csv_file:
            csv_filename = secure_filename(csv_file.filename)
            csv_path = os.path.join(app.config['UPLOAD_FOLDER_CSV'], csv_filename)
            csv_file.save(csv_path)

            
            try:
                df_recipients = pd.read_csv(csv_path)
                if 'email' not in df_recipients.columns:
                    flash("Il file CSV deve contenere una colonna 'email'.", 'danger')
                    return redirect(request.url)
                csv_recipients = df_recipients['email'].dropna().unique().tolist()
                recipients.extend(csv_recipients)
            except Exception as e:
                flash(f"Errore nella lettura del file CSV: {e}", 'danger')
                logger.error(f"Errore nella lettura del file CSV: {e}")
                return redirect(request.url)

        
        manual_recipients = []
        if manual_emails:
            
            manual_recipients = [email.strip() for email in manual_emails.split('\n') if email.strip()]
            
            
            email_regex = r"[^@]+@[^@]+\.[^@]+"
            invalid_emails = [email for email in manual_recipients if not re.match(email_regex, email)]
            if invalid_emails:
                flash(f"Alcuni indirizzi email manuali non sono validi: {', '.join(invalid_emails)}", 'danger')
                logger.warning(f"Email non valide inserite manualmente: {invalid_emails}")
                return redirect(request.url)

            recipients.extend(manual_recipients)

        
        recipients = list(set(recipients))

        if not recipients:
            flash("Nessun destinatario trovato.", 'danger')
            logger.warning("Nessun destinatario trovato dopo la validazione.")
            return redirect(request.url)

        
        df_accounts = load_gmail_accounts()
        if df_accounts.empty:
            flash("Nessun account Gmail disponibile. Aggiungi almeno un account per inviare email.", 'danger')
            logger.error("Nessun account Gmail disponibile per l'invio.")
            return redirect(request.url)

        
        
        global current_email_limit
        if 'current_email_limit' not in globals():
            current_email_limit = 500  
        email_limit = current_email_limit

        
        log_messages = []
        sent_count = 0
        failed_count = 0

        
        for recipient in recipients:
            
            idx, account = get_available_account(df_accounts, email_limit)
            if account is None:
                log_messages.append("Tutti gli account Gmail hanno raggiunto il limite di invio giornaliero.")
                flash("Tutti gli account Gmail hanno raggiunto il limite di invio giornaliero.", 'danger')
                logger.warning("Tutti gli account Gmail hanno raggiunto il limite giornaliero.")
                break

            
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            try:
                server.login(account['email'], account['password'])
            except Exception as e:
                log_messages.append(f"❌ Errore di login SMTP per {account['email']}: {e}")
                logger.error(f"Errore di login SMTP per {account['email']}: {e}")
                failed_count += 1
                
                df_accounts.at[idx, 'sent_today'] = email_limit  
                save_gmail_accounts(df_accounts)
                continue

            
            msg = MIMEMultipart()
            msg['From'] = account['email']
            msg['To'] = recipient
            msg['Subject'] = subject
            if html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))

            
            for file in attachments:
                if file:
                    try:
                        filename = secure_filename(file.filename)
                        file_path = os.path.join(app.config['UPLOAD_FOLDER_ATTACHMENTS'], filename)
                        file.save(file_path)

                        part = MIMEBase('application', 'octet-stream')
                        with open(file_path, 'rb') as attachment_file:
                            part.set_payload(attachment_file.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {filename}',
                        )
                        msg.attach(part)
                    except Exception as e:
                        log_messages.append(f"❌ Errore nell'allegare {filename}: {e}")
                        logger.error(f"Errore nell'allegare {filename}: {e}")

            
            try:
                server.send_message(msg)
                log_messages.append(f"✅ Email inviata a {recipient} tramite {account['email']}")
                logger.info(f"Email inviata a {recipient} tramite {account['email']}")
                sent_count += 1
                
                df_accounts.at[idx, 'sent_today'] += 1
                save_gmail_accounts(df_accounts)
            except Exception as e:
                log_messages.append(f"❌ Errore nell'invio a {recipient}: {e}")
                logger.error(f"Errore nell'invio a {recipient}: {e}")
                failed_count += 1
            finally:
                server.quit()

        
        log_filename = f"log_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.txt"
        log_path = os.path.join(LOGS_FOLDER, log_filename)
        with open(log_path, 'w', encoding='utf-8') as log_file:
            for message in log_messages:
                log_file.write(message + '\n')

        flash(f"✅ Invio completato: {sent_count} inviati, {failed_count} falliti.", 'success')
        logger.info(f"Invio completato: {sent_count} inviati, {failed_count} falliti.")
        return redirect(url_for('log_view', log_filename=log_filename))

    return render_template('index.html', form=form)


@app.route('/log/<log_filename>')
def log_view(log_filename):
    log_file_path = os.path.join(LOGS_FOLDER, log_filename)
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r', encoding='utf-8') as file:
            log_content = file.read()
        return render_template('log_view.html', log_content=log_content, log_filename=log_filename)
    else:
        flash("Log non trovato.", 'danger')
        logger.warning(f"Log non trovato: {log_filename}")
        return redirect(url_for('index'))


@app.route('/update_email_limit', methods=['POST'])
def update_email_limit():
    global current_email_limit
    data = request.get_json()
    new_limit = data.get('max_limit')
    if isinstance(new_limit, int) and new_limit > 0:
        current_email_limit = new_limit
        logger.info(f"Limite massimo aggiornato a {current_email_limit}.")
        return jsonify({'status': 'success', 'message': 'Limite massimo aggiornato correttamente.'})
    else:
        logger.warning(f"Tentativo di aggiornare il limite con valore non valido: {new_limit}")
        return jsonify({'status': 'error', 'message': 'Valore non valido per il limite massimo.'}), 400


@app.route('/get_accounts', methods=['GET'])
def get_accounts():
    try:
        df = pd.read_csv(GMAIL_ACCOUNTS_CSV)
        accounts = df[['email', 'sent_today', 'last_sent_date']].to_dict(orient='records')
        return jsonify({'status': 'success', 'accounts': accounts})
    except Exception as e:
        logger.error(f"Errore nel recupero degli account: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/add_account', methods=['POST'])
def add_account():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        logger.warning("Tentativo di aggiungere un account senza email o password.")
        return jsonify({'status': 'error', 'message': 'Email e password sono obbligatorie.'}), 400

    
    try:
        df = pd.read_csv(GMAIL_ACCOUNTS_CSV)
        if email in df['email'].values:
            logger.warning(f"Tentativo di aggiungere un account già esistente: {email}")
            return jsonify({'status': 'error', 'message': 'Questo account è già presente.'}), 400
        new_account = {'email': email, 'password': password, 'sent_today': 0, 'last_sent_date': datetime.now().strftime('%Y-%m-%d')}
        df = pd.concat([df, pd.DataFrame([new_account])], ignore_index=True)
        df.to_csv(GMAIL_ACCOUNTS_CSV, index=False)
        logger.info(f"Account aggiunto correttamente: {email}")
        return jsonify({'status': 'success', 'message': 'Account aggiunto correttamente.'})
    except Exception as e:
        logger.error(f"Errore nell'aggiunta dell'account {email}: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/delete_account', methods=['POST'])
def delete_account():
    data = request.get_json()
    email = data.get('email')

    if not email:
        logger.warning("Tentativo di rimuovere un account senza email.")
        return jsonify({'status': 'error', 'message': 'Email è obbligatoria.'}), 400

    try:
        df = pd.read_csv(GMAIL_ACCOUNTS_CSV)
        if email not in df['email'].values:
            logger.warning(f"Tentativo di rimuovere un account inesistente: {email}")
            return jsonify({'status': 'error', 'message': 'Account non trovato.'}), 404
        df = df[df['email'] != email]
        df.to_csv(GMAIL_ACCOUNTS_CSV, index=False)
        logger.info(f"Account rimosso correttamente: {email}")
        return jsonify({'status': 'success', 'message': 'Account rimosso correttamente.'})
    except Exception as e:
        logger.error(f"Errore nella rimozione dell'account {email}: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/list_logs', methods=['GET'])
def list_logs():
    try:
        logs = sorted(os.listdir(LOGS_FOLDER), reverse=True)  
        return jsonify({'status': 'success', 'logs': logs})
    except Exception as e:
        logger.error(f"Errore nell'elenco dei log: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/reset_sent_counts', methods=['POST'])
def reset_sent_counts():
    try:
        df = pd.read_csv(GMAIL_ACCOUNTS_CSV)
        df['sent_today'] = 0
        df.to_csv(GMAIL_ACCOUNTS_CSV, index=False)
        logger.info("Contatori delle email giornaliere resettati correttamente.")
        return jsonify({'status': 'success', 'message': 'Contatori delle email giornaliere resettati correttamente.'})
    except Exception as e:
        logger.error(f"Errore nel resettare i contatori delle email giornaliere: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)