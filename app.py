from flask import Flask, render_template, request, jsonify, redirect, url_for, abort
from flask_wtf.csrf import CSRFProtect
import json
import uuid
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)  # Generate a random secret key
csrf = CSRFProtect(app)

# Store projects in memory (in a real application, use a database)
projects = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/projects')
def project_list():
    return render_template('projects.html', projects=projects)

@app.route('/create_project', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        project_name = request.form.get('project_name')
        if not project_name:
            return jsonify({"error": "Project name is required"}), 400
        project_id = str(uuid.uuid4())
        projects[project_id] = {
            'name': project_name,
            'schema': {},
            'landing_pages': []
        }
        return redirect(url_for('edit_project', project_id=project_id))
    return render_template('create_project.html')

@app.route('/project/<project_id>')
def edit_project(project_id):
    project = projects.get(project_id)
    if not project:
        abort(404, description="Project not found")
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(project)
    return render_template('edit_project.html', project=project, project_id=project_id)

@app.route('/generate_schema', methods=['POST'])
@csrf.exempt  # Exempt this route from CSRF protection as it's handled by AJAX
def generate_schema():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    project_id = data.get('project_id')
    
    schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": data.get('name', ''),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": data.get('streetAddress', ''),
            "addressLocality": data.get('city', ''),
            "addressRegion": data.get('state', ''),
            "postalCode": data.get('postalCode', ''),
            "addressCountry": data.get('country', '')
        },
        "telephone": data.get('telephone', ''),
        "url": data.get('website', '')
    }
    
    if project_id:
        if project_id not in projects:
            return jsonify({"error": "Project not found"}), 404
        projects[project_id]['schema'] = schema
        
        # Add landing pages to the schema
        landing_pages = projects[project_id]['landing_pages']
        if landing_pages:
            schema['subpage'] = [{"@id": page['url']} for page in landing_pages]
    
    return jsonify(schema)

@app.route('/add_landing_page/<project_id>', methods=['POST'])
def add_landing_page(project_id):
    project = projects.get(project_id)
    if not project:
        abort(404, description="Project not found")
    page_name = request.form.get('page_name')
    page_url = request.form.get('page_url')
    if not page_name or not page_url:
        return jsonify({"error": "Both page name and URL are required"}), 400
    project['landing_pages'].append({'name': page_name, 'url': page_url})
    return redirect(url_for('edit_project', project_id=project_id))

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": str(error)}), 404

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({"error": str(error)}), 400

if __name__ == '__main__':
    app.run(debug=True)  # Set debug to True for development to see detailed error messages