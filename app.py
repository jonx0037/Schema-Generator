from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import uuid

app = Flask(__name__)

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
        project_id = str(uuid.uuid4())
        project_name = request.form.get('project_name')
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
    if project:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(project)
        return render_template('edit_project.html', project=project, project_id=project_id)
    return "Project not found", 404

@app.route('/generate_schema', methods=['POST'])
def generate_schema():
    data = request.json
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
        projects[project_id]['schema'] = schema
        
        # Add landing pages to the schema
        landing_pages = projects[project_id]['landing_pages']
        if landing_pages:
            schema['subpage'] = [{"@id": page['url']} for page in landing_pages]
    
    return jsonify(schema)

@app.route('/add_landing_page/<project_id>', methods=['POST'])
def add_landing_page(project_id):
    project = projects.get(project_id)
    if project:
        page_name = request.form.get('page_name')
        page_url = request.form.get('page_url')
        project['landing_pages'].append({'name': page_name, 'url': page_url})
        return redirect(url_for('edit_project', project_id=project_id))
    return "Project not found", 404

if __name__ == '__main__':
    app.run(debug=True)