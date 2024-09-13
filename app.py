from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
import markdown
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from markupsafe import Markup
import textwrap
from flask_talisman import Talisman
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from config import ADMIN_USERNAME, ADMIN_PASSWORD

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
Talisman(app, content_security_policy=None, force_https=False)

auth = HTTPBasicAuth()

users = {
    ADMIN_USERNAME: generate_password_hash(ADMIN_PASSWORD)
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

# Ensure data directory exists
os.makedirs('data', exist_ok=True)
os.makedirs('data/projects', exist_ok=True)
os.makedirs('data/blog', exist_ok=True)

def get_metadata_and_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        metadata = {}
        content_start = 0
        for i, line in enumerate(lines):
            if line.strip() == '---':
                content_start = i + 1
                break
            key, value = line.strip().split(': ', 1)
            metadata[key] = value
        content = ''.join(lines[content_start:])
        
        # Add clickable icons for GitHub and website links
        github_icon = '<i class="fab fa-github"></i>'
        website_icon = '<i class="fas fa-globe"></i>'
        
        if 'github' in metadata:
            metadata['github'] = Markup(f'<a href="{metadata["github"]}" target="_blank">{github_icon}</a>')
        if 'website' in metadata:
            metadata['website'] = Markup(f'<a href="{metadata["website"]}" target="_blank">{website_icon}</a>')
        
        # Ensure 'image' and 'description' keys exist in metadata
        if 'image' not in metadata:
            metadata['image'] = ''
        if 'description' not in metadata:
            metadata['description'] = ''
        
        return metadata, markdown.markdown(content)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/projects')
def project_page():
    projects = []
    projects_dir = 'data/projects'
    for filename in os.listdir(projects_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(projects_dir, filename)
            metadata, content = get_metadata_and_content(file_path)
            projects.append({**metadata, 'content': content, 'filename': filename})
    return render_template('projects.html', projects=projects)

@app.route('/blog')
def blog_page():
    posts = []
    blog_dir = 'data/blog'
    for filename in os.listdir(blog_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(blog_dir, filename)
            metadata, content = get_metadata_and_content(file_path)
            
            # Ensure 'image' key exists in metadata
            if 'image' not in metadata:
                metadata['image'] = ''
            
            posts.append({**metadata, 'content': content, 'filename': filename})
    # Ensure 'date' key exists in metadata before sorting
    posts.sort(key=lambda x: datetime.strptime(x.get('date', '1900-01-01'), '%Y-%m-%d'), reverse=True)
    return render_template('blog.html', posts=posts)

@app.route('/admin')
@auth.login_required
def admin():
    projects = os.listdir('data/projects')
    blog_posts = os.listdir('data/blog')
    return render_template('admin.html', projects=projects, blog_posts=blog_posts)

@app.route('/add/<file_type>', methods=['POST'])
@auth.login_required
def add_file(file_type):
    if file_type not in ['project', 'blog']:
        return redirect(url_for('admin'))
    
    file = request.files['file']
    if file and file.filename.endswith('.md'):
        filename = secure_filename(file.filename)
        # Use 'projects' instead of 'project'
        directory = os.path.join('data', file_type + 's')
        
        # Ensure the directory exists
        os.makedirs(directory, exist_ok=True)
        
        file_path = os.path.join(directory, filename)
        file.save(file_path)
    return redirect(url_for('admin'))

@app.route('/delete/<file_type>/<path:filename>')
@auth.login_required
def delete_file(file_type, filename):
    if file_type == 'project':
        file_path = os.path.join('data/projects', filename)
    elif file_type == 'blog':
        file_path = os.path.join('data/blog', filename)
    else:
        return redirect(url_for('admin'))
    
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect(url_for('admin'))

@app.route('/edit/<file_type>/<path:filename>', methods=['GET', 'POST'])
@auth.login_required
def edit_file(file_type, filename):
    if file_type == 'project':
        file_path = os.path.join('data/projects', filename)
    elif file_type == 'blog':
        file_path = os.path.join('data/blog', filename)
    else:
        return redirect(url_for('admin'))

    if request.method == 'POST':
        content = request.form['content']
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return redirect(url_for('admin'))
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    return render_template('edit_file.html', content=content, file_type=file_type, filename=filename)

@app.route('/blog/<path:filename>')
def blog_post(filename):
    file_path = os.path.join('data/blog', filename)
    if not os.path.exists(file_path):
        abort(404)
    metadata, content = get_metadata_and_content(file_path)
    return render_template('blog_post.html', post=metadata, content=content)

@app.route('/blog/<path:filename>/content')
def blog_post_content(filename):
    file_path = os.path.join('data/blog', filename)
    if not os.path.exists(file_path):
        abort(404)
    metadata, content = get_metadata_and_content(file_path)
    return jsonify({
        'title': metadata.get('title', ''),
        'date': metadata.get('date', ''),
        'content': content
    })

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)