# Personal Portfolio Website

A modern, responsive portfolio website built with Flask, featuring a blog, project showcase, and an admin panel for easy content management.

![Portfolio Screenshot](static/portfolio-screenshot.png)

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Customization](#customization)
7. [Deployment](#deployment)
8. [Contributing](#contributing)
9. [License](#license)

## Features

- Responsive design for various screen sizes
- Dynamic project showcase
- Integrated blog with Markdown support
- Admin panel for content management
- SEO-friendly structure
- Dark mode support
- Easy customization

## Prerequisites

- Python 3.7+
- pip (Python package manager)
- Git (optional, for cloning the repository)

## Installation

1. Clone the repository (or download and extract the ZIP file):
   ```
   git clone https://github.com/yourusername/portfolio-website.git
   cd portfolio-website
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Flask development server:
   ```
   python app.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`

3. To access the admin panel, go to `http://localhost:5000/admin`

## Customization

### Updating Personal Information

1. Edit the `templates/home.html` file to update your personal information, skills, and experience.

### Adding Projects

1. Create a new Markdown file in the `data/projects/` directory for each project.
2. Use the following format for project metadata:
   ```markdown
   ---
   title: Project Title
   description: Short project description
   image: /static/images/project-image.jpg
   github: https://github.com/yourusername/project
   website: https://project-demo.com
   state: Active
   ---

   Project content goes here...
   ```

### Adding Blog Posts

1. Create a new Markdown file in the `data/blog/` directory for each blog post.
2. Use the following format for blog post metadata:
   ```markdown
   ---
   title: Blog Post Title
   date: 2023-04-20
   image: /static/images/blog-post-image.jpg
   ---

   Blog post content goes here...
   ```

### Modifying the Design

1. Edit the `static/style.css` file to change the website's appearance.
2. Update the color scheme by modifying the CSS variables in the `:root` selector.

## Deployment

### Deploying to Heroku

1. Install the Heroku CLI and log in.
2. In the project root, run:
   ```
   heroku create your-app-name
   git push heroku main
   ```

### Deploying to a VPS

1. Set up a VPS with Python and Nginx.
2. Clone the repository to your server.
3. Set up a virtual environment and install dependencies.
4. Configure Nginx to proxy requests to your Flask app.
5. Use a process manager like Supervisor to keep your app running.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).