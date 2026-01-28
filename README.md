# Vet_Calendar_v2
 Vet Scheduler rebuilt with responsive frontend

## Setup
To initialize the virtual environment: pipenv shell
To install dependencies: pipenv install
To update: pipenv update

# IMPORTANT!!!
The following must be at the end of the .htaccess file for the frontend or there will be CORS errors when trying to hit the backend as well as 503 errors when reloading!!!
'''
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /sub/
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteCond %{REQUEST_FILENAME} !-l
  RewriteRule . /index.html [L]
</IfModule>
'''

# Running on Nginx server:
The year/month/user variables in the URL will cause a 404 error on Nginx. 
To correct this add a location block to the "appname.domain.com.conf" file located in /etc/nginx/sites-available
Add the following somewhere in the server block:
location / {
  root /path/to/your/app;  # replace with the actual path to your Quasar app
  try_files $uri $uri/ /index.html;
}

# Current available features:
- Login:
  - User login
  - User access request
  - "Remember Me" function to keep user logged in for multipple days
- Manage Users
  - New user creation (admin)
  - Edit User Details
  - Delete User
- Manage Schedule
  - 

## Environment Variables

| Variable                | Description                                                      | Sample Value / Example                                      |
|-------------------------|------------------------------------------------------------------|-------------------------------------------------------------|
| `SECRET_KEY`            | Django secret key for cryptographic signing.                     | `your-secret-key-here`                                      |
| `DEBUG`                 | Enable/disable Django debug mode.                                | `"True"` or `"False"`                                       |
| `DEVELOPMENT_MODE`      | Flag for development mode.                                       | `"True"` or `"False"`                                       |
| `DB_HOST`               | Database host address.                                           | `"127.0.0.1"`                                               |
| `DB_USER`               | Database username.                                               | `"dbuser"`                                                  |
| `DB_PASS`               | Database password.                                               | `"dbpassword"`                                              |
| `DB_TABLE`              | Database name/schema.                                            | `"mydatabase"`                                              |
| `DJANGO_ALLOWED_HOSTS`  | Comma-separated list of allowed hosts for Django.                | `"localhost,127.0.0.1,example.com"`                         |
| `CSRF_TRUSTED_ORIGINS`  | Comma-separated list of trusted origins for CSRF protection.     | `"http://localhost:9000/*,https://example.com/*"`           |
| `LOCAL_KEY`             | Local application key (purpose-specific).                        | `"your-local-key"`                                          |
| `GOOGLE_CLIENT_ID`      | Google OAuth2 client ID.                                         | `"your-google-client-id.apps.googleusercontent.com"`         |
| `GOOGLE_API_KEY`        | Google API key for accessing Google services.                    | `"your-google-api-key"`                                     |
| `DISCOVERY_DOC`         | Google API discovery document URL.                               | `"https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest"` |
| `SCOPES`                | OAuth2 scopes for Google API access.                             | `"https://www.googleapis.com/auth/calendar"`                 |
| `IMAP_HOSTNAME`         | IMAP server hostname for email.                                  | `"imap.example.com"`                                        |
| `IMAP_PORT`             | IMAP server port.                                                | `"993"`                                                     |
| `POP3_HOSTNAME`         | POP3 server hostname for email.                                  | `"pop3.example.com"`                                        |
| `POP3_PORT`             | POP3 server port.                                                | `"995"`                                                     |
| `SMTP_HOSTNAME`         | SMTP server hostname for sending email.                          | `"smtp.example.com"`                                        |
| `SMTP_PORT`             | SMTP server port.                                                | `"587"`                                                     |
| `EMAIL_HOST_USER`       | Email account username for sending email.                        | `"user@example.com"`                                        |
| `EMAIL_HOST_PASSWORD`   | Email account password for sending email.                        | `"emailpassword"`                                           |
| `DEBUG_EMAIL`           | Email address for debug notifications.                           | `"debug@example.com"`                                       |