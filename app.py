import os
import re
import logging
import io
import validators
from datetime import datetime, timezone, timedelta
from typing import Dict, Tuple, List, Any, Optional, Union

import pytz
import bleach
import markdown
from dotenv import load_dotenv
from lxml import etree
from feedgen.feed import FeedGenerator
from markupsafe import Markup, escape
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException
import json

from flask import Flask, render_template, request, redirect, url_for, abort, jsonify, make_response
from flask_talisman import Talisman
from flask_httpauth import HTTPBasicAuth
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from flask_sitemap import Sitemap
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import TextAreaField, SubmitField
from markdown.extensions.fenced_code import FencedCodeExtension

# Constants
DATA_DIR: str = 'data'
PROJECTS_DIR: str = os.path.join(DATA_DIR, 'projects')
BLOG_DIR: str = os.path.join(DATA_DIR, 'blog')
MAX_FILENAME_LENGTH: int = 255
ALLOWED_FILE_TYPES: List[str] = ['project', 'blog']
ALLOWED_TAGS: List[str] = ['p', 'br', 'strong', 'em', 'h1', 'h2', 'h3', 'ul', 'ol', 'li', 'a', 'img', 'blockquote', 'pre', 'code']
ALLOWED_ATTRIBUTES: Dict[str, List[str]] = {'a': ['href', 'title'], 'img': ['src', 'alt', 'loading']}
DATE_FORMAT: str = '%Y-%m-%d'

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
csrf = CSRFProtect(app)

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Update Talisman configuration
Talisman(app, 
         content_security_policy={
             'default-src': "'self'",
             'script-src': ["'self'", "'unsafe-inline'", 'https://www.googletagmanager.com'],
             'style-src': ["'self'", "'unsafe-inline'", 'https://cdnjs.cloudflare.com'],
             'img-src': ["'self'", 'data:', 'https:'],
             'font-src': ["'self'", 'https://cdnjs.cloudflare.com'],
         },
         force_https=False,
         session_cookie_secure=True,
         session_cookie_http_only=True)

# Update this line
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

auth = HTTPBasicAuth()

# Use environment variables
ADMIN_USERNAME: str = os.getenv('ADMIN_USERNAME', '')
ADMIN_PASSWORD: str = os.getenv('ADMIN_PASSWORD', '')
SHOW_ADMIN_LINK: bool = os.getenv('SHOW_ADMIN_LINK', 'False').lower() == 'true'

users: Dict[str, str] = {
    ADMIN_USERNAME: generate_password_hash(ADMIN_PASSWORD)
}

@auth.verify_password
def verify_password(username: str, password: str) -> Optional[str]:
    if username in users and check_password_hash(users.get(username, ''), password):
        return username
    return None

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PROJECTS_DIR, exist_ok=True)
os.makedirs(BLOG_DIR, exist_ok=True)

def sanitize_filename(filename: str) -> str:
    filename = filename[:MAX_FILENAME_LENGTH]
    return secure_filename(re.sub(r'[^a-zA-Z0-9_.-]', '', filename))

def validate_metadata(metadata: Dict[str, Any], file_type: str) -> bool:
    required_fields: List[str] = ['title']
    if file_type == 'blog':
        required_fields.append('date')
    
    for field in required_fields:
        if field not in metadata or not metadata[field]:
            raise ValueError(f"Missing required field: {field}")
    
    if 'date' in metadata:
        try:
            datetime.strptime(metadata['date'], DATE_FORMAT)
        except ValueError:
            raise ValueError(f"Invalid date format. Expected {DATE_FORMAT}")
    
    for url_field in ['github', 'website']:
        if url_field in metadata and metadata[url_field]:
            if not validators.url(metadata[url_field]):
                raise ValueError(f"Invalid URL for {url_field}")
    
    return True

def get_metadata_and_content(file_path: str, file_type: str) -> Tuple[Dict[str, Any], str]:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines: List[str] = file.readlines()
            metadata: Dict[str, Any] = {}
            content_start: int = 0
            for i, line in enumerate(lines):
                if line.strip() == '---':
                    content_start = i + 1
                    break
                try:
                    key, value = line.strip().split(': ', 1)
                    metadata[key] = value
                except ValueError:
                    continue
            
            if not validate_metadata(metadata, file_type):
                raise ValueError("Invalid metadata")
            
            content: str = ''.join(lines[content_start:])
            
            github_icon: str = '<i class="fab fa-github"></i>'
            website_icon: str = '<i class="fas fa-globe"></i>'
            
            if 'github' in metadata:
                metadata['github'] = Markup(f'<a href="{bleach.clean(metadata["github"], strip=True)}" target="_blank">{github_icon}</a>')
            if 'website' in metadata:
                metadata['website'] = Markup(f'<a href="{bleach.clean(metadata["website"], strip=True)}" target="_blank">{website_icon}</a>')
            
            metadata.setdefault('image', '')
            metadata.setdefault('description', '')
            
            # Use markdown with extensions to properly render quotes and code blocks
            md = markdown.Markdown(extensions=['fenced_code', 'codehilite'])
            content_html = md.convert(content)
            
            # Apply bleach cleaning after Markdown conversion
            content_html = bleach.clean(content_html, tags=ALLOWED_TAGS + ['blockquote', 'pre', 'code'], attributes=ALLOWED_ATTRIBUTES)
            content_html = content_html.replace('<img', '<img loading="lazy"')
            
            return metadata, Markup(content_html)
    except FileNotFoundError:
        app.logger.error(f"File not found: {file_path}")
        raise
    except IOError as e:
        app.logger.error(f"IO error reading file {file_path}: {str(e)}")
        raise
    except Exception as e:
        app.logger.error(f"Unexpected error processing file {file_path}: {str(e)}")
        raise

@app.route('/')
def home() -> str:
    return render_template('home.html')

@app.route('/projects')
@limiter.limit("30 per minute")
def project_page() -> Union[str, Tuple[str, int]]:
    projects: List[Dict[str, Any]] = []
    active_projects: List[Dict[str, Any]] = []
    other_projects: List[Dict[str, Any]] = []
    try:
        for filename in os.listdir(PROJECTS_DIR):
            if filename.endswith('.md'):
                file_path: str = os.path.join(PROJECTS_DIR, filename)
                try:
                    metadata, content = get_metadata_and_content(file_path, 'project')
                    project: Dict[str, Any] = {**metadata, 'content': content, 'filename': filename}
                    if metadata.get('state', '').lower() == 'active':
                        active_projects.append(project)
                    else:
                        other_projects.append(project)
                except Exception as e:
                    app.logger.error(f"Error processing project file {filename}: {str(e)}")
                    error_project: Dict[str, Any] = {
                        'title': f"Error in {filename}",
                        'content': f"There was an error processing this project: {str(e)}",
                        'filename': filename,
                        'state': 'error'
                    }
                    other_projects.append(error_project)
        
        active_projects.sort(key=lambda x: x.get('title', '').lower())
        projects = active_projects + other_projects
        
        return render_template('projects.html', projects=projects)
    except Exception as e:
        app.logger.error(f"Error accessing projects directory: {str(e)}")
        return render_template('error.html', error="Unable to load projects at this time."), 500

@app.route('/blog')
@limiter.limit("30 per minute")
def blog_page(filename: Optional[str] = None) -> Union[str, Tuple[str, int]]:
    if filename:
        return blog_post(filename)
    
    posts: List[Dict[str, Any]] = []
    try:
        for file in os.listdir(BLOG_DIR):
            if file.endswith('.md'):
                file_path: str = os.path.join(BLOG_DIR, file)
                metadata, content = get_metadata_and_content(file_path, 'blog')
                
                if 'image' not in metadata:
                    metadata['image'] = ''
                
                posts.append({**metadata, 'content': content, 'filename': file})
        posts.sort(key=lambda x: datetime.strptime(x.get('date', '1900-01-01'), DATE_FORMAT), reverse=True)
        return render_template('blog.html', posts=posts)
    except Exception as e:
        app.logger.error(f"Error accessing blog directory: {str(e)}")
        return render_template('error.html', error="Unable to load blog posts at this time."), 500

@app.route('/blog/<path:filename>')
@limiter.limit("10 per minute")
def blog_post(filename: str) -> Union[str, Tuple[str, int]]:
    filename = sanitize_filename(filename)
    if not filename:
        abort(400, description="Invalid filename")
    
    file_path: str = os.path.join(BLOG_DIR, filename)
    if not os.path.exists(file_path):
        abort(404)
    
    try:
        metadata, content = get_metadata_and_content(file_path, 'blog')
        post: Dict[str, Any] = {**metadata, 'content': content, 'filename': filename}
        
        best: str = request.accept_mimetypes.best_match(['text/html', 'application/json', 'application/rss+xml'])
        
        if best == 'application/json':
            return jsonify({k: escape(v) if isinstance(v, str) else v for k, v in post.items()})
        elif best == 'application/rss+xml':
            fg = FeedGenerator()
            fg.title(escape(post['title']))
            fg.description(escape(post.get('description', '')))
            fg.link(href=request.url)
            fg.language('en')

            fe = fg.add_entry()
            fe.title(escape(post['title']))
            fe.link(href=request.url)
            fe.description(markdown.markdown(escape(post['content'])))
            fe.guid(request.url, permalink=True)
            fe.pubDate(pytz.utc.localize(datetime.strptime(post['date'], DATE_FORMAT)))

            response = make_response(fg.rss_str(pretty=True))
            response.headers.set('Content-Type', 'application/rss+xml')
            return response
        else:  # Default to HTML
            return render_template('blog_post.html', post={k: escape(v) if isinstance(v, str) else v for k, v in post.items()})
    except Exception as e:
        app.logger.error(f"Error processing blog post {filename}: {str(e)}")
        return render_template('error.html', error="Unable to load blog post at this time."), 500

@app.route('/admin', methods=['GET', 'POST'])
@auth.login_required
@limiter.limit("5 per minute")
def admin() -> str:
    projects: List[str] = os.listdir(PROJECTS_DIR)
    blog_posts: List[str] = os.listdir(BLOG_DIR)
    form = AddFileForm()  # Create an instance of the form
    return render_template('admin.html', projects=projects, blog_posts=blog_posts, form=form)

class AddFileForm(FlaskForm):
    file = FileField('File', validators=[FileRequired(), FileAllowed(['md'], 'Markdown files only!')])
    submit = SubmitField('Upload')

@app.route('/add/<file_type>', methods=['GET', 'POST'])
@auth.login_required
@limiter.limit("5 per minute")
def add_file(file_type: str) -> Union[str, Tuple[str, int]]:
    if file_type not in ALLOWED_FILE_TYPES:
        abort(400, description="Invalid file type")
    
    form = AddFileForm()
    
    if form.validate_on_submit():
        file = form.file.data
        filename: str = sanitize_filename(file.filename)
        if not filename:
            abort(400, description="Invalid filename")
        
        directory: str = PROJECTS_DIR if file_type == 'project' else BLOG_DIR
        os.makedirs(directory, exist_ok=True)
        file_path: str = os.path.join(directory, filename)
        
        try:
            content: str = file.read().decode('utf-8')
            
            # Validate metadata
            lines = content.split('\n')
            metadata = {}
            content_start = 0
            for i, line in enumerate(lines):
                if line.strip() == '---':
                    content_start = i + 1
                    break
                try:
                    key, value = line.strip().split(': ', 1)
                    metadata[key] = value
                except ValueError:
                    continue
            
            if not validate_metadata(metadata, file_type):
                raise ValueError("Invalid metadata")
            
            sanitized_content: str = bleach.clean(content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(sanitized_content)
            
            if file_type == 'blog':
                update_last_build_date()
            
            return redirect(url_for('admin'))
        except ValueError as e:
            app.logger.error(f"Validation error when adding {file_type} file: {str(e)}")
            abort(400, description=str(e))
        except IOError as e:
            app.logger.error(f"IO error when adding {file_type} file: {str(e)}")
            abort(500, description="Error saving file")
        except Exception as e:
            app.logger.error(f"Unexpected error when adding {file_type} file: {str(e)}")
            abort(500, description="Unexpected error occurred")
    
    # If it's a GET request or form validation failed, render the admin page
    projects: List[str] = os.listdir(PROJECTS_DIR)
    blog_posts: List[str] = os.listdir(BLOG_DIR)
    return render_template('admin.html', projects=projects, blog_posts=blog_posts, form=form)

@app.route('/delete/<file_type>/<path:filename>')
@auth.login_required
def delete_file(file_type: str, filename: str) -> Union[str, Tuple[str, int]]:
    if file_type not in ALLOWED_FILE_TYPES:
        abort(400, description="Invalid file type")
    
    filename = sanitize_filename(filename)
    if not filename:
        abort(400, description="Invalid filename")
    
    directory: str = PROJECTS_DIR if file_type == 'project' else BLOG_DIR
    file_path: str = os.path.join(directory, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect(url_for('admin'))

class EditFileForm(FlaskForm):
    content = TextAreaField('Content')

@app.route('/edit/<file_type>/<path:filename>', methods=['GET', 'POST'])
@auth.login_required
@limiter.limit("10 per minute")
def edit_file(file_type: str, filename: str) -> Union[str, Tuple[str, int]]:
    logging.info(f"Attempting to edit file: {file_type}/{filename}")
    if file_type not in ALLOWED_FILE_TYPES:
        abort(400, description="Invalid file type")
    
    filename = sanitize_filename(filename)
    if not filename:
        abort(400, description="Invalid filename")
    
    directory: str = PROJECTS_DIR if file_type == 'project' else BLOG_DIR
    file_path: str = os.path.join(directory, filename)
    
    if not os.path.exists(file_path):
        abort(404, description=f"File not found: {filename}")

    form = EditFileForm()

    if form.validate_on_submit():
        content = form.content.data
        
        try:
            # Validate metadata without using get_metadata_and_content
            lines = content.split('\n')
            metadata = {}
            content_start = 0
            for i, line in enumerate(lines):
                if line.strip() == '---':
                    content_start = i + 1
                    break
                try:
                    key, value = line.strip().split(': ', 1)
                    metadata[key] = value
                except ValueError:
                    continue
            
            if not validate_metadata(metadata, file_type):
                raise ValueError("Invalid metadata")
            
            sanitized_content = bleach.clean(content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(sanitized_content)
            update_last_build_date()
            return redirect(url_for('admin'))
        except ValueError as e:
            abort(400, description=str(e))
        except Exception as e:
            app.logger.error(f"Error processing file {filename}: {str(e)}")
            abort(500, description="An unexpected error occurred while processing the file")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            form.content.data = file.read()
    except IOError:
        abort(500, description=f"Error reading file: {filename}")
    
    return render_template('edit_file.html', form=form, file_type=file_type, filename=filename)

@app.route('/blog/<path:filename>/content')
def blog_post_content(filename: str) -> Any:
    filename = sanitize_filename(filename)
    if not filename:
        abort(400, description="Invalid filename")
    
    file_path = os.path.join(BLOG_DIR, filename)
    if not os.path.exists(file_path):
        abort(404)
    metadata, content = get_metadata_and_content(file_path, 'blog')
    
    return jsonify({
        'title': escape(metadata.get('title', '')),
        'date': escape(metadata.get('date', '')),
        'content': content
    })

@app.route('/blog/posts')
@limiter.limit("20 per minute")
def blog_posts() -> Any:
    page = max(1, int(request.args.get('page', 1)))
    per_page = max(1, min(20, int(request.args.get('per_page', 5))))  # Limit per_page between 1 and 20
    
    all_posts: List[Dict[str, Any]] = []
    for filename in os.listdir(BLOG_DIR):
        if filename.endswith('.md'):
            file_path = os.path.join(BLOG_DIR, filename)
            metadata, content = get_metadata_and_content(file_path, 'blog')
            all_posts.append({
                **{k: escape(v) if isinstance(v, str) else v for k, v in metadata.items()},
                'content': content,
                'filename': escape(filename),
                'image': escape(metadata.get('image', ''))  # Ensure image is included
            })
    
    all_posts.sort(key=lambda x: datetime.strptime(x.get('date', '1900-01-01'), DATE_FORMAT), reverse=True)
    total_posts = len(all_posts)
    paginated_posts = all_posts[(page-1)*per_page:page*per_page]
    
    return jsonify({
        'posts': paginated_posts,
        'total_posts': total_posts,
        'page': page,
        'per_page': per_page
    })

def get_blog_posts():
    posts = []
    for filename in os.listdir(BLOG_DIR):
        if filename.endswith('.md'):
            file_path = os.path.join(BLOG_DIR, filename)
            metadata, content = get_metadata_and_content(file_path, 'blog')
            posts.append({
                'id': filename[:-3],  # Remove .md extension
                'title': escape(metadata.get('title', '')),
                'date': escape(metadata.get('date', '')),
                'content': content
            })
    return sorted(posts, key=lambda x: datetime.strptime(x['date'], DATE_FORMAT), reverse=True)

LAST_BUILD_DATE_FILE = os.getenv('LAST_BUILD_DATE_FILE', os.path.join(BLOG_DIR, 'last_build_date'))

def get_last_build_date():
    if os.path.exists(LAST_BUILD_DATE_FILE):
        with open(LAST_BUILD_DATE_FILE, 'r') as f:
            date_str = f.read().strip()
            if date_str:
                return datetime.fromisoformat(date_str)
    return datetime.now(timezone.utc)

def update_last_build_date():
    os.makedirs(os.path.dirname(LAST_BUILD_DATE_FILE), exist_ok=True)
    with open(LAST_BUILD_DATE_FILE, 'w') as f:
        f.write(datetime.now(timezone.utc).isoformat())

@app.route('/rss')
@limiter.limit("10 per minute")
def rss_feed():
    fg = FeedGenerator()
    fg.title('Quantin BODIN\'s Blog')
    fg.description('Lead DevSecOps showcasing projects and blog posts IT and technology.')
    fg.link(href=request.url_root)
    fg.language('en')

    fg.link(href=url_for('rss_feed', _external=True), rel='self')

    posts = get_blog_posts()
    last_build_date = get_last_build_date()
    
    fg.lastBuildDate(last_build_date)
    
    for post in posts:
        fe = fg.add_entry()
        fe.title(escape(post['title']))
        post_url = url_for('blog_page', filename=f"{post['id']}.md", _external=True)
        fe.link(href=post_url)
        fe.description(post['content'])  # Full content as description
        
        fe.guid(post_url, permalink=True)
        
        post_date = datetime.strptime(post['date'], '%Y-%m-%d')
        post_date_with_tz = pytz.utc.localize(post_date)
        fe.pubDate(post_date_with_tz)

    response = make_response(fg.rss_str(pretty=True))
    response.headers.set('Content-Type', 'application/rss+xml')

    # Remove generator information
    xml = etree.fromstring(response.get_data())
    for generator in xml.xpath('//generator'):
        generator.getparent().remove(generator)
    response.set_data(etree.tostring(xml, pretty_print=True))

    return response

@app.after_request
def add_security_headers(response: Any) -> Any:
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@app.context_processor
def inject_show_admin() -> Dict[str, bool]:
    return dict(show_admin=SHOW_ADMIN_LINK)

@app.context_processor
def inject_favicon():
    return dict(favicon_url=url_for('static', filename='favicon.ico'))

# Add this near the top of your file, after the imports
logging.basicConfig(level=logging.INFO)

@app.route('/sitemap.xml')
def sitemap():
    logging.info("Sitemap function called")
    try:
        pages = []
        current_time = datetime.now().strftime("%Y-%m-%d")
        
        # Add static pages
        pages.append([url_for('home', _external=True, _scheme='https'), current_time])
        pages.append([url_for('project_page', _external=True, _scheme='https'), current_time])
        pages.append([url_for('blog_page', _external=True, _scheme='https'), current_time])
        
        # Add dynamic pages
        # Add blog posts
        for post in get_blog_posts():
            pages.append([url_for('blog_page', filename=f"{post['id']}.md", _external=True, _scheme='https'), current_time])

        # Add project pages
        for filename in os.listdir(PROJECTS_DIR):
            if filename.endswith('.md'):
                pages.append([url_for('project_page', filename=filename, _external=True, _scheme='https'), current_time])

        logging.info(f"Pages to be included in sitemap: {pages}")

        sitemap_xml = render_template('sitemap_template.xml', pages=pages)
        response = make_response(sitemap_xml)
        response.headers["Content-Type"] = "application/xml"    

        logging.info(f"Sitemap generated with {len(pages)} pages")
        logging.info(f"Sitemap content: {sitemap_xml}")
        return response
    except Exception as e:
        logging.error(f"Error generating sitemap: {str(e)}")
        return "Error generating sitemap", 500

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": escape(e.name),
        "description": escape(e.description),
    })
    response.content_type = "application/json"
    return response

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 page."""
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({"error": "Not found", "code": 404})
        response.status_code = 404
        return response
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Custom 500 page."""
    app.logger.error('An internal error occurred: %s', str(e))
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({"error": "Internal server error", "code": 500})
        response.status_code = 500
        return response
    return render_template('500.html'), 500

@app.errorhandler(Exception)
def handle_unexpected_error(error):
    app.logger.error('An unexpected error has occurred: %s', str(error))
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({
            'error': 'An unexpected error occurred',
            'description': escape(str(error))
        })
        response.status_code = 500
        return response
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)