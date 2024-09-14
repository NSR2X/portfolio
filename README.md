# Quantin BODIN's Portfolio

This is a Flask-based web application for Quantin BODIN's portfolio, showcasing projects and blog posts.

## Features

- Project showcase
- Blog with markdown support
- Admin interface for content management
- Responsive design
- Security enhancements (CSRF protection, XSS prevention, etc.)
- SEO optimizations

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add the following:
   ```
   SECRET_KEY=your_secret_key
   ADMIN_USERNAME=your_admin_username
   ADMIN_PASSWORD=your_admin_password
   SHOW_ADMIN_LINK=False
   ```

5. Run the application:
   ```
   python app.py
   ```

## Usage

- Access the website at `http://localhost:5001`
- Admin interface is available at `/admin` (login required)

## Recent Updates

- Implemented CSRF protection for forms
- Enhanced XSS prevention measures
- Added lazy loading for images
- Improved error handling and logging
- Implemented proper meta tags for better SEO
- Added type hints for better code maintainability

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[CC-0](https://creativecommons.org/publicdomain/zero/1.0/deed.en)