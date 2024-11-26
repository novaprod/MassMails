import os
import sys
import subprocess
import threading
import json
import webbrowser
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import pandas as pd
import re
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, FileField, MultipleFileField
from wtforms.validators import DataRequired, Optional
from PIL import Image, ImageTk
import customtkinter as ctk

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

current_email_limit = 500

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
def update_email_limit_route():
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
def get_accounts_route():
    try:
        df = pd.read_csv(GMAIL_ACCOUNTS_CSV)
        accounts = df[['email', 'sent_today', 'last_sent_date']].to_dict(orient='records')
        return jsonify({'status': 'success', 'accounts': accounts})
    except Exception as e:
        logger.error(f"Errore nel recupero degli account: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/add_account', methods=['POST'])
def add_account_route():
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
def delete_account_route():
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
def list_logs_route():
    try:
        logs = sorted(os.listdir(LOGS_FOLDER), reverse=True)  
        return jsonify({'status': 'success', 'logs': logs})
    except Exception as e:
        logger.error(f"Errore nell'elenco dei log: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/reset_sent_counts', methods=['POST'])
def reset_sent_counts_route():
    try:
        df = pd.read_csv(GMAIL_ACCOUNTS_CSV)
        df['sent_today'] = 0
        df.to_csv(GMAIL_ACCOUNTS_CSV, index=False)
        logger.info("Contatori delle email giornaliere resettati correttamente.")
        return jsonify({'status': 'success', 'message': 'Contatori delle email giornaliere resettati correttamente.'})
    except Exception as e:
        logger.error(f"Errore nel resettare i contatori delle email giornaliere: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

class ModernFlaskLauncher:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Launcher MailSender")
        self.root.geometry("900x650")
        self.root.minsize(800, 600)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.server_thread = None
        self.is_server_running = False
        
        self.load_config()
        self.create_widgets()
        
        self.root.bind("<Configure>", self.on_window_resize)
        
    def load_config(self):
        default_config = {
            'theme': 'dark',
            'port': 5000,
            'last_access': None,
            'auto_launch_browser': True
        }
        
        try:
            with open('launcher_config.json', 'r') as f:
                loaded_config = json.load(f)
                self.config = {**default_config, **loaded_config}
        except FileNotFoundError:
            self.config = default_config
            self.save_config()
            
    def save_config(self):
        self.config['last_access'] = datetime.now().isoformat()
        with open('launcher_config.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def create_widgets(self):
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.header = ctk.CTkFrame(
            self.root, 
            height=70, 
            corner_radius=0,
            fg_color=("gray85", "gray20")
        )
        self.header.grid(row=0, column=0, sticky="nsew")
        self.create_header()
        
        self.main_content = ctk.CTkFrame(
            self.root,
            fg_color=("gray95", "gray10")
        )
        self.main_content.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.create_main_content()
        
        self.create_footer()
        
    def create_header(self):
        self.header.grid_columnconfigure(1, weight=1)
        
        title_frame = ctk.CTkFrame(
            self.header,
            fg_color="transparent"
        )
        title_frame.grid(row=0, column=0, padx=20, pady=10)
        
        self.title_label = ctk.CTkLabel(
            title_frame,
            text="Flask Dashboard",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("gray15", "gray90")
        )
        self.title_label.pack()
        
        subtitle = ctk.CTkLabel(
            title_frame,
            text="MassMailSender V 1.0.0",
            font=ctk.CTkFont(size=14),
            text_color=("gray45", "gray60")
        )
        subtitle.pack()
        
        controls_frame = ctk.CTkFrame(
            self.header,
            fg_color="transparent"
        )
        controls_frame.grid(row=0, column=2, padx=20)
        
        self.appearance_mode_menu = ctk.CTkSegmentedButton(
            controls_frame,
            values=["Scuro", "Chiaro"],
            command=self.change_appearance_mode,
            width=150
        )
        self.appearance_mode_menu.set("Scuro" if self.config.get('theme') == 'dark' else "Chiaro")
        self.appearance_mode_menu.pack(pady=5)
        
    def create_main_content(self):
        self.control_frame = ctk.CTkFrame(
            self.main_content,
            fg_color="transparent"
        )
        self.control_frame.pack(fill="x", pady=(0, 20))
        
        self.control_frame.grid_columnconfigure(0, weight=1)
        self.control_frame.grid_rowconfigure(0, weight=0)
        self.control_frame.grid_rowconfigure(1, weight=0)
        self.control_frame.grid_rowconfigure(2, weight=0)
        
        button_frame = ctk.CTkFrame(
            self.control_frame,
            fg_color="transparent"
        )
        button_frame.grid(row=0, column=0, pady=10)
        
        self.start_button = ctk.CTkButton(
            button_frame,
            text="Avvia Server",
            font=ctk.CTkFont(size=15, weight="bold"),
            width=180,
            height=40,
            corner_radius=8,
            fg_color=("#2196F3", "#1976D2"),
            hover_color=("#1E88E5", "#1565C0"),
            command=self.start_server
        )
        self.start_button.pack(side="left", padx=10)
        
        self.stop_button = ctk.CTkButton(
            button_frame,
            text="Ferma Server",
            font=ctk.CTkFont(size=15, weight="bold"),
            width=180,
            height=40,
            corner_radius=8,
            fg_color=("#F44336", "#D32F2F"),
            hover_color=("#E53935", "#C62828"),
            command=self.stop_server,
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=10)
        
        self.status_label = ctk.CTkLabel(
            self.control_frame,
            text="◉ Server Spento",
            font=ctk.CTkFont(size=15),
            text_color=("#E57373", "#EF5350")
        )
        self.status_label.grid(row=1, column=0, pady=(10, 0))
        
        separator = ctk.CTkFrame(
            self.main_content,
            height=2,
            fg_color=("gray75", "gray30")
        )
        separator.pack(fill="x", pady=15)
        
        console_frame = ctk.CTkFrame(
            self.main_content,
            fg_color=("gray90", "gray15")
        )
        console_frame.pack(fill="both", expand=True)
        
        console_header = ctk.CTkFrame(
            console_frame,
            fg_color="transparent"
        )
        console_header.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            console_header,
            text="Log Console",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("gray20", "gray80")
        ).pack(side="left")
        
        self.clear_console_btn = ctk.CTkButton(
            console_header,
            text="Pulisci Log",
            font=ctk.CTkFont(size=13),
            width=100,
            height=28,
            command=self.clear_console
        )
        self.clear_console_btn.pack(side="right")
        
        self.console = ctk.CTkTextbox(
            console_frame,
            font=ctk.CTkFont(family="Consolas", size=13),
            height=250,
            fg_color=("white", "gray17"),
            border_width=1,
            border_color=("gray70", "gray25")
        )
        self.console.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
    def create_footer(self):
        footer = ctk.CTkFrame(
            self.root,
            height=30,
            fg_color=("gray90", "gray15")
        )
        footer.grid(row=2, column=0, sticky="ew")
        
        footer.grid_columnconfigure(1, weight=1)
        
        port_label = ctk.CTkLabel(
            footer,
            text=f"Porta: {self.config.get('port', 5000)}",
            font=ctk.CTkFont(size=12),
            text_color=("gray45", "gray60")
        )
        port_label.grid(row=0, column=0, padx=20, pady=5)
        
        last_access = self.config.get('last_access')
        if last_access:
            try:
                last_access_dt = datetime.fromisoformat(last_access)
                last_access_str = last_access_dt.strftime("%d/%m/%Y %H:%M")
                access_label = ctk.CTkLabel(
                    footer,
                    text=f"Ultimo accesso: {last_access_str}",
                    font=ctk.CTkFont(size=12),
                    text_color=("gray45", "gray60")
                )
                access_label.grid(row=0, column=1, padx=20, pady=5)
            except (ValueError, TypeError):
                pass
    
    def update_status(self, message, is_running=False):
        status_text = f"◉ {message}"
        status_color = ("#66BB6A", "#4CAF50") if is_running else ("#E57373", "#EF5350")
        
        self.status_label.configure(
            text=status_text,
            text_color=status_color
        )
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.insert("end", f"[{timestamp}] {message}\n")
        self.console.see("end")
        
        self.start_button.configure(state="disabled" if is_running else "normal")
        self.stop_button.configure(state="normal" if is_running else "disabled")
        
    def clear_console(self):
        self.console.delete("1.0", "end")
        self.console.insert("end", "Console pulita...\n")

    def start_server(self):
        if self.is_server_running:
            self.show_error("Il server è già in esecuzione!")
            return

        try:
            self.server_thread = threading.Thread(target=self._run_flask_app)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            self.is_server_running = True
            self.update_status(f"Server attivo sulla porta {self.config.get('port', 5000)}", True)
            
            if self.config.get('auto_launch_browser', True):
                self.root.after(1500, lambda: webbrowser.open(f"http://127.0.0.1:{self.config.get('port', 5000)}"))
            
        except Exception as e:
            self.show_error(f"Errore durante l'avvio del server: {str(e)}")

    def _run_flask_app(self):
        try:
            from werkzeug.serving import make_server

            class ServerThread(threading.Thread):
                def __init__(self, app, host, port):
                    threading.Thread.__init__(self)
                    self.srv = make_server(host, port, app)
                    self.ctx = app.app_context()
                    self.ctx.push()

                def run(self):
                    self.srv.serve_forever()

                def shutdown(self):
                    self.srv.shutdown()

            self.flask_server = ServerThread(app, "127.0.0.1", self.config.get('port', 5000))
            self.flask_server.start()

            self.root.after(0, lambda: self.console.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] Server Flask avviato.\n"))
            self.console.see("end")

        except Exception as e:
            self.root.after(0, lambda: self.show_error(f"Errore del server Flask: {str(e)}"))
            self.is_server_running = False
            self.root.after(0, lambda: self.update_status("Server arrestato", False))

    def stop_server(self):
        if not self.is_server_running:
            self.show_error("Il server non è in esecuzione.")
            return

        try:
            self.flask_server.shutdown()
            self.is_server_running = False
            self.update_status("Server arrestato", False)
            self.console.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] Server Flask arrestato.\n")
            self.console.see("end")
        except Exception as e:
            self.show_error(f"Errore durante l'arresto del server: {str(e)}")

    def show_error(self, message):
        dialog = ctk.CTkMessagebox(
            title="Errore",
            message=message,
            icon="cancel",
            button_color=("#F44336", "#D32F2F")
        )
        dialog.mainloop()

    def change_appearance_mode(self, new_appearance_mode):
        mode = "dark" if new_appearance_mode == "Scuro" else "light"
        ctk.set_appearance_mode(mode)
        self.config['theme'] = mode
        self.save_config()

    def on_window_resize(self, event=None):
        if hasattr(self, 'console'):
            window_height = self.root.winfo_height()
            self.console.configure(height=max(250, window_height - 400))

    def run(self):
        if self.config.get('theme') == 'light':
            self.appearance_mode_menu.set("Chiaro")
            ctk.set_appearance_mode("light")
        else:
            self.appearance_mode_menu.set("Scuro")
            ctk.set_appearance_mode("dark")
            
        self.root.mainloop()

if __name__ == "__main__":
    app_thread = threading.Thread(target=lambda: app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False))
    launcher = ModernFlaskLauncher()
    launcher.run()
