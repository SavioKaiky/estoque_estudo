from database import db
from models.lote_insumo import LoteInsumo
 
 
def baixar_estoque_fifo(insumo_id: int, quantidade: float) -> float:
    """
    Consome insumos pelos lotes mais antigos primeiro (FIFO).
    Retorna o custo total consumido.
    NÃO faz commit — deixa para o chamador controlar a transação.
    """
    lotes = (
        LoteInsumo.query
        .filter_by(insumo_id=insumo_id)
        .filter(LoteInsumo.quantidade_restante > 0)
        .order_by(LoteInsumo.created_at.asc())
        .all()
    )
 
    restante = quantidade
    custo_total = 0.0
 
    for lote in lotes:
        if restante <= 0:
            break
        usar = min(lote.quantidade_restante, restante)
        custo_total += usar * lote.custo_unitario
        lote.quantidade_restante -= usar
        restante -= usar
 
    if restante > 0:
        raise ValueError("Estoque insuficiente nos lotes (FIFO)")
 
    # SEM db.session.commit() aqui — transação controlada pelo producao_service
    return custo_total
 
 
def baixar_estoque_lifo(insumo_id: int, quantidade: float) -> float:
    """
    Consome insumos pelos lotes mais recentes primeiro (LIFO).
    Retorna o custo total consumido.
    NÃO faz commit — deixa para o chamador controlar a transação.
    """
    lotes = (
        LoteInsumo.query
        .filter_by(insumo_id=insumo_id)
        .filter(LoteInsumo.quantidade_restante > 0)
        .order_by(LoteInsumo.created_at.desc())
        .all()
    )
 
    restante = quantidade
    custo_total = 0.0
 
    for lote in lotes:
        if restante <= 0:
            break
        usar = min(lote.quantidade_restante, restante)
        custo_total += usar * lote.custo_unitario
        lote.quantidade_restante -= usar
        restante -= usar
 
    if restante > 0:
        raise ValueError("Estoque insuficiente nos lotes (LIFO)")
 
    # SEM db.session.commit() aqui
    return custo_total
 
 
def validar_estoque_fifo(insumo_id: int, quantidade: float) -> bool:
    """
    Verifica se há quantidade disponível nos lotes sem alterar nada.
    Usado antes de iniciar uma produção para falhar rápido.
    """
    lotes = (
        LoteInsumo.query
        .filter_by(insumo_id=insumo_id)
        .filter(LoteInsumo.quantidade_restante > 0)
        .all()
    )
    total_disponivel = sum(l.quantidade_restante for l in lotes)
    return total_disponivel >= quantidade
 