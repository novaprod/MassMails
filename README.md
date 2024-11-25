# MassMailSender

**MassMailSender** is an application developed with **Python Flask**, **HTML**, **CSS**, and **JavaScript** for bulk email sending using Google accounts. The app includes an **autoswitch** function to automatically handle Google's daily sending limits.

## Features
- **Bulk email sending** with customizable templates.
- **Automatic autoswitch** between Google accounts when the daily limit (500 emails per account) is reached.
- Intuitive web interface for configuration and monitoring.
- Support for:
  - Uploading recipient lists in CSV format.
  - Manually entering email addresses.
  - Adding attachments.
  - Message preview and customization.
- Detailed logs to monitor email sending status.
- **Dark/Light theme** configurable.

## Requirements
- **Python 3.x**
- **Required Python Libraries:**
  - Flask
  - Flask-Mail
  - Pandas
  - WTForms
- **Google Accounts** configured with:
  - Access for less secure apps enabled.
  - App-specific passwords (recommended).

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/mass-mailsender.git
   cd mass-mailsender
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create the required directories for the project:
   ```bash
   mkdir -p static/uploads/csv static/uploads/attachments logs
   ```
4. Configure Google accounts by adding a CSV file in the `static/uploads/csv` directory with the following format:
   ```csv
   email,password,sent_today,last_sent_date
   example1@gmail.com,password1,0,2024-11-25
   example2@gmail.com,password2,0,2024-11-25
   ```
5. Run the application:
   ```bash
   python app.py
   ```

## Usage
1. Upload a CSV file with an "email" column for recipients or manually enter addresses.
2. Configure the message:
   - Subject.
   - Body (text or HTML).
   - Optional attachments.
3. Start sending and monitor progress via the progress bar and logs.
4. View detailed logs for each sent email.

## Customization
MassMailSender is fully customizable:
- Change the theme (dark or light) via the user interface.
- Add new Google accounts to increase sending capacity.
- Configure the maximum daily email limit per account.

## Security
Ensure that each Google account is properly configured to guarantee maximum security:
- Use app-specific passwords.
- Configure access via OAuth 2.0 for enhanced security (optional).

## License
This project is distributed under the MIT license. Refer to the LICENSE file for more details.

---
**Note:**
The use of this application must comply with anti-spam policies and local email marketing laws.
