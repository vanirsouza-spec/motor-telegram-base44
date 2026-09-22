import logging
import json
import requests
import re
import os
from threading import Thread
from flask import Flask
from datetime import datetime
from telethon import TelegramClient, events

# ==========================================
# 1. CONFIGURAÇÃO DO RASTREIO (LOGS)
# ==========================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("rastreio_base44.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# ==========================================
# 2. MINI SERVIDOR WEB (OBRIGATÓRIO PARA O RENDER GRÁTIS)
# ==========================================
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot Telegram Base44 ativo e a operar em plano gratuito!", 200

def run_flask():
    porta = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=porta)

# ==========================================
# 3. CREDENCIAIS
# ==========================================
api_id = '36667927'
api_hash = '7514985528ad7a0458d289549d0dc678'
TOKEN_BASE44 = 'b44u_527ea4fab8b748efe22e59eb3596437bde1021dd515e3f5183d51d131c09fdb4'
URL_BASE44 = 'https://ambrosial-ops-flow-dash.base44.app/api/entities/Operacoes'

client = TelegramClient('sessao_telegram', api_id, api_hash)

# ==========================================
# 4. FUNÇÃO DE ENVIO COM RASTREIO
# ==========================================
def enviar_para_base44(casa_aposta, padrao, liga, resultado):
    payload = {
        "casa_de_aposta": casa_aposta,
        "padrao": padrao,
        "liga": liga,
        "resultado": int(resultado),
        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    headers = {
        "Authorization": f"Bearer {TOKEN_BASE44}",
        "Content-Type": "application/json"
    }

    try:
        resposta = requests.post(URL_BASE44, json=payload, headers=headers, timeout=10)
        
        if resposta.status_code in [200, 201]:
            logging.info("✅ [SUCESSO] Operação comercial entregue à Base44!")
        else:
            logging.error(f"❌ [ERRO API] Código {resposta.status_code}. Retorno: {resposta.text}")
            
    except Exception as e:
        logging.critical(f"💥 [FALHA CRÍTICA] Erro de rede ou servidor: {e}")

# ==========================================
# 5. ESCUTADOR DO TELEGRAM E EXTRAÇÃO (REGEX)
# ==========================================
@client.on(events.NewMessage)
async def my_event_handler(event):
    mensagem = event.message.message
    
    resultado = None
    if "GREEN" in mensagem.upper() or "✅" in mensagem:
        resultado = 1
    elif "RED" in mensagem.upper() or "❌" in mensagem:
        resultado = -1
        
    if resultado is not None:
        logging.info(f"📩 Sinal detectado no Telegram. Resultado: {'Green' if resultado == 1 else 'Red'}")
        
        # Procura por "Padrão" ou "Padrao" ignorando maiúsculas/minúsculas e acentos
        padrao_match = re.search(r'padr[ãa]o[:\*\s]*(.+)', mensagem, re.IGNORECASE)
        padrao_detectado = padrao_match.group(1).strip() if padrao_match else "Padrão Não Identificado"
        
        # Procura por "Liga" ignorando maiúsculas/minúsculas
        liga_match = re.search(r'liga[:\*\s]*(.+)', mensagem, re.IGNORECASE)
        liga_detectada = liga_match.group(1).strip() if liga_match else "Liga Não Identificada"
        
        casa_aposta = "Desconhecida"
        msg_lower = mensagem.lower()
        if any(termo in msg_lower for termo in ["betano", "betano.bet.br", "vigia betano"]):
            casa_aposta = "Betano"
        elif any(termo in msg_lower for termo in ["bet365", "bet365.com", "bet365.bet"]):
            casa_aposta = "Bet365"

        logging.info(f"🔍 Dados Extraídos -> Padrão: {padrao_detectado} | Liga: {liga_detectada} | Casa: {casa_aposta}")
        
        enviar_para_base44(casa_aposta, padrao_detectado, liga_detectada, resultado)



# ==========================================
# 6. INICIALIZAÇÃO SIMULTÂNEA (WEB + TELEGRAM)
# ==========================================
if __name__ == '__main__':
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

    logging.info("🚀 Servidor Web e Escutador Comercial ativados em paralelo...")
    with client:
        client.run_until_disconnected()
