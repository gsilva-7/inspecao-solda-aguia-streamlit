import streamlit as st
from datetime import datetime
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pytz

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Inspeção Perfiladeira Nova LC - Solda",
    page_icon="🦅",
    layout="centered"
)

# 2. FUNÇÃO DE SALVAMENTO
def salvar_no_gspread(dados_lista):
    creds_dict = st.secrets["connections"]["gsheets"]["service_account"]
    if isinstance(creds_dict, str):
        import json
        creds_dict = json.loads(creds_dict)
    
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    
    ID_PLANILHA = "11OHSy_VaQV0Z6beBzJMdwhR4TDqxggA_YqZG7vvJdVA" 
    sheet = client.open_by_key(ID_PLANILHA).worksheet("Dados")
    sheet.append_row(dados_lista)

# 3. CABEÇALHO
col_logo, col_titulo = st.columns([1, 4], vertical_alignment="center")

with col_logo:
    try:
        st.image("logo.jpg", width=100)
    except:
        st.title("🦅")

with col_titulo:
    st.title("Inspeção Perfiladeira Nova LC - Solda")
    st.caption("Data da Edição: 23/10/2025 | Revisão: 3 | Setor: Qualidade Industrial")
    st.caption("Autor(a): Gabriela Mendes | Verificado: Melina Favaro | Inspeção: a cada 60 minutos")
    st.caption("Desenvolvido por: Guilherme (Aprendiz - Desenvolvimento Web)")

# 4. ABA DE REFERÊNCIA
with st.expander("Visualizar Instruções de Medição (Referência Rev. 3)"):
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.subheader("1º PASSO")
        try: 
            st.image("passo1_ref.png", width="stretch")
        except: 
            st.warning("Arquivo 'passo1_ref.png' não encontrado.")
    with col_p2:
        st.subheader("2º PASSO")
        try: 
            st.image("passo2_ref.png", width="stretch")
        except: 
            st.warning("Arquivo 'passo2_ref.png' não encontrado.")

# 5. FORMULÁRIO
with st.container(border=True):
    c1, c2, c3 = st.columns(3)
    
    fuso_br = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(fuso_br)
    
    with c1: 
        st.text_input("Data", value=agora.strftime('%d/%m/%Y'), read_only=True)
    with c2: 
        st.text_input("Hora", value=agora.strftime('%H:%M:%S'), read_only=True)
    with c3: 
        op = st.text_input("O.P.")

    st.markdown("---")
    st.subheader("1º PASSO")
    st.caption("Efetuar medidas A1 e A2 (altura topo da garra) e B (comprimento longarina)")
    col_a1, col_a2, col_b = st.columns(3)
    a1 = col_a1.number_input("Medida A1", step=0.01, format="%.2f")
    a2 = col_a2.number_input("Medida A2", step=0.01, format="%.2f")
    b_medida = col_b.number_input("Medida B", step=0.01, format="%.2f")

    st.markdown("---")
    st.subheader("2º PASSO")
    st.caption("Medir distância garra/perfil (C) e validar qualidade visual da solda")
    col_c, col_solda = st.columns(2)
    with col_c: c_distancia = st.number_input("Distância C", step=0.01, format="%.2f")
    with col_solda: solda_status = st.radio("Solda", ["OK", "Ñ OK"], horizontal=True)

    st.markdown("---")
    inspetor = st.text_input("Inspetor")
    obs = st.text_area("Observações")

# 6. BOTÃO DE REGISTRO
submit = st.button("REGISTRAR INSPEÇÃO", use_container_width=True, type="primary")

# 7. LÓGICA DE EXECUÇÃO
if submit:
    if not op or not inspetor:
        st.warning("⚠️ O.P. e Inspetor são obrigatórios!")
    else:
        linha_para_salvar = [
            agora.strftime("%d/%m/%Y"), # Pega a data de Brasília
            agora.strftime("%H:%M:%S"), # Pega a hora de Brasília
            op, a1, a2, b_medida, c_distancia, solda_status, inspetor, obs
        ]
        try:
            salvar_no_gspread(linha_para_salvar)
            st.toast("✅ Registro salvo com sucesso!", icon="🦅")
        except Exception as e:
            st.error(f"Erro ao salvar: {e}")