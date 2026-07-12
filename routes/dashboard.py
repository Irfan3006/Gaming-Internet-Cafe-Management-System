from flask import Blueprint, render_template, current_app

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
def index():
    warnet = current_app.warnet_system
    stats = warnet.get_statistik()
    transaksi_terbaru = warnet.get_transaksi_terbaru(5)
    return render_template('dashboard.html', stats=stats, transaksi_terbaru=transaksi_terbaru)
