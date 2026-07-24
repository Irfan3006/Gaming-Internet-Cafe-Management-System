from flask import Flask, session, redirect, url_for, request
from config import Config
from models.warnet import Warnet
from routes import (
    dashboard_bp,
    komputer_bp,
    pelanggan_bp,
    penyewaan_bp,
    transaksi_bp,
    laporan_bp,
    log_bp
)
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.warnet_system = Warnet(Config)

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(komputer_bp)
    app.register_blueprint(pelanggan_bp)
    app.register_blueprint(penyewaan_bp)
    app.register_blueprint(transaksi_bp)
    app.register_blueprint(laporan_bp)
    app.register_blueprint(log_bp)

    @app.template_filter('rupiah')
    def rupiah_filter(value):
        try:
            val = float(value)
            formatted = f"{val:,.0f}".replace(",", ".")
            return f"Rp {formatted}"
        except (ValueError, TypeError):
            return f"Rp {value}"

    @app.template_filter('datetime_format')
    def datetime_format_filter(value):
        if not value:
            return ""
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return value
        return value.strftime("%d/%m/%Y %H:%M")

    @app.before_request
    def check_login():
        allowed_paths = ['/', '/login', '/simpan-kontak', '/robots.txt', '/sitemap.xml', '/llms.txt']
        if request.path not in allowed_paths and not request.path.startswith('/static/'):
            if not session.get('logged_in'):
                return redirect(url_for('dashboard.login'))

    @app.route('/robots.txt')
    def robots_txt():
        content = "User-agent: *\nAllow: /\nSitemap: http://127.0.0.1:5000/sitemap.xml\n"
        return content, 200, {'Content-Type': 'text/plain'}

    @app.route('/sitemap.xml')
    def sitemap_xml():
        content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>http://127.0.0.1:5000/</loc>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>"""
        return content, 200, {'Content-Type': 'application/xml'}

    @app.route('/llms.txt')
    def llms_txt():
        content = """# NetGaming Cafe System

Esports Arena & Premium Internet Cafe Management System built on Python Flask, MySQL, and OOP principles.

- Real-time PC availability monitoring (RTX 5090/5080)
- Protective session auth for administrative management
- Customer CRUD with Gen Z fully unique naming sets
- Automated rental sessions with Member (Rp 7,000/hr) vs Standard (Rp 8,000/hr) tariff calculator
- Tom Select search-integrated select forms
- Live analytics with Chart.js reporting & PDF document exports
- Auto-standby session release scanner
"""
        return content, 200, {'Content-Type': 'text/plain'}

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)