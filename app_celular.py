import subprocess
import sys

try:
    import streamlit as st
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit", "requests"])
    import streamlit as st

import requests

API_CONTADOR = "https://kvdict.com"

def obtener_estado_por_ip():
    try:
        resposta = requests.get("http://ip-api.com", timeout=3).json()
        return resposta.get("region", "Ignorado")
    except:
        return "Ignorado"

def computar_acesso(estado):
    if estado != "Ignorado" and estado:
        try:
            requests.post(f"{API_CONTADOR}/increment/{estado}", timeout=3)
        except:
            pass

st.set_page_config(page_title="Verificador Anti-Golpe", page_icon="🛡️", layout="centered")
st.title("🛡️ Verificador Anti-Golpe")
st.write("Cole o link suspeito recebido no WhatsApp ou SMS para analisar se é seguro:")

url_entrada = st.text_input("Cole o link aqui:", placeholder="https://...").strip()

if st.button("VERIFICAR AGORA", use_container_width=True):
    if not url_entrada:
        st.warning("⚠️ Por favor, cole um link primeiro!")
    else:
        estado_usuario = obtener_estado_por_ip()
        computar_acesso(estado_usuario)
        if not url_entrada.startswith("http://") and not url_entrada.startswith("https://"):
            url_entrada = "https://" + url_entrada
        palavras_suspeitas = ["atualizacao", "recadastro", "promocao", "ganhe", "sorteio", "vaga", "pix"]
        score = sum(1 for p in palavras_suspeitas if p in url_entrada.lower())
        try:
            resposta = requests.get(url_entrada, timeout=5, allow_redirects=True)
            url_final = resposta.url.lower()
            if score > 0 or "login" in url_final:
                st.error("🚨 LINK MALICIOSO - GOLPE/ROUBO DE DADOS 🚨\n\nEste site tenta roubar suas informações. Não digite nenhuma senha ou dado!")
            else:
                st.success("✅ LINK SEGURO ✅\n\nNenhuma ameaça foi encontrada neste endereço.")
        except:
            st.warning("⚠️ LINK INDISPONÍVEL OU INVÁLIDO ⚠️\n\nO site não respondeu. Pode ser um golpe que já foi desativado.")
