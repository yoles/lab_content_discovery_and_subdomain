from flask import Flask, render_template, jsonify
import platform
import sys

app = Flask(__name__)

# Staging configuration
app.config['ENV'] = 'staging'
app.config['DEBUG'] = False
app.config['SECRET_KEY'] = 'staging-secret-key-2024'

# FLAG 6 - Staging Environment
FLAG = 'FLAG{staging_env_exposed_8g3b}'

@app.route('/')
def index():
    """Staging environment homepage"""
    return render_template('index.html')

@app.route('/phpinfo.php')
def phpinfo():
    """
    Simulated phpinfo page - FLAG 6
    This mimics a common misconfiguration where phpinfo() is left accessible
    """
    php_info = {
        'version': '8.2.0-dev',
        'system': platform.system() + ' ' + platform.release(),
        'server_api': 'FPM/FastCGI',
        'virtual_directory': 'disabled',
        'config_file_path': '/etc/php/8.2/fpm',
        'loaded_config': '/etc/php/8.2/fpm/php.ini'
    }

    environment_vars = {
        'SERVER_NAME': 'staging.techcorp.local',
        'SERVER_PORT': '8082',
        'DOCUMENT_ROOT': '/var/www/staging',
        'DB_HOST': 'staging-db.internal.techcorp.local',
        'DB_PORT': '5432',
        'DB_NAME': 'techcorp_staging',
        'DB_USER': 'staging_admin',
        'DB_PASS': 'St@g1ng_P@ss_2024',
        'REDIS_HOST': 'staging-redis.internal',
        'ADMIN_PORTAL': 'admin.techcorp.local',
        'ADMIN_EMAIL': 'admin@techcorp.local',
        'SMTP_SERVER': 'smtp.staging.techcorp.local',
        'API_KEY': 'staging_api_key_abc123xyz',
        'SECRET_TOKEN': 'stg_tok_9f8e7d6c5b4a3210'
    }

    php_extensions = [
        'Core', 'date', 'filter', 'hash', 'json', 'pcre', 'readline',
        'Reflection', 'SPL', 'standard', 'mysqlnd', 'PDO', 'pdo_mysql',
        'pdo_pgsql', 'curl', 'openssl', 'zip', 'gd', 'mbstring'
    ]

    # Return HTML mimicking phpinfo()
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>phpinfo() - Staging Server</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: #fff; color: #000; margin: 20px; }}
            h1 {{ background: #9999cc; color: #fff; padding: 20px; text-align: center; }}
            h2 {{ background: #9999cc; color: #fff; padding: 10px; margin-top: 30px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
            td {{ padding: 8px; border: 1px solid #000; }}
            td:first-child {{ background: #ccccff; font-weight: bold; width: 30%; }}
            .warning {{ background: #ff6666; color: #fff; padding: 15px; margin: 20px 0; text-align: center; font-weight: bold; }}
            .flag {{ background: #ffcc00; color: #000; padding: 20px; margin: 20px 0; text-align: center; font-size: 1.5em; font-weight: bold; border: 3px solid #ff6600; }}
        </style>
    </head>
    <body>
        <h1>PHP Version {php_info['version']}</h1>

        <div class="warning">
            ⚠️ WARNING: This page should NOT be accessible in production!
        </div>

        <div class="flag">
            🚩 FLAG: {FLAG}
        </div>

        <h2>System Information</h2>
        <table>
            <tr><td>PHP Version</td><td>{php_info['version']}</td></tr>
            <tr><td>System</td><td>{php_info['system']}</td></tr>
            <tr><td>Server API</td><td>{php_info['server_api']}</td></tr>
            <tr><td>Virtual Directory Support</td><td>{php_info['virtual_directory']}</td></tr>
            <tr><td>Configuration File (php.ini) Path</td><td>{php_info['config_file_path']}</td></tr>
            <tr><td>Loaded Configuration File</td><td>{php_info['loaded_config']}</td></tr>
        </table>

        <h2>Environment Variables</h2>
        <table>
    '''

    for key, value in environment_vars.items():
        html += f'<tr><td>{key}</td><td>{value}</td></tr>\n'

    html += '''
        </table>

        <h2>PHP Extensions</h2>
        <table>
            <tr><td colspan="2">''' + ', '.join(php_extensions) + '''</td></tr>
        </table>

        <h2>Security Notes</h2>
        <table>
            <tr><td>expose_php</td><td>On (BAD - reveals PHP version)</td></tr>
            <tr><td>display_errors</td><td>On (BAD - shows errors to users)</td></tr>
            <tr><td>log_errors</td><td>On</td></tr>
            <tr><td>error_reporting</td><td>E_ALL (verbose)</td></tr>
        </table>

        <h2>Next Steps</h2>
        <table>
            <tr><td>Hint</td><td>Database credentials are exposed above. Try accessing admin.techcorp.local next!</td></tr>
            <tr><td>Admin Portal</td><td>admin.techcorp.local (may require authentication)</td></tr>
            <tr><td>Admin Email</td><td>admin@techcorp.local</td></tr>
        </table>

        <p style="text-align: center; margin-top: 40px; color: #666;">
            <em>This is a staging environment. Never expose phpinfo() on production servers!</em>
        </p>
    </body>
    </html>
    '''

    return html

@app.route('/info')
def info():
    """Additional staging environment information"""
    return jsonify({
        'environment': 'staging',
        'version': '2.1.4-staging',
        'flag': FLAG,
        'server': 'staging.techcorp.local',
        'database': {
            'host': 'staging-db.internal.techcorp.local',
            'name': 'techcorp_staging',
            'user': 'staging_admin',
            'password': 'St@g1ng_P@ss_2024'
        },
        'features_enabled': [
            'debug_toolbar',
            'sql_logging',
            'profiler',
            'error_reporting'
        ],
        'internal_services': {
            'redis': 'staging-redis.internal',
            'elasticsearch': 'staging-es.internal',
            'rabbitmq': 'staging-mq.internal'
        },
        'hints': [
            'phpinfo.php is accessible (major security issue)',
            'Database credentials are exposed',
            'Try the admin portal: admin.techcorp.local',
            'Admin authentication might be weak'
        ]
    })

@app.route('/test.php')
def test():
    """Another test page often left behind"""
    return '''
    <html>
    <head><title>Staging Test Page</title></head>
    <body>
        <h1>Staging Environment - Test Page</h1>
        <p>This is a test page for the staging environment.</p>
        <ul>
            <li><a href="/phpinfo.php">PHPInfo (Debug)</a></li>
            <li><a href="/info">Environment Info (JSON)</a></li>
        </ul>
        <p><em>FLAG Hint: Check phpinfo.php for the flag!</em></p>
    </body>
    </html>
    '''

# Add staging-specific headers
@app.after_request
def add_staging_headers(response):
    response.headers['X-Environment'] = 'staging'
    response.headers['X-TechCorp-Version'] = '2.1.4-staging'
    response.headers['X-Server-Type'] = 'staging-web-01'
    response.headers['X-Debug-Info'] = 'enabled'
    return response

if __name__ == '__main__':
    print("=" * 60)
    print("TechCorp Staging Environment")
    print("=" * 60)
    print(f"FLAG: {FLAG}")
    print(f"Environment: {app.config['ENV']}")
    print("Critical files exposed:")
    print("  - /phpinfo.php (contains FLAG and credentials)")
    print("  - /info (environment details)")
    print("  - /test.php (test page)")
    print("=" * 60)
    print("Starting Flask server on port 5002...")
    print("Access: http://staging.techcorp.local:8082")
    print("=" * 60)

    app.run(host='127.0.0.1', port=5002, debug=False)
