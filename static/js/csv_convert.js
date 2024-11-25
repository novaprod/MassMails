function convertEmailsToCSV(emails) {
    
    let csvContent = "Email\n";
    
    csvContent += emails.map(email => `"${email}"`).join("\n");
    return csvContent;
}


function downloadCSV(csvContent, filename) {
    var blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    if (navigator.msSaveBlob) { 
        navigator.msSaveBlob(blob, filename);
    } else {
        var link = document.createElement("a");
        if (link.download !== undefined) { 
            var url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", filename);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    $('#downloadManualEmails').click(function() {
        console.log("Bottone cliccato");
        var manualEmails = $('#manual_emails').val().trim();
        console.log("Manual Emails:", manualEmails);
        if (manualEmails === '') {
            console.log("Nessuna email da scaricare.");
            Swal.fire({
                icon: 'warning',
                title: 'Nessuna email',
                text: 'Inserisci almeno un\'email!'
            });
            return;
        }
        var emails = manualEmails.split('\n').map(email => email.trim()).filter(email => email !== '');
        console.log("Emails:", emails);
        var csvContent = convertEmailsToCSV(emails);
        console.log("CSV Content:", csvContent);
        var filename = 'manual_emails.csv';
        downloadCSV(csvContent, filename);
        Swal.fire({
            icon: 'success',
            title: 'Download iniziato',
            text: 'Il download è in corso!'
        });
    });
});
