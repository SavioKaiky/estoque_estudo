from database import db
from models.insumo import Insumo
from models.movimentacao_insumo import MovimentacaoInsumo
from models.lote_insumo import LoteInsumo
 
 
def movimentar_insumo(insumo_id: int, tipo: str, quantidade: float,
                      motivo: str, valor_total: float = None) -> None:
    """
    Registra entrada ou saída de insumo.
 
    Entrada: cria lote com custo unitário e registra movimentação de entrada.
    Saída:   valida saldo (via movimentações) e registra movimentação de saída.
 
    Não atualiza coluna estoque_atual — o saldo é calculado pela property do model.
    """
    insumo = db.session.get(Insumo, insumo_id)
 
    if not insumo:
        raise ValueError("Insumo não encontrado")
 
    if quantidade <= 0:
        raise ValueError("Quantidade deve ser maior que zero")
 
    if tipo == "saida":
        saldo = insumo.estoque_atual  # calculado via property
        if saldo < quantidade:
            raise ValueError(f"Estoque insuficiente. Disponível: {saldo:.2f}")
 
    elif tipo == "entrada":
        if valor_total is None or valor_total <= 0:
            raise ValueError("Informe o valor total da compra para registrar a entrada")
 
        custo_unitario = valor_total / quantidade
 
        lote = LoteInsumo(
            insumo_id=insumo_id,
            quantidade_inicial=quantidade,
            quantidade_restante=quantidade,
            custo_unitario=custo_unitario
        )
        db.session.add(lote)
 
    else:
        raise ValueError(f"Tipo inválido: '{tipo}'. Use 'entrada' ou 'saida'")
 
    # A movimentação É o saldo — não precisa de coluna separada
    mov = MovimentacaoInsumo(
        insumo_id=insumo_id,
        tipo=tipo,
        quantidade=quantidade,
        motivo=motivo
    )
    db.session.add(mov)
 
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
 