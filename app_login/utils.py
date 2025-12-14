from flask import request
from app_login.extensions import db
from app_login.models.auth import UserActivityLog
import re
from datetime import datetime, date

# ---------------------------------------------------------
# 1) Rastreamento de atividades dentro do sistema
# ---------------------------------------------------------
def log_activity(user, action):
    entry = UserActivityLog(
        user_id=user.id,
        action=action,
        ip_address=request.remote_addr,
        user_agent=request.headers.get("User-Agent")
    )
    db.session.add(entry)
    db.session.commit()

# ---------------------------------------------------------
# 2) Validação de CPF
# ---------------------------------------------------------
def validar_cpf(cpf: str) -> bool:
    # Remove caracteres não numéricos
    cpf = re.sub(r'[^0-9]', '', cpf)

    # CPF deve ter 11 dígitos
    if len(cpf) != 11:
        return False

    # Não pode ser sequência repetida
    if cpf == cpf[0] * 11:
        return False

    # Validação dos dígitos verificadores
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    dig1 = (soma * 10 % 11) % 10
    if dig1 != int(cpf[9]):
        return False

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    dig2 = (soma * 10 % 11) % 10
    if dig2 != int(cpf[10]):
        return False

    return True

# ---------------------------------------------------------
# 3) Converte "YYYY-MM-DD" → "DD/MM/YYYY"
# ---------------------------------------------------------
def data_db_para_ptbr(data_str: str) -> str:
    try:
        data = datetime.strptime(data_str, "%Y-%m-%d")
        return data.strftime("%d/%m/%Y")
    except Exception:
        return data_str  # Caso venha vazio ou quebrado

# ---------------------------------------------------------
# 4) Converte "DD/MM/YYYY" → "YYYY-MM-DD"
# ---------------------------------------------------------
def data_ptbr_para_db(data_str: str) -> str:
    try:
        data = datetime.strptime(data_str, "%d/%m/%Y")
        return data.strftime("%Y-%m-%d")
    except Exception:
        return data_str

# ---------------------------------------------------------
# 5) Converte datetime do banco "YYYY-MM-DD HH:MM:SS" → "DD/MM/YYYY HH:MM"
# ---------------------------------------------------------
def datetime_db_para_ptbr(dt_str: str) -> str:
    try:
        data = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        return data.strftime("%d/%m/%Y %H:%M")
    except Exception:
        return dt_str


# ---------------------------------------------------------
# 5) Converte "DD/MM/YYYY HH:MM" → "YYYY-MM-DD HH:MM:SS"
# ---------------------------------------------------------
def datetime_ptbr_para_db(dt_str: str) -> str:
    try:
        data = datetime.strptime(dt_str, "%d/%m/%Y %H:%M")
        return data.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return dt_str
    
# ---------------------------------------------------------
# 6) VALIDADOR DE E-MAIL
# ---------------------------------------------------------
def validar_email(email: str) -> bool:
    """ Aceita e-mails como:
    - usuario@dominio.com
    - nome.sobrenome@empresa.org.br
    - teste+tag@gmail.com
    """
    if not email:
        return False

    email = email.strip()

    # Regex boa e enxuta para e-mails reais
    padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    return re.match(padrao, email) is not None


# ---------------------------------------------------------
# 7) CALCULAR IDADE A PARTIR DA DATA DE NASCIMENTO (YYYY-MM-DD)
# ---------------------------------------------------------
def calcular_idade(data_nascimento: str) -> int:
    try:
        nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
    except Exception:
        return -1

    hoje = date.today()
    idade = hoje.year - nascimento.year

    # Ajusta se a pessoa ainda não fez aniversário neste ano
    if (hoje.month, hoje.day) < (nascimento.month, nascimento.day):
        idade -= 1

    return idade


# ---------------------------------------------------------
# 8) LIMPAR VISUALIZADOR DE ACESSOS
# ---------------------------------------------------------
def parse_browser(user_agent: str) -> str:
    if not user_agent:
        return "-"

    ua = user_agent.lower()

    if "edg" in ua:
        return "Edge"
    if "chrome" in ua and "safari" in ua:
        return "Chrome"
    if "firefox" in ua:
        return "Firefox"
    if "safari" in ua and "chrome" not in ua:
        return "Safari"
    if "opera" in ua or "opr" in ua:
        return "Opera"
    if "msie" in ua or "trident" in ua:
        return "Internet Explorer"

    return "Desconhecido"
