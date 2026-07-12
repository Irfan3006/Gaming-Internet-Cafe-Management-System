from flask import Flask
from config import Config
from models.warnet import Warnet
from routes import (
    dashboard_bp,
    komputer_bp,
    pelanggan_bp,
    penyewaan_bp,
    transaksi_bp,
    laporan_bp
)
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inisialisasi service Warnet yang menerapkan Abstraction & DB connection
    app.warnet_system = Warnet(Config)

    # Register blueprints
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(komputer_bp)
    app.register_blueprint(pelanggan_bp)
    app.register_blueprint(penyewaan_bp)
    app.register_blueprint(transaksi_bp)
    app.register_blueprint(laporan_bp)

    # Filter Jinja2 untuk format Rupiah
    @app.template_filter('rupiah')
    def rupiah_filter(value):
        try:
            val = float(value)
            formatted = f"{val:,.0f}".replace(",", ".")
            return f"Rp {formatted}"
        except (ValueError, TypeError):
            return f"Rp {value}"

    # Filter Jinja2 untuk format Waktu & Tanggal Indonesia
    @app.template_filter('datetime_format')
    def datetime_format_filter(value):
        if not value:
            return ""
        if isinstance(value, str):
            try:
                # Coba parse dari format string database standard
                value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return value
        return value.strftime("%d/%m/%Y %H:%M")

    return app

app = create_app()

if __name__ == '__main__':
    # Menjalankan aplikasi secara lokal
    app.run(debug=True, host='0.0.0.0', port=5000)
