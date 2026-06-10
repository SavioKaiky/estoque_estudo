import os

class Config:
    # CORREÇÃO: SECRET_KEY obrigatória para flash() e sessões funcionarem
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-insecure-key-troque-em-producao")

    # CORREÇÃO: lê do ambiente em produção; cai no padrão local em dev
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root:@localhost/sistema_estoque"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False