Flask-based portfolio, showcasing projects and blog posts, integrating an RSS feed.

## Features

Discover a powerful and versatile portfolio solution with these outstanding features:

- **Dynamic Project Showcase**: Impress visitors with an elegant display of your work, highlighting your skills and accomplishments.
- **Rich Content Blog**: Share your insights and expertise through a fully-featured blog with Markdown support, allowing for beautifully formatted and easy-to-write posts.
- **Streamlined Content Management**: Take control of your content with an intuitive admin interface, making updates and additions a breeze.
- **RSS Feed**: Stay connected with your audience through an RSS feed for your blog posts, ensuring they never miss an update.
- **Responsive Design**: Ensure a flawless user experience across all devices with a sleek, mobile-friendly layout.
- **Robust Security Measures**: Rest easy knowing your site is protected with advanced security features like CSRF protection and XSS prevention.
- **SEO Optimization**: Boost your online visibility and attract more visitors with built-in SEO enhancements.
- **Flask-Powered Performance**: Leverage the speed and flexibility of Flask, a modern Python web framework, for optimal site performance.
- **Customizable and Extensible**: Easily adapt the portfolio to your unique style and needs, with room for future growth and feature additions.

Elevate your online presence with this feature-rich portfolio solution, designed to showcase your talents and engage your audience effectively.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/NSR2X/portfolio.git
   cd portfolio
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

4. Create a `.env` file from `.env.example` in the root directory and add the following:
   ```
   SECRET_KEY="your_secret_key"
   ADMIN_USERNAME="your_admin_username"
   ADMIN_PASSWORD="your_admin_password"
   SHOW_ADMIN_LINK=False
   LAST_BUILD_DATE_FILE="/data/blog/last_build_date"
   ```

5. Run the application:
   ```
   python app.py
   ```

## Usage

- Home page is available at `/`
- Admin interface is available at `/admin` (login required)
- Blog posts are available at `/blog`
- Projects are available at `/projects`
- RSS feed is available at `/rss`
- Sitemap is available at `/sitemap.xml`
- Upload blog posts and projects in markdown format from the admin interface, **if you want them to be available in the RSS feed.**

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[CC-0](https://creativecommons.org/publicdomain/zero/1.0/deed.en)