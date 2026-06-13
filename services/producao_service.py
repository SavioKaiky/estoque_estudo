from database import db
from models.produto import Produto
from models.insumo import Insumo
from models.ficha_tecnica import FichaTecnica
from models.movimentacao_produto import MovimentacaoProduto
from models.movimentacao_insumo import MovimentacaoInsumo
from services.custo_service import baixar_estoque_fifo, validar_estoque_fifo
 
 
def produzir(produto_id: int, quantidade: int) -> dict:
    """
    Orquestra a produção em UMA única transação atômica:
      1. Valida existência do produto e ficha técnica
      2. Verifica saldo de TODOS os insumos (antes de alterar qualquer coisa)
      3. Consome insumos via FIFO + registra movimentações de saída
      4. Registra movimentação de entrada do produto acabado
      5. Um único commit no final — ou tudo salva, ou nada salva
    """
    produto = db.session.get(Produto, produto_id)
    if not produto:
        raise ValueError("Produto não encontrado")
 
    if quantidade <= 0:
        raise ValueError("Quantidade deve ser maior que zero")
 
    ficha = FichaTecnica.query.filter_by(produto_id=produto_id).all()
    if not ficha:
        raise ValueError("Produto sem ficha técnica cadastrada")
 
    # ETAPA 1 — Validar todos os insumos ANTES de alterar qualquer coisa
    for item in ficha:
        insumo = db.session.get(Insumo, item.insumo_id)
        consumo = item.quantidade * quantidade
        if not validar_estoque_fifo(insumo.id, consumo):
            raise ValueError(
                f"Estoque insuficiente: {insumo.nome} "
                f"(necessário: {consumo:.2f}, disponível em lotes)"
            )
 
    # ETAPA 2 — Consumir FIFO e registrar saídas (sem commit intermediário)
    cmv_total = 0.0
 
    for item in ficha:
        insumo = db.session.get(Insumo, item.insumo_id)
        consumo = item.quantidade * quantidade
 
        # baixar_estoque_fifo NÃO faz commit — faz parte desta transação
        custo = baixar_estoque_fifo(insumo.id, consumo)
        cmv_total += custo
 
        mov_insumo = MovimentacaoInsumo(
            insumo_id=insumo.id,
            tipo="saida",
            quantidade=consumo,
            motivo="produção"
        )
        db.session.add(mov_insumo)
 
    # ETAPA 3 — Registrar entrada do produto acabado
    cmv_unitario = cmv_total / quantidade
 
    mov_produto = MovimentacaoProduto(
        produto_id=produto_id,
        tipo="entrada",
        quantidade=quantidade,
        motivo="produção",
        custo_total=cmv_total,
        custo_unitario=cmv_unitario
    )
    db.session.add(mov_produto)
 
    # ÚNICO commit de toda a operação — atômico
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
 
    return {"custo_total": cmv_total, "custo_unitario": cmv_unitario}
 
 
def saida_produto(produto_id: int, quantidade: int) -> None:
    """
    Registra venda/saída de produto acabado.
    Saldo calculado via movimentações (sem ler estoque_atual da coluna).
    """
    produto = db.session.get(Produto, produto_id)
    if not produto:
        raise ValueError("Produto não encontrado")
 
    if quantidade <= 0:
        raise ValueError("Quantidade deve ser maior que zero")
 
    saldo = produto.estoque_atual  # calculado via property nas movimentações
    if saldo < quantidade:
        raise ValueError(f"Estoque insuficiente. Disponível: {saldo}")
 
    mov = MovimentacaoProduto(
        produto_id=produto_id,
        tipo="saida",
        quantidade=quantidade,
        motivo="venda"
    )
    db.session.add(mov)
 
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
 