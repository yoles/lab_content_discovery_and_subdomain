from flask import Flask, render_template, jsonify
import sys
import os

app = Flask(__name__)

# Development configuration - INTENTIONALLY INSECURE
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret-dev-key-123'
app.config['ENV'] = 'development'
app.config['TESTING'] = False

# FLAG 5 - Dev Subdomain
FLAG = 'FLAG{dev_subdomain_pwned_5f2a}'

@app.route('/')
def index():
    """Main development environment page with FLAG and debug info"""
    debug_info = {
        'python_version': sys.version,
        'flask_version': '3.0.0',
        'flask_config': {
            'DEBUG': app.config['DEBUG'],
            'SECRET_KEY': app.config['SECRET_KEY'],
            'ENV': app.config['ENV'],
            'TESTING': app.config['TESTING']
        },
        'environment': 'development',
        'database': 'sqlite:///dev_database.db',
        'secret_key': app.config['SECRET_KEY'],
        'internal_api': 'http://dev.techcorp.local:8081/api/debug',
        'hint': 'Next: Try staging.techcorp.local and admin.techcorp.local'
    }

    return render_template('index.html',
                         flag=FLAG,
                         debug_info=debug_info)

@app.route('/debug')
def debug():
    """Debug endpoint with extensive information"""
    routes_list = [str(rule) for rule in app.url_map.iter_rules()]

    return jsonify({
        'flag': FLAG,
        'message': 'Development environment - Debug mode ENABLED',
        'routes': routes_list,
        'config': {k: str(v) for k, v in app.config.items()},
        'environment_variables': {
            'FLASK_ENV': os.environ.get('FLASK_ENV', 'development'),
            'FLASK_DEBUG': os.environ.get('FLASK_DEBUG', '1'),
            'PATH': os.environ.get('PATH', 'N/A')[:100] + '...'
        },
        'system_info': {
            'python_version': sys.version,
            'platform': sys.platform,
            'executable': sys.executable
        }
    })

@app.route('/api/status')
def api_status():
    """Dev API status endpoint"""
    return jsonify({
        'status': 'development',
        'debug': True,
        'environment': 'dev',
        'endpoints': [
            '/debug',
            '/api/status',
            '/config'
        ]
    })

@app.route('/config')
def config():
    """Expose configuration (dangerous in production!)"""
    return jsonify({
        'flag': FLAG,
        'configuration': {
            'SECRET_KEY': app.config['SECRET_KEY'],
            'DEBUG': app.config['DEBUG'],
            'DATABASE_URI': 'sqlite:///dev_database.db',
            'ALLOWED_HOSTS': ['dev.techcorp.local', 'localhost'],
            'ADMIN_EMAIL': 'john.dev@techcorp.local',
            'STAGING_URL': 'http://staging.techcorp.local:8082',
            'ADMIN_PORTAL': 'http://admin.techcorp.local:8083'
        }
    })

# Add custom headers - revealing debug mode
@app.after_request
def add_debug_headers(response):
    response.headers['X-Debug-Mode'] = 'enabled'
    response.headers['X-Environment'] = 'development'
    response.headers['X-Flask-Debug'] = 'true'
    response.headers['X-Developer'] = 'john.dev@techcorp.local'
    response.headers['X-Internal-IP'] = '10.0.0.15'
    return response

# Error handlers that reveal too much information
@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'error': '404 Not Found',
        'message': str(e),
        'available_routes': [str(rule) for rule in app.url_map.iter_rules()],
        'hint': 'This is a development environment - all routes are listed above'
    }), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        'error': '500 Internal Server Error',
        'message': str(e),
        'debug_mode': True,
        'traceback': 'Full traceback would appear here in dev mode'
    }), 500

if __name__ == '__main__':
    print("=" * 60)
    print("TechCorp Development Environment")
    print("=" * 60)
    print(f"FLAG: {FLAG}")
    print(f"Environment: {app.config['ENV']}")
    print(f"Debug Mode: {app.config['DEBUG']}")
    print(f"Secret Key: {app.config['SECRET_KEY']}")
    print("=" * 60)
    print("Starting Flask development server on port 5001...")
    print("Access: http://dev.techcorp.local:8081")
    print("=" * 60)

    app.run(host='127.0.0.1', port=5001, debug=True)
