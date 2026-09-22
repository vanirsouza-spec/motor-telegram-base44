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
        logging.info(f"📩 Sinal detectado! Texto:\n{mensagem}")
        
        # Procura por Padrão, Entrada ou qualquer linha descritiva
        padrao_match = re.search(r'(?:padr[ãa]o|padrao|entrada|estrat[ée]gia)[:\*\s]*([^\n]+)', mensagem, re.IGNORECASE)
        if padrao_match:
            padrao_detectado = padrao_match.group(1).replace('*', '').strip()
        else:
            # Se não achar a palavra exata, pega a primeira linha útil da mensagem
            linhas = [l.strip() for l in mensagem.split('\n') if l.strip()]
            padrao_detectado = linhas[0] if linhas else "Padrão Automático"
        
        # Captura flexível para a Liga
        liga_match = re.search(r'(?:liga)[:\*\s]*([^\n]+)', mensagem, re.IGNORECASE)
        liga_detectada = liga_match.group(1).replace('*', '').strip() if liga_match else "Liga Geral"
        
        # Identificação da Casa de Aposta
        casa_aposta = "Betano" # Valor padrão caso o canal seja focado numa casa específica, ou detetado pelo texto:
        msg_lower = mensagem.lower()
        if "bet365" in msg_lower:
            casa_aposta = "Bet365"
        elif "betano" in msg_lower:
            casa_aposta = "Betano"

        logging.info(f"🔍 Dados Extraídos -> Padrão: {padrao_detectado} | Liga: {liga_detectada} | Casa: {casa_aposta}")
        
        enviar_para_base44(casa_aposta, padrao_detectado, liga_detectada, resultado)
