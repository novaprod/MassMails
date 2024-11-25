document.addEventListener('DOMContentLoaded', function() {
    
    $('#emailForm').on('submit', function(e) {
        e.preventDefault();

        
        $('#progress-container').removeClass('hidden');

        
        var bar = new ProgressBar.Line('#progress-bar', {
            strokeWidth: 4,
            easing: 'easeInOut',
            duration: 1400,
            color: '#1d4ed8', 
            trailColor: '#d1d5db', 
            trailWidth: 1,
            svgStyle: {width: '100%', height: '100%'}
        });

        
        var progress = 0;
        var interval = setInterval(function() {
            progress += 1;
            bar.animate(progress / 100);  
            $('#progress-text').text(progress + '% completato');
            if(progress >= 100){
                clearInterval(interval);
                
                $('#emailForm')[0].submit();
            }
        }, 50);
    });
});


        
        const translations = {
            'it': {
                'edit_email': 'Modifica Email',
                'preview_email': 'Anteprima Email',
                'send_email': 'Invio di Email di Massa',
                'send_email_description': 'Invia email personalizzate a molti destinatari in modo semplice e veloce.',
                'subject': 'Oggetto',
                'body': 'Corpo del Messaggio',
                'body_placeholder': 'Inserisci il corpo del messaggio',
                'send_as_template': 'Invia come template',
                'email_template': 'Template Email',
                'choose_template': 'Scegli il template',
                'template_help': 'Carica un file HTML come template dell\'email.',
                'csv_file': 'File CSV',
                'choose_csv': 'Scegli il file CSV',
                'insert_manual_emails': 'Inserisci Email Manualmente',
                'csv_help': 'Il file CSV deve contenere una colonna \'email\'.<br>Oppure, puoi inserire email manualmente.',
                'no_manual_emails': 'Nessuna email inserita manualmente.',
                'attachments': 'Allegati',
                'choose_attachments': 'Scegli gli allegati',
                'attachments_help': 'Puoi aggiungere più allegati.',
                'send_email_button': 'Invia Email',
                'insert_manual_emails_modal_title': 'Inserisci Email Manualmente',
                'emails_per_line': 'Email (una per riga)',
                'emails_placeholder': 'esempio1@gmail.com\nesempio2@gmail.com',
                'emails_help': 'Inserisci una lista di indirizzi email, uno per riga.',
                'cancel': 'Annulla',
                'save_emails': 'Salva Email',
                'edit_email_window': 'Modifica Email',
                'upload_banner': 'Carica Banner',
                'upload_banner_placeholder': 'Seleziona un\'immagine',
                'footer_text': 'Testo del Footer',
                'custom_font': 'Font Personalizzato',
                'close': 'Chiudi',
                'save_changes': 'Salva modifiche',
                'email_logs': 'Log di Invio Email',
                'debug_settings': 'Debug e Impostazioni Sviluppatore',
                'max_email_limit': 'Limite massimo di email',
                'max_email_limit_placeholder': 'Inserisci il nuovo limite massimo',
                'debug_console': 'Console di Debug',
                'utilities': 'Utilità',
                'clear_console': 'Pulisci Console',
                'force_reload': 'Forza Reload',
                'reset_daily_emails': 'Resetta Email Giornaliere',
                'reset_daily_emails_text': 'Resetta Email Giornaliere',
                'save': 'Salva',
                'gmail_account_management': 'Gestione Account Gmail',
                'gmail_email': 'Email Gmail',
                'gmail_email_placeholder': 'esempio@gmail.com',
                'in_app_password': 'Password In-App',
                'in_app_password_placeholder': 'Password',
                'add_account': 'Aggiungi Account',
                'added_accounts': 'Account Aggiunti:',
                'additional_settings': 'Impostazioni Aggiuntive:',
                'language': 'Lingua',
                'language_help': 'Seleziona la lingua dell\'interfaccia.',
                'theme': 'Tema',
                'dark_theme': 'Scuro',
                'theme_help': 'Attiva o disattiva il tema scuro.',
                'sending_emails': 'Invio Email in corso',
                'sending_progress': 'Progressione Invio Email',
                'progress_percentage': '0% completato'
            },
            'en': {
                'edit_email': 'Edit Email',
                'preview_email': 'Email Preview',
                'send_email': 'Send Emails',
                'send_email_description': 'Send personalized emails to many recipients easily and quickly.',
                'subject': 'Subject',
                'body': 'Message Body',
                'body_placeholder': 'Enter the message body',
                'send_as_template': 'Send as Template',
                'email_template': 'Email Template',
                'choose_template': 'Choose Template',
                'template_help': 'Upload an HTML file as the email template.',
                'csv_file': 'CSV File',
                'choose_csv': 'Choose CSV File',
                'insert_manual_emails': 'Insert Emails Manually',
                'csv_help': 'The CSV file must contain an \'email\' column.<br>Alternatively, you can insert emails manually.',
                'no_manual_emails': 'No emails inserted manually.',
                'attachments': 'Attachments',
                'choose_attachments': 'Choose Attachments',
                'attachments_help': 'You can add multiple attachments.',
                'send_email_button': 'Send Email',
                'insert_manual_emails_modal_title': 'Insert Emails Manually',
                'emails_per_line': 'Emails (one per line)',
                'emails_placeholder': 'example1@gmail.com\example2@gmail.com',
                'emails_help': 'Enter a list of email addresses, one per line.',
                'cancel': 'Cancel',
                'save_emails': 'Save Emails',
                'edit_email_window': 'Edit Email',
                'upload_banner': 'Upload Banner',
                'upload_banner_placeholder': 'Select an image',
                'footer_text': 'Footer Text',
                'custom_font': 'Custom Font',
                'close': 'Close',
                'save_changes': 'Save Changes',
                'email_logs': 'Email Sending Logs',
                'debug_settings': 'Debug and Developer Settings',
                'max_email_limit': 'Maximum Email Limit',
                'max_email_limit_placeholder': 'Enter the new maximum limit',
                'debug_console': 'Debug Console',
                'utilities': 'Utilities',
                'clear_console': 'Clear Console',
                'force_reload': 'Force Reload',
                'reset_daily_emails': 'Reset Daily Emails',
                'reset_daily_emails_text': 'Reset Daily Emails',
                'save': 'Save',
                'gmail_account_management': 'Manage Gmail Accounts',
                'gmail_email': 'Gmail Email',
                'gmail_email_placeholder': 'example@gmail.com',
                'in_app_password': 'In-App Password',
                'in_app_password_placeholder': 'Password',
                'add_account': 'Add Account',
                'added_accounts': 'Added Accounts:',
                'additional_settings': 'Additional Settings:',
                'language': 'Language',
                'language_help': 'Select the interface language.',
                'theme': 'Theme',
                'dark_theme': 'Dark',
                'theme_help': 'Enable or disable dark theme.',
                'sending_emails': 'Sending Emails in Progress',
                'sending_progress': 'Email Sending Progress',
                'progress_percentage': '0% completed'
            }
            
        };

        
        function applyTranslations(lang) {
            $('[data-i18n]').each(function() {
                const key = $(this).attr('data-i18n');
                if(translations[lang] && translations[lang][key]) {
                    $(this).text(translations[lang][key]);
                }
            });
            
            $('[data-i18n-placeholder]').each(function() {
                const key = $(this).attr('data-i18n-placeholder');
                if(translations[lang] && translations[lang][key]) {
                    $(this).attr('placeholder', translations[lang][key]);
                }
            });
            
            $('[data-i18n-html]').each(function() {
                const key = $(this).attr('data-i18n-html');
                if(translations[lang] && translations[lang][key]) {
                    $(this).html(translations[lang][key]);
                }
            });
        }

        
        function saveSettings() {
            
            const isDark = $('#themeToggle').is(':checked');
            if(isDark) {
                $('body').addClass('dark');
                localStorage.setItem('theme', 'dark');
            } else {
                $('body').removeClass('dark');
                localStorage.setItem('theme', 'light');
            }

            
            const selectedLanguage = $('#languageSelect').val();
            localStorage.setItem('language', selectedLanguage);

            
            applyTranslations(selectedLanguage);

            
            

            Swal.fire({
                icon: 'success',
                title: 'Successo',
                text: (selectedLanguage === 'it') ? 'Impostazioni salvate correttamente.' : 'Settings saved successfully.'
            });
        }

        
        function loadSettings() {
            
            const theme = localStorage.getItem('theme') || 'light';
            if(theme === 'dark') {
                $('body').addClass('dark');
                $('#themeToggle').prop('checked', true);
            } else {
                $('body').removeClass('dark');
                $('#themeToggle').prop('checked', false);
            }

            
            const language = localStorage.getItem('language') || 'it';
            $('#languageSelect').val(language);
            applyTranslations(language);
        }

        
        function logToConsole(message) {
            const consoleElement = document.getElementById('debugConsole');
            const timestamp = new Date().toLocaleTimeString();
            consoleElement.value += `[${timestamp}] ${message}\n`;
            consoleElement.scrollTop = consoleElement.scrollHeight;
        }

        
        $(document).ready(function() {
            
            AOS.init();

            
            loadSettings();

            
            $('#modifyEmailWindow').draggable({
                handle: ".window-header"
            }).resizable();

            
            $('#modify-email').click(function() {
                $('#modifyEmailWindow').show();
            });

            
            $('#closeModifyWindow, #closeModifyWindowFooter').click(function() {
                $('#modifyEmailWindow').hide();
            });

            
            $('#saveChanges').click(function() {
                
                var bannerFile = $('#bannerInput')[0].files[0];
                if (bannerFile) {
                    var reader = new FileReader();
                    reader.onload = function(e) {
                        $('#email-banner').html('<img src="' + e.target.result + '" style="width:100%; border-bottom: 1px solid #dadce0;">');
                    };
                    reader.readAsDataURL(bannerFile);
                } else {
                    $('#email-banner').empty();
                }

                
                var footerText = $('#footerText').val();
                $('#email-footer').text(footerText);

                
                var selectedFont = $('#fontSelect').val();
                $('#preview-body').css('font-family', selectedFont);
                $('#preview-subject').css('font-family', selectedFont);

                
                $('#modifyEmailWindow').hide();
            });

            
            function toggleTemplateField() {
                if ($('#template_checkbox').is(':checked')) {
                    
                    $('#template_file').prop('disabled', false);
                    $('#template_button').prop('disabled', false);
                    $('#template_field').removeClass('disabled-field');
                } else {
                    
                    $('#template_file').prop('disabled', true);
                    $('#template_button').prop('disabled', true); 
                    $('#template_field').addClass('disabled-field');

                    
                    $('#template-file-name').text('Scegli il template');

                    
                    $('#preview-body').html($('#email-body').val().replace(/\n/g, '<br>') || '[Corpo del messaggio]');
                }
            }

            
            toggleTemplateField();

            
            $('#template_checkbox').change(function() {
                toggleTemplateField();
            });

            
            $('#csv_file').change(function(e){
                var fileName = e.target.files[0] ? e.target.files[0].name : 'Scegli il file CSV';
                $('#csv-file-name').text(fileName);
            });

            
            $('#attachments').change(function(e){
                var files = e.target.files;
                var fileNames = [];
                for(var i=0; i<files.length; i++){
                    fileNames.push(files[i].name);
                }
                if(fileNames.length > 0){
                    $('#attachments-file-name').text(fileNames.join(', '));
                } else {
                    $('#attachments-file-name').text('Scegli gli allegati');
                }
            });

            
            $('#template_file').change(function(e){
                var file = e.target.files[0];
                if(file){
                    $('#template-file-name').text(file.name);
                    
                    var reader = new FileReader();
                    reader.onload = function(e) {
                        $('#preview-body').html(e.target.result);
                    };
                    reader.readAsText(file);
                } else {
                    $('#template-file-name').text('Scegli il template');
                    $('#preview-body').html($('#email-body').val().replace(/\n/g, '<br>') || '[Corpo del messaggio]');
                }
            });

            
            var progressModal = new bootstrap.Modal(document.getElementById('progressModal'), {
                backdrop: 'static',
                keyboard: false
            });

            
            $('#emailForm').on('submit', function(e) {
                var csvProvided = $('#csv_file').get(0).files.length > 0;
                var manualEmails = $('#manual_emails').val().trim();

                if (!csvProvided && manualEmails === '') {
                    e.preventDefault(); 
                    Swal.fire({
                        icon: 'error',
                        title: 'Errore',
                        text: (localStorage.getItem('language') === 'en') ? 'You must provide a CSV file or enter emails manually.' : 'Devi fornire un file CSV o inserire email manualmente.'
                    });
                } else {
                    e.preventDefault(); 

                    
                    progressModal.show();

                    
                    var progress = 0;
                    $('#progress-bar').css('width', '0%').attr('aria-valuenow', 0);
                    $('#progress-text').text('0% completato');

                    var interval = setInterval(function() {
                        progress += 1;
                        $('#progress-bar').css('width', progress + '%').attr('aria-valuenow', progress);
                        $('#progress-text').text(progress + '% completato');
                        if(progress >= 100){
                            clearInterval(interval);
                            
                            progressModal.hide();
                            
                            $('#emailForm').off('submit');
                            
                            $('#emailForm')[0].submit();
                        }
                    }, 50);
                }
            });

            
            $('#toggle-preview').click(function() {
                $('#preview-panel').toggleClass('open');

                
                if ($('#preview-panel').hasClass('open')) {
                    $('.main-container').removeClass('full-width').addClass('half-width');
                } else {
                    $('.main-container').removeClass('half-width').addClass('full-width');
                }
            });

            
            $('.main-container').addClass('full-width');

            
            $('#email-subject').on('input', function() {
                var subject = $(this).val();
                $('#preview-subject').text(subject || '[Oggetto]');
            });

            $('#email-body').on('input', function() {
                
                if(!$('#template_checkbox').is(':checked') || !$('#template_file')[0].files[0]){
                    var body = $(this).val().replace(/\n/g, '<br>');
                    $('#preview-body').html(body || '[Corpo del messaggio]');
                }
            });

            
            var settingsModal = new bootstrap.Modal(document.getElementById('settingsModal'), {
                keyboard: false
            });

            
            var logsModal = new bootstrap.Modal(document.getElementById('logsModal'), {
                keyboard: false
            });

            
            $('#settings-icon').click(function() {
                settingsModal.show();
                loadAccounts();
                loadSettings(); 
            });

            
            $('#logs-icon').click(function() {
                loadLogs();
                logsModal.show();
            });

            
            function loadAccounts() {
                $.ajax({
                    url: "{{ url_for('get_accounts') }}",
                    method: 'GET',
                    success: function(response) {
                        if(response.status === 'success'){
                            $('#accountsList').empty();
                            response.accounts.forEach(function(account){
                                $('#accountsList').append(`
                                    <li class="list-group-item d-flex justify-content-between align-items-center">
                                        <div>
                                            <strong>Email:</strong> ${account.email}<br>
                                            <strong>Inviate oggi:</strong> ${account.sent_today} / ${currentEmailLimit}<br>
                                            <strong>Ultimo invio:</strong> ${account.last_sent_date}
                                        </div>
                                        <button class="btn btn-danger btn-sm remove-account" data-email="${account.email}">
                                            <i class="fas fa-trash"></i> <span data-i18n="remove">Rimuovi</span>
                                        </button>
                                    </li>
                                `);
                            });
                        } else {
                            Swal.fire({
                                icon: 'error',
                                title: (localStorage.getItem('language') === 'en') ? 'Error' : 'Errore',
                                text: response.message
                            });
                        }
                    },
                    error: function(xhr){
                        Swal.fire({
                            icon: 'error',
                            title: (localStorage.getItem('language') === 'en') ? 'Error' : 'Errore',
                            text: xhr.responseJSON ? xhr.responseJSON.message : ((localStorage.getItem('language') === 'en') ? 'Error loading accounts.' : 'Errore nel caricamento degli account.')
                        });
                    }
                });
            }

            
            function loadLogs() {
                $.ajax({
                    url: "{{ url_for('list_logs') }}",
                    method: 'GET',
                    success: function(response) {
                        if(response.status === 'success'){
                            $('#logsList').empty();
                            if(response.logs.length === 0){
                                $('#logsList').append('<li class="list-group-item" data-i18n="no_logs">Nessun log disponibile.</li>');
                            } else {
                                response.logs.forEach(function(log){
                                    $('#logsList').append(`
                                        <li class="list-group-item d-flex justify-content-between align-items-center">
                                            <span>${log}</span>
                                            <a href="/log/${log}" target="_blank" class="btn btn-sm btn-primary" data-i18n="view">
                                                <i class="fas fa-eye"></i> <span data-i18n="view">Visualizza</span>
                                            </a>
                                        </li>
                                    `);
                                });
                            }
                        } else {
                            Swal.fire({
                                icon: 'error',
                                title: (localStorage.getItem('language') === 'en') ? 'Error' : 'Errore',
                                text: response.message
                            });
                        }
                    },
                    error: function(xhr){
                        Swal.fire({
                            icon: 'error',
                            title: (localStorage.getItem('language') === 'en') ? 'Error' : 'Errore',
                            text: xhr.responseJSON ? xhr.responseJSON.message : ((localStorage.getItem('language') === 'en') ? 'Error loading logs.' : 'Errore nel caricamento dei log.')
                        });
                    }
                });
            }

            
            $('#addAccountForm').submit(function(e) {
                e.preventDefault();
                var email = $('#gmailEmail').val().trim();
                var password = $('#gmailPassword').val().trim();

                if(email === '' || password === ''){
                    Swal.fire({
                        icon: 'error',
                        title: (localStorage.getItem('language') === 'en') ? 'Error' : 'Errore',
                        text: (localStorage.getItem('language') === 'en') ? 'Both fields are required.' : 'Entrambi i campi sono obbligatori.'
                    });
                    return;
                }

                $.ajax({
                    url: "{{ url_for('add_account') }}",
                    method: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({email: email, password: password}),
                    success: function(response){
                        if(response.status === 'success'){
                            
                            $('#addAccountForm')[0].reset();

                            
                            loadAccounts();

                            Swal.fire({
                                icon: 'success',
                                title: (localStorage.getItem('language') === 'en') ? 'Success' : 'Successo',
                                text: response.message
                            });
                        } else {
                            Swal.fire({
                                icon: 'error',
                                title: (localStorage.getItem('language') === 'en') ? 'Error' : 'Errore',
                                text: response.message
                            });
                        }
                    },
                    error: function(xhr){
                        Swal.fire({
                            icon: 'error',
                            title: (localStorage.getItem('language') === 'en') ? 'Error' : 'Errore',
                            text: xhr.responseJSON ? xhr.responseJSON.message : ((localStorage.getItem('language') === 'en') ? 'Error adding account.' : 'Errore nell\'aggiunta dell\'account.')
                        });
                    }
                });
            });

            
            $('#accountsList').on('click', '.remove-account', function(){
                var email = $(this).data('email');

                Swal.fire({
                    title: (localStorage.getItem('language') === 'en') ? 'Are you sure?' : 'Sei sicuro?',
                    text: (localStorage.getItem('language') === 'en') ? `Do you want to remove the account ${email}?` : `Vuoi rimuovere l'account ${email}?`,
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonText: (localStorage.getItem('language') === 'en') ? 'Yes, remove!' : 'Sì, rimuovi!',
                    cancelButtonText: (localStorage.getItem('language') === 'en') ? 'Cancel' : 'Annulla'
                }).then((result) => {
                    if(result.isConfirmed){
                        $.ajax({
                            url: "{{ url_for('delete_account') }}",
                            method: 'POST',
                            contentType: 'application/json',
                            data: JSON.stringify({email: email}),
                            success: function(response){
                                if(response.status === 'success'){
                                    
                                    loadAccounts();

                                    Swal.fire({
                                        icon: 'success',
                                        title: (localStorage.getItem('language') === 'en') ? 'Removed' : 'Rimosso',
                                        text: response.message
                                    });
                                } else {
                                    Swal.fire({
                                        icon: 'error',
                                        title: (localStorage.getItem('language') === 'en') ? 'Error' : 'Errore',
                                        text: response.message
                                    });
                                }
                            },
                            error: function(xhr){
                                Swal.fire({
                                    icon: 'error',
                                    title: (localStorage.getItem('language') === 'en') ? 'Error' : 'Errore',
                                    text: xhr.responseJSON ? xhr.responseJSON.message : ((localStorage.getItem('language') === 'en') ? 'Error removing account.' : 'Errore nella rimozione dell\'account.')
                                });
                            }
                        });
                    }
                });
            });

            
            $('#settingsModal').on('show.bs.modal', function () {
                $('#main-content').addClass('blur');
            });

            $('#settingsModal').on('hidden.bs.modal', function () {
                $('#main-content').removeClass('blur');
            });

            $('#logsModal').on('show.bs.modal', function () {
                $('#main-content').addClass('blur');
            });

            $('#logsModal').on('hidden.bs.modal', function () {
                $('#main-content').removeClass('blur');
            });

            
            
            $('#openManualEmailsModal').click(function() {
                $('#manualEmailsModal').modal('show');
            });

            
            $('#saveManualEmails').click(function() {
                var manualEmails = $('#manualEmailsTextarea').val().trim();
                if (manualEmails === '') {
                    Swal.fire({
                        icon: 'warning',
                        title: (localStorage.getItem('language') === 'en') ? 'No Emails Entered' : 'Nessuna Email Inserita',
                        text: (localStorage.getItem('language') === 'en') ? 'Please enter at least one email address or cancel.' : 'Per favore, inserisci almeno un indirizzo email o annulla.'
                    });
                    return;
                }

                
                var emails = manualEmails.split('\n').map(email => email.trim()).filter(email => email !== '');
                var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                var invalidEmails = emails.filter(email => !emailRegex.test(email));

                if (invalidEmails.length > 0) {
                    Swal.fire({
                        icon: 'error',
                        title: (localStorage.getItem('language') === 'en') ? 'Invalid Emails' : 'Email non valide',
                        text: (localStorage.getItem('language') === 'en') ? 'Some email addresses are invalid: ' : 'Alcuni indirizzi email non sono validi: ' + invalidEmails.join(', ')
                    });
                    return;
                }

                
                var uniqueEmails = [...new Set(emails)].join('\n');

                
                $('#manual_emails').val(uniqueEmails);

                
                $('#manual-emails-count').text(emails.length + ' ' + ((localStorage.getItem('language') === 'en') ? 'emails inserted manually.' : 'email inserite manualmente.'));

                
                $('#manualEmailsModal').modal('hide');
            });

            
            var existingManualEmails = $('#manual_emails').val();
            if (existingManualEmails) {
                var emails = existingManualEmails.split('\n').map(email => email.trim()).filter(email => email !== '');
                $('#manual-emails-count').text(emails.length + ' ' + ((localStorage.getItem('language') === 'en') ? 'emails inserted manually.' : 'email inserite manualmente.'));
            } else {
                $('#manual-emails-count').text((localStorage.getItem('language') === 'en') ? 'No emails inserted manually.' : 'Nessuna email inserita manualmente.');
            }

            
            $('#resetSentCounts').click(function() {
                Swal.fire({
                    title: (localStorage.getItem('language') === 'en') ? 'Are you sure?' : 'Sei sicuro?',
                    text: (localStorage.getItem('language') === 'en') ? "Do you want to reset the daily email counts for all Gmail accounts?" : "Vuoi resettare i contatori delle email giornaliere per tutti gli account Gmail?",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonText: (localStorage.getItem('language') === 'en') ? 'Yes, reset' : 'Sì, resettare',
                    cancelButtonText: (localStorage.getItem('language') === 'en') ? 'Cancel' : 'Annulla',
                    reverseButtons: true
                }).then((result) => {
                    if (result.isConfirmed) {
                        
                        fetch('/reset_sent_counts', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({})
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.status === 'success') {
                                Swal.fire({
                                    icon: 'success',
                                    title: (localStorage.getItem('language') === 'en') ? 'Reset' : 'Resettato',
                                    text: data.message
                                });
                                logToConsole((localStorage.getItem('language') === 'en') ? '✅ Daily email counts reset.' : '✅ Contatori delle email giornaliere resettati.');
                                
                                loadAccounts();
                            } else {
                                Swal.fire({
                                    icon: 'error',
                                    title: (localStorage.getItem('language') === 'en') ? 'Error' : 'Errore',
                                    text: data.message
                                });
                                logToConsole(`❌ ${(localStorage.getItem('language') === 'en') ? 'Error' : 'Errore'}: ${data.message}`);
                            }
                        })
                        .catch(error => {
                            Swal.fire({
                                icon: 'error',
                                title: (localStorage.getItem('language') === 'en') ? 'Error' : 'Errore',
                                text: (localStorage.getItem('language') === 'en') ? `Request error: ${error}` : `Errore nella richiesta: ${error}`
                            });
                            logToConsole(`❌ ${(localStorage.getItem('language') === 'en') ? 'Request error' : 'Errore nella richiesta'}: ${error}`);
                        });
                    }
                });
            });

            
            $('#themeToggle, #languageSelect').change(function() {
                saveSettings();
            });

            
            document.addEventListener('keydown', function(event) {
                if (event.ctrlKey && event.altKey && event.key === 'm') {
                    const emailLimitModal = new bootstrap.Modal(document.getElementById('emailLimitModal'));
                    emailLimitModal.show();
                    
                    document.getElementById('emailLimitInput').value = currentEmailLimit;
                    logToConsole(`Aperto modale. Limite corrente: ${currentEmailLimit}`);
                }
            });

            
            document.getElementById('saveEmailLimit').addEventListener('click', function() {
                const newLimit = parseInt(document.getElementById('emailLimitInput').value);
                if (newLimit && newLimit > 0) {
                    
                    currentEmailLimit = newLimit;

                    
                    fetch('/update_email_limit', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ max_limit: newLimit })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            logToConsole(`✅ ${(localStorage.getItem('language') === 'en') ? 'Maximum email limit updated to ' : 'Limite massimo aggiornato a '}${currentEmailLimit}.`);
                            const emailLimitModal = bootstrap.Modal.getInstance(document.getElementById('emailLimitModal'));
                            emailLimitModal.hide();
                        } else {
                            logToConsole(`❌ ${(localStorage.getItem('language') === 'en') ? 'Error' : 'Errore'}: ${data.message}`);
                        }
                    })
                    .catch(error => {
                        logToConsole(`❌ ${(localStorage.getItem('language') === 'en') ? 'Request error' : 'Errore nella richiesta'}: ${error}`);
                    });
                } else {
                    logToConsole((localStorage.getItem('language') === 'en') ? '⚠️ Please enter a valid value.' : '⚠️ Inserisci un valore valido.');
                }
            });

            
            document.getElementById('clearDebugConsole').addEventListener('click', function() {
                document.getElementById('debugConsole').value = '';
            });

            
            document.getElementById('forceReload').addEventListener('click', function() {
                logToConsole((localStorage.getItem('language') === 'en') ? '🔄 Forcing page reload.' : '🔄 Reload forzato della pagina.');
                location.reload();
            });

            
            logToConsole((localStorage.getItem('language') === 'en') ? '🛠️ Debug console ready.' : '🛠️ Console di debug pronta.');

            
            $('#emailLimitModal .modal-content').draggable({
                handle: ".modal-header"
            }).resizable();
        });
