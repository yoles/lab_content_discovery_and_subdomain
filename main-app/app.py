from flask import Flask, render_template, jsonify, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-do-not-use-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), default='user')

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

# Initialize database
def init_db():
    with app.app_context():
        db.create_all()

        # Seed data if empty
        if User.query.count() == 0:
            users = [
                User(username='admin', email='admin@techcorp.local', role='admin'),
                User(username='developer', email='john.dev@techcorp.local', role='developer'),
                User(username='pentester', email='pentester@techcorp.local', role='auditor')
            ]
            db.session.add_all(users)

            services = [
                Service(name='Penetration Testing', description='Professional security audits and vulnerability assessments'),
                Service(name='Security Consulting', description='Expert security guidance for your infrastructure'),
                Service(name='Incident Response', description='24/7 security incident handling and forensics')
            ]
            db.session.add_all(services)
            db.session.commit()
            print("Database initialized with seed data")

# Middleware - Add custom headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Powered-By'] = 'Flask/3.0.0'
    response.headers['X-TechCorp-Version'] = '2.1.4'
    response.headers['Server'] = 'nginx/1.24.0'
    return response

# Main Routes
@app.route('/')
def index():
    services = Service.query.all()
    return render_template('index.html', services=services)

@app.route('/about')
def about():
    users = User.query.all()
    return render_template('about.html', users=users)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/services')
def services():
    services = Service.query.all()
    return render_template('services.html', services=services)

# Public files - FLAG 1
@app.route('/robots.txt')
def robots():
    return send_from_directory('public', 'robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('public', 'sitemap.xml')

@app.route('/humans.txt')
def humans():
    return send_from_directory('public', 'humans.txt')

# Vulnerable endpoints - FLAG 2 (Backup files)
@app.route('/backup/<path:filename>')
def backup_files(filename):
    """Intentionally vulnerable - serves backup files"""
    return send_from_directory('backup', filename)

# Vulnerable endpoints - FLAG 3 (Exposed .git)
@app.route('/.git/<path:filename>')
def git_files(filename):
    """Intentionally vulnerable - serves .git files"""
    try:
        return send_from_directory('.git', filename)
    except:
        return "File not found", 404

# API v1 - Documented
@app.route('/api/v1/info')
def api_v1_info():
    return jsonify({
        'version': '1.0',
        'name': 'TechCorp API',
        'endpoints': [
            '/api/v1/info',
            '/api/v1/status'
        ],
        'documentation': '/api/v1/docs'
    })

@app.route('/api/v1/status')
def api_v1_status():
    return jsonify({
        'status': 'operational',
        'uptime': '99.9%',
        'services': ['web', 'api', 'database'],
        'version': '2.1.4'
    })

# API v2 - Undocumented - FLAG 4
@app.route('/api/v2/admin/users')
def api_v2_admin_users():
    """Intentionally undocumented endpoint - FLAG 4"""
    users = User.query.all()
    return jsonify({
        'flag': 'FLAG{api_v2_discovered_1e9f}',
        'message': 'Congratulations! You found the undocumented API endpoint.',
        'users': [
            {'id': u.id, 'username': u.username, 'email': u.email, 'role': u.role}
            for u in users
        ],
        'hint': 'Try enumerating subdomains: dev, staging, admin'
    })

@app.route('/api/v2/config')
def api_v2_config():
    """Another hidden endpoint that reveals environment info"""
    return jsonify({
        'environments': {
            'production': 'techcorp.local',
            'development': 'dev.techcorp.local',
            'staging': 'staging.techcorp.local',
            'admin': 'admin.techcorp.local'
        },
        'database': 'sqlite:///database.db',
        'secret_key': 'REDACTED'
    }), 403  # Forbidden but still reveals info

# Protected routes (return 401/403)
@app.route('/admin/')
def admin_route():
    return "Unauthorized - Admin access required", 401

@app.route('/secret/')
def secret_route():
    return "Forbidden - Access denied", 403

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # Initialize database on first run
    if not os.path.exists('database.db'):
        init_db()

    app.run(host='127.0.0.1', port=5000, debug=False)
