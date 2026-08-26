from src.core.config import Settings
from sqlmodel import Session, create_engine

# Instância única global contendo as variáveis de ambiente validadas pelo Pydantic
settings = Settings()

# Engine de Conexão: abstração do SQLAlchemy responsável pelo pool de conexões TCP nativas com o PostgreSQL
# Dica: Adicione `echo=True` nos parâmetros de create_engine() para depurar e ver no terminal o SQL gerado
engine = create_engine(settings.SUPABASE_URL)

def get_session():
    """
    Gerador de Sessão (Generator) para Injeção de Dependência no FastAPI.

    Instancia uma nova sessão de transação vinculada ao 'engine' e pausa a execução no 'yield'
    para entregar o objeto à rota HTTP. Após o término do processamento do endpoint (ou em
    caso de exceção), o bloco 'with' é encerrado automaticamente, garantindo que a conexão
    seja fechada e devolvida ao pool com segurança.
    """
    
    with Session(engine) as session:
        yield session