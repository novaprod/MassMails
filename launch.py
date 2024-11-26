import os
import subprocess
import sys
import webbrowser
from datetime import datetime
import threading
import json
import customtkinter as ctk
from PIL import Image, ImageTk

class ModernFlaskLauncher:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Launcher MailSender")
        self.root.geometry("900x650")
        self.root.minsize(800, 600)
        
        # Configurazione iniziale
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.server_process = None
        self.is_server_running = False
        
        # Caricamento configurazione e creazione UI
        self.load_config()
        self.create_widgets()
        
        # Binding per il ridimensionamento della finestra
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
                # Merge con i valori di default per assicurarsi che tutti i campi esistano
                self.config = {**default_config, **loaded_config}
        except FileNotFoundError:
            self.config = default_config
            self.save_config()
            
    def save_config(self):
        self.config['last_access'] = datetime.now().isoformat()
        with open('launcher_config.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def create_widgets(self):
        # Configurazione del grid layout principale
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Creazione e stile dell'header
        self.header = ctk.CTkFrame(
            self.root, 
            height=70, 
            corner_radius=0,
            fg_color=("gray85", "gray20")
        )
        self.header.grid(row=0, column=0, sticky="nsew")
        self.create_header()
        
        # Contenuto principale
        self.main_content = ctk.CTkFrame(
            self.root,
            fg_color=("gray95", "gray10")
        )
        self.main_content.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.create_main_content()
        
        # Footer con informazioni aggiuntive
        self.create_footer()
        
    def create_header(self):
        self.header.grid_columnconfigure(1, weight=1)
        
        # Logo/Titolo
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
        
        # Controls frame
        controls_frame = ctk.CTkFrame(
            self.header,
            fg_color="transparent"
        )
        controls_frame.grid(row=0, column=2, padx=20)
        
        # Theme switcher
        self.appearance_mode_menu = ctk.CTkSegmentedButton(
            controls_frame,
            values=["Scuro", "Chiaro"],
            command=self.change_appearance_mode,
            width=150
        )
        self.appearance_mode_menu.set("Scuro")
        self.appearance_mode_menu.pack(pady=5)
        
    def create_main_content(self):
        # Frame per i controlli principali
        self.control_frame = ctk.CTkFrame(
            self.main_content,
            fg_color="transparent"
        )
        self.control_frame.pack(fill="x", pady=(0, 20))
        
        # Configurazione del grid layout nel control_frame
        self.control_frame.grid_columnconfigure(0, weight=1)
        self.control_frame.grid_rowconfigure(0, weight=0)
        self.control_frame.grid_rowconfigure(1, weight=0)
        self.control_frame.grid_rowconfigure(2, weight=0)
        
        # Bottoni principali
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
        
        # Aggiungi lo status label sotto i bottoni
        self.status_label = ctk.CTkLabel(
            self.control_frame,
            text="◉ Server Spento",
            font=ctk.CTkFont(size=15),
            text_color=("#E57373", "#EF5350")
        )
        self.status_label.grid(row=1, column=0, pady=(10, 0))
        
        # Separatore
        separator = ctk.CTkFrame(
            self.main_content,
            height=2,
            fg_color=("gray75", "gray30")
        )
        separator.pack(fill="x", pady=15)
        
        # Console frame
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
        
        # Console text area
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
        
        # Port info
        port_label = ctk.CTkLabel(
            footer,
            text=f"Porta: {self.config.get('port', 5000)}",
            font=ctk.CTkFont(size=12),
            text_color=("gray45", "gray60")
        )
        port_label.grid(row=0, column=0, padx=20, pady=5)
        
        # Last access
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
                pass  # Ignora se il formato della data non è valido
            
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
        if not os.path.exists('app.py'):
            self.show_error("File app.py non trovato nella directory corrente!")
            return
        
        try:
            self.server_thread = threading.Thread(target=self._run_server)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            self.is_server_running = True
            self.update_status(f"Server attivo sulla porta {self.config.get('port', 5000)}", True)
            
            if self.config.get('auto_launch_browser', True):
                self.root.after(1500, lambda: webbrowser.open(f"http://127.0.0.1:{self.config.get('port', 5000)}"))
            
        except Exception as e:
            self.show_error(f"Errore durante l'avvio del server: {str(e)}")

    def _run_server(self):
        try:
            self.server_process = subprocess.Popen(
                [sys.executable, 'app.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Monitor output in real-time
            while True:
                output = self.server_process.stdout.readline()
                if output:
                    self.root.after(0, lambda x=output: self.console.insert("end", x.decode()))
                    self.console.see("end")
                if not output and self.server_process.poll() is not None:
                    break
                    
            if self.server_process.poll() != 0:
                error = self.server_process.stderr.read().decode()
                self.root.after(0, lambda: self.show_error(f"Errore del server: {error}"))
                
        except Exception as e:
            self.root.after(0, lambda: self.show_error(f"Errore del server: {str(e)}"))

    def stop_server(self):
        if self.server_process:
            self.server_process.terminate()
            self.is_server_running = False
            self.update_status("Server arrestato", False)

    def show_error(self, message):
        dialog = ctk.CTkInputDialog(
            text=message,
            title="Errore",
            button_fg_color=("#F44336", "#D32F2F")
        )
        
    def change_appearance_mode(self, new_appearance_mode):
        mode = "dark" if new_appearance_mode == "Scuro" else "light"
        ctk.set_appearance_mode(mode)
        self.config['theme'] = mode
        self.save_config()
        
    def on_window_resize(self, event=None):
        # Aggiusta dinamicamente l'altezza della console in base alla dimensione della finestra
        if hasattr(self, 'console'):
            window_height = self.root.winfo_height()
            self.console.configure(height=max(250, window_height - 400))

    def run(self):
        # Carica le preferenze del tema
        if self.config.get('theme') == 'light':
            self.appearance_mode_menu.set("Chiaro")
            ctk.set_appearance_mode("light")
            
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernFlaskLauncher()
    app.run()
