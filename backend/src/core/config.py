from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Gerenciador Global de Configurações e Variáveis de Ambiente.

    Utiliza o Pydantic Settings para ler e validar as variáveis do arquivo '.env'
    no momento em que a aplicação inicia. Centralizar aqui evita a exposição de 
    segredos (como senhas do banco) e lança erros claros se faltar alguma variável.
    """
    
    # String de conexão nativa PostgreSQL (ex: postgresql://user:pass@host:port/dbname)
    SUPABASE_URL: str
    
    # Define a fonte e a codificação das variáveis
    model_config = SettingsConfigDict(env_file='.env', 
                                      env_file_encoding='utf-8',
                                      # Dica: adicione `extra="ignore"` se houver variáveis no .env que o backend não vá utilizar
    )