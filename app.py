import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from database import init_db
from seed import seed_data
from auth import auth_bp
from routes.admin import admin_bp
from routes.teacher import teacher_bp
from routes.student import student_bp
from routes.shared import shared_bp

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Vercel specific configuration
is_vercel = os.environ.get('VERCEL') == '1'

if is_vercel:
    os.environ['DATABASE_PATH'] = '/tmp/eduflow.db'
    UPLOAD_FOLDER = '/tmp/uploads'
    
    # Initialize and seed database on cold start in Vercel's /tmp dir
    if not os.path.exists('/tmp/eduflow.db'):
        try:
            init_db()
            seed_data()
        except Exception as e:
            print(f"Error initializing database on Vercel: {e}")
else:
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')

try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
except Exception as e:
    print(f"Could not create upload folder: {e}")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20 MB limit

# Register blueprints
from routes.taxonomy_mongo import taxonomy_bp
app.register_blueprint(taxonomy_bp, url_prefix='/api/taxonomy')
app.register_blueprint(auth_bp,    url_prefix='/api/auth')
app.register_blueprint(admin_bp,   url_prefix='/api/admin')
app.register_blueprint(teacher_bp, url_prefix='/api/teacher')
app.register_blueprint(student_bp, url_prefix='/api/student')
app.register_blueprint(shared_bp,  url_prefix='/api/shared')

@app.route('/api/uploads/<path:filename>')
def serve_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/proxy-pdf')
def proxy_pdf():
    from flask import request, Response
    import urllib.request
    url = request.args.get('url')
    if not url:
        return "No url provided", 400
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            return Response(response.read(), mimetype='application/pdf')
    except Exception as e:
        return str(e), 500

@app.route('/')
def index():
    return {'message': 'EduFlow API is running', 'version': '2.0'}

if __name__ == '__main__':
    print("Initializing database...")
    init_db()
    print("Seeding data...")
    seed_data()
    port = int(os.getenv('PORT', 5000))
    print(f"Starting EduFlow API on port {port}...")
    app.run(debug=True, port=port)
