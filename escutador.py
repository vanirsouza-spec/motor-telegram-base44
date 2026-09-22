@client.on(events.NewMessage)
async def my_event_handler(event):
    mensagem = event.message.message
    
    resultado = None
    msg_upper = mensagem.upper()
    if any(termo in msg_upper for termo in ["GREEN", "✅", "WIN", "VITÓRIA", "ITORIA"]):
        resultado = 1
    elif any(termo in msg_upper for termo in ["RED", "❌", "LOSS", "DERROTA", "ERRO"]):
        resultado = -1
        
    if resultado is not None:
        # Mostra exatamente o texto que chegou do Telegram nos logs para diagnóstico
        logging.info(f"📩 Sinal detectado! Texto original:\n{mensagem}")
        
        # Procura pelo Padrão considerando quebra de linha ou asteriscos
        padrao_match = re.search(r'(?:padrão|padrao)[:\*\s]*([^\n]+)', mensagem, re.IGNORECASE)
        padrao_detectado = padrao_match.group(1).replace('*', '').strip() if padrao_match else "Padrão Não Identificado"
        
        # Procura pela Liga considerando quebra de linha ou asteriscos
        liga_match = re.search(r'(?:liga)[:\*\s]*([^\n]+)', mensagem, re.IGNORECASE)
        liga_detectada = liga_match.group(1).replace('*', '').strip() if liga_match else "Liga Não Identificada"
        
        casa_aposta = "Desconhecida"
        msg_lower = mensagem.lower()
        if any(termo in msg_lower for termo in ["betano", "betano.bet.br", "vigia betano"]):
            casa_aposta = "Betano"
        elif any(termo in msg_lower for termo in ["bet365", "bet365.com", "bet365.bet"]):
            casa_aposta = "Bet365"

        logging.info(f"🔍 Dados Extraídos -> Padrão: {padrao_detectado} | Liga: {liga_detectada} | Casa: {casa_aposta}")
        
        enviar_para_base44(casa_aposta, padrao_detectado, liga_detectada, resultado)

