"""
routes/dashboard.py
====================
Rotas do dashboard — home e endpoint JSON para o React.
"""

from flask import Blueprint, render_template, jsonify
from services.dashboard_service import (
    resumo_estoque_por_tipo,
    pratos_mais_vendidos,
    insumos_abaixo_minimo,
    cards_resumo,
)

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def home():
    return render_template("home.html")


@dashboard_bp.route("/api/dashboard")
def api_dashboard():
    """
    Endpoint JSON consumido pelo componente React da home.
    Retorna todos os dados do dashboard em uma única chamada.
    """
    return jsonify({
        "cards": cards_resumo(),
        "estoque_por_tipo": resumo_estoque_por_tipo(),
        "pratos_mais_vendidos": pratos_mais_vendidos(dias=30),
        "insumos_abaixo_minimo": insumos_abaixo_minimo(),
    })