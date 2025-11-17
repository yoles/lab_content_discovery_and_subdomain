from flask import Flask, render_template, request, Response, jsonify
from functools import wraps
import base64

app = Flask(__name__)

app.config['SECRET_KEY'] = 'admin-portal-secret-key-2024'

# FLAG 7 - Admin Portal
FLAG = 'FLAG{admin_portal_found_3h4c}'

# Weak admin credentials - INTENTIONALLY INSECURE
ADMIN_USERS = {
    'admin': 'admin123',           # Very weak and common
    'techcorp': 'techcorp2024',    # Company name based
    'administrator': 'password',    # Extremely weak
    'root': 'root123',             # Common default
    'superuser': 'super2024'       # Predictable
}

def check_auth(username, password):
    """
    Check if username/password combination is valid
    Returns True if credentials are correct
    """
    return username in ADMIN_USERS and ADMIN_USERS[username] == password

def authenticate():
    """
    Sends a 401 response that enables basic auth
    """
    return Response(
        'Authentication Required\n\n'
        'This is a restricted admin portal. Valid credentials are required.\n\n'
        'Hint: Try common admin usernames and weak passwords.\n'
        'Examples: admin, administrator, techcorp, root\n',
        401,
        {'WWW-Authenticate': 'Basic realm="TechCorp Admin Portal - Restricted Access"'}
    )

def requires_auth(f):
    """
    Decorator to require HTTP Basic Authentication
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    """
    Public login page (doesn't require auth, but provides info)
    """
    return render_template('login.html')

@app.route('/dashboard')
@requires_auth
def dashboard():
    """
    Admin dashboard - requires authentication - FLAG 7
    """
    username = request.authorization.username
    return render_template('dashboard.html',
                         flag=FLAG,
                         username=username,
                         admin_users=ADMIN_USERS)

@app.route('/api/admin/status')
@requires_auth
def admin_status():
    """
    Admin API endpoint - requires authentication
    """
    return jsonify({
        'flag': FLAG,
        'message': 'Congratulations! You found and accessed the admin portal!',
        'authenticated_as': request.authorization.username,
        'permissions': ['read', 'write', 'delete', 'admin'],
        'access_level': 'full',
        'all_flags_summary': {
            'total': 7,
            'locations': [
                'FLAG 1: robots.txt on main site',
                'FLAG 2: backup file on main site',
                'FLAG 3: .git/config on main site',
                'FLAG 4: /api/v2/admin/users on main site',
                'FLAG 5: dev.techcorp.local (debug mode)',
                'FLAG 6: staging.techcorp.local/phpinfo.php',
                'FLAG 7: admin.techcorp.local/dashboard (you are here!)'
            ]
        },
        'security_note': 'All 7 flags found! Review the security issues discovered.',
        'vulnerabilities_found': [
            'Exposed robots.txt revealing sensitive paths',
            'Accessible backup files with database dumps',
            'Exposed .git directory with credentials',
            'Undocumented API endpoints',
            'Discoverable development subdomain',
            'Staging environment with phpinfo() exposed',
            'Admin portal with weak authentication'
        ]
    })

@app.route('/api/admin/users')
@requires_auth
def admin_users():
    """
    List admin users (authenticated endpoint)
    """
    return jsonify({
        'users': [
            {'username': user, 'role': 'admin', 'active': True}
            for user in ADMIN_USERS.keys()
        ],
        'note': 'These users have weak passwords - major security issue!'
    })

@app.route('/api/admin/config')
@requires_auth
def admin_config():
    """
    Admin configuration endpoint
    """
    return jsonify({
        'flag': FLAG,
        'admin_portal': {
            'version': '2.1.4',
            'authentication': 'HTTP Basic Auth (WEAK)',
            'session_timeout': '30 minutes',
            'two_factor': False,
            'rate_limiting': False,
            'ip_whitelist': []
        },
        'database': {
            'host': 'prod-db.internal.techcorp.local',
            'port': 5432,
            'name': 'techcorp_production',
            'user': 'admin',
            'backup_schedule': 'daily at 02:00 UTC'
        },
        'services': {
            'main_site': 'techcorp.local:8080',
            'dev_environment': 'dev.techcorp.local:8081',
            'staging_environment': 'staging.techcorp.local:8082',
            'admin_portal': 'admin.techcorp.local:8083'
        }
    })

# Add admin-specific headers
@app.after_request
def add_admin_headers(response):
    response.headers['X-Portal-Type'] = 'admin'
    response.headers['X-Auth-Method'] = 'basic'
    response.headers['X-TechCorp-Version'] = '2.1.4'
    response.headers['X-Admin-Portal'] = 'true'
    return response

# Error handlers
@app.errorhandler(401)
def unauthorized(e):
    return jsonify({
        'error': '401 Unauthorized',
        'message': 'Authentication required',
        'hint': 'Try common admin credentials: admin/admin123, administrator/password, techcorp/techcorp2024'
    }), 401

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    print("=" * 60)
    print("TechCorp Admin Portal")
    print("=" * 60)
    print(f"FLAG: {FLAG}")
    print("Authentication: HTTP Basic Auth (WEAK)")
    print("\nValid credentials (weak passwords!):")
    for username, password in ADMIN_USERS.items():
        print(f"  - {username}:{password}")
    print("\nEndpoints:")
    print("  - / (public login page)")
    print("  - /dashboard (requires auth - FLAG location)")
    print("  - /api/admin/status (requires auth)")
    print("  - /api/admin/users (requires auth)")
    print("  - /api/admin/config (requires auth)")
    print("=" * 60)
    print("Starting Flask server on port 5003...")
    print("Access: http://admin.techcorp.local:8083")
    print("=" * 60)

    app.run(host='127.0.0.1', port=5003, debug=False)
