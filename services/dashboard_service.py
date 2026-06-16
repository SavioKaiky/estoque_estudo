"""
services/dashboard_service.py
===============================
REGRAS DE NEGÓCIO do dashboard.
Agrega dados de estoque, vendas e alertas para a home.
Sem dependência de Flask — retorna dicts puros.
"""

from datetime import datetime, timedelta
from sqlalchemy import func
from database import db
from models.insumo import Insumo
from models.produto import Produto
from models.movimentacao_produto import MovimentacaoProduto


def resumo_estoque_por_tipo() -> list[dict]:
    """
    Retorna saldo total agrupado por tipo de armazenamento.
    Ex: [{"tipo": "Estoque Seco", "total": 45.0}, ...]
    """
    insumos = Insumo.query.filter_by(ativo=True).all()
    grupos = {"seco": 0.0, "fria": 0.0, "congelada": 0.0}

    for insumo in insumos:
        grupos[insumo.tipo_armazenamento] = (
            grupos.get(insumo.tipo_armazenamento, 0.0) + insumo.estoque_atual
        )

    labels = {"seco": "Estoque Seco", "fria": "Câmara Fria", "congelada": "Câmara Congelada"}
    return [{"tipo": labels[k], "total": round(v, 2)} for k, v in grupos.items()]


def pratos_mais_vendidos(dias: int = 30) -> list[dict]:
    """
    Retorna os 10 produtos mais vendidos no período (saídas com motivo 'venda').
    """
    desde = datetime.utcnow() - timedelta(days=dias)

    resultado = (
        db.session.query(
            Produto.nome,
            func.sum(MovimentacaoProduto.quantidade).label("total_vendido")
        )
        .join(Produto, MovimentacaoProduto.produto_id == Produto.id)
        .filter(
            MovimentacaoProduto.tipo == "saida",
            MovimentacaoProduto.motivo == "venda",
            MovimentacaoProduto.created_at >= desde,
        )
        .group_by(Produto.id, Produto.nome)
        .order_by(func.sum(MovimentacaoProduto.quantidade).desc())
        .limit(10)
        .all()
    )

    return [{"nome": r.nome, "total": int(r.total_vendido)} for r in resultado]


def insumos_abaixo_minimo() -> list[dict]:
    """
    Retorna insumos com estoque abaixo do mínimo para o card de alertas.
    """
    insumos = Insumo.query.filter_by(ativo=True).all()
    alertas = []
    for insumo in insumos:
        if insumo.abaixo_minimo:
            alertas.append({
                "id": insumo.id,
                "nome": insumo.nome,
                "estoque_atual": round(insumo.estoque_atual, 2),
                "estoque_minimo": insumo.estoque_minimo,
                "unidade": insumo.unidade,
                "tipo_armazenamento": insumo.tipo_armazenamento_label,
            })
    return alertas


def cards_resumo() -> dict:
    """
    Números rápidos para os cards do topo do dashboard.
    """
    total_insumos = Insumo.query.filter_by(ativo=True).count()
    total_produtos = Produto.query.count()
    alertas = len(insumos_abaixo_minimo())

    desde = datetime.utcnow() - timedelta(days=30)
    vendas_mes = db.session.query(
        func.coalesce(func.sum(MovimentacaoProduto.quantidade), 0)
    ).filter(
        MovimentacaoProduto.tipo == "saida",
        MovimentacaoProduto.motivo == "venda",
        MovimentacaoProduto.created_at >= desde,
    ).scalar()

    return {
        "total_insumos": total_insumos,
        "total_produtos": total_produtos,
        "alertas_estoque": alertas,
        "vendas_mes": int(vendas_mes),
    }