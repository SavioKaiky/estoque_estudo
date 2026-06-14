# Importa todos os models para garantir que o SQLAlchemy
# os registre antes de configurar os relacionamentos.
# REGRA: sempre importe aqui, nunca individualmente no create_db ou app.

from models.user import User                            # primeiro — outros dependem dele
from models.insumo import Insumo, MovimentacaoInsumo   # MovimentacaoInsumo está em insumo.py
from models.produto import Produto
from models.lote_insumo import LoteInsumo
from models.ficha_tecnica import FichaTecnica
from models.movimentacao_produto import MovimentacaoProduto