import streamlit as st
import pandas as pd
from datetime import datetime

# Dados iniciais com os novos nomes
atendentes = [
    {"nome": "Camila", "ultimo": datetime.fromisoformat("2025-07-25T19:43:00"), "ativos": 4},
    {"nome": "Laura", "ultimo": datetime.fromisoformat("2025-07-25T19:42:00"), "ativos": 3},
    {"nome": "Juliana", "ultimo": datetime.fromisoformat("2025-07-25T19:40:00"), "ativos": 3},
    {"nome": "Flaviane", "ultimo": datetime.fromisoformat("2025-07-25T19:38:00"), "ativos": 2},
    {"nome": "Lays", "ultimo": datetime.fromisoformat("2025-07-25T19:37:00"), "ativos": 1},
    {"nome": "Sophia", "ultimo": datetime.fromisoformat("2025-07-25T19:36:00"), "ativos": 0},
    {"nome": "Larissa", "ultimo": datetime.fromisoformat("2025-07-25T19:35:00"), "ativos": 0},
    {"nome": "Valquiria", "ultimo": datetime.fromisoformat("2025-07-25T19:34:00"), "ativos": 0},
    {"nome": "Beatriz", "ultimo": datetime.fromisoformat("2025-07-25T19:33:00"), "ativos": 0},
    {"nome": "Giovanna", "ultimo": datetime.fromisoformat("2025-07-25T19:32:00"), "ativos": 0},
]

MAX_ATIVOS = 5

# Usamos session_state para armazenar o estado entre reruns do Streamlit
if "atendentes" not in st.session_state:
    st.session_state.atendentes = atendentes

if "ultimo_na_vez" not in st.session_state:
    st.session_state.ultimo_na_vez = None

def atualizar_status():
    atendentes = st.session_state.atendentes
    puxaveis = [at for at in atendentes if at["ativos"] < MAX_ATIVOS]
    puxaveis.sort(key=lambda x: (x["ativos"], x["ultimo"]))

    for at in atendentes:
        at["pode_puxar"] = at["ativos"] < MAX_ATIVOS
        if at["pode_puxar"]:
            at["ordem"] = puxaveis.index(at) + 1
        else:
            at["ordem"] = "—"

    atual_na_vez = puxaveis[0]["nome"] if puxaveis else None
    if atual_na_vez != st.session_state.ultimo_na_vez and atual_na_vez is not None:
        st.session_state.ultimo_na_vez = atual_na_vez
        st.success(f"🚨 Agora é a vez de **{atual_na_vez}** puxar um cliente!")

def adicionar_cliente(nome):
    for at in st.session_state.atendentes:
        if at["nome"].lower() == nome.lower():
            if at["ativos"] < MAX_ATIVOS:
                at["ativos"] += 1
                at["ultimo"] = datetime.now()
                st.success(f"Cliente adicionado para {at['nome']}.")
            else:
                st.warning(f"{at['nome']} já atingiu o limite de clientes ativos.")
            return
    st.error("Atendente não encontrado.")

def remover_cliente(nome):
    for at in st.session_state.atendentes:
        if at["nome"].lower() == nome.lower():
            if at["ativos"] > 0:
                at["ativos"] -= 1
                st.success(f"Cliente removido de {at['nome']}.")
            else:
                st.warning(f"{at['nome']} não tem clientes ativos para remover.")
            return
    st.error("Atendente não encontrado.")

def mostrar_tabela():
    data = []
    for at in st.session_state.atendentes:
        data.append({
            "Atendente": at["nome"],
            "Último Atendimento": at["ultimo"].strftime("%d/%m/%Y %H:%M:%S"),
            "Clientes Ativos": at["ativos"],
            "Pode Puxar?": "Sim" if at["pode_puxar"] else "Não",
            "Ordem Sugerida": at["ordem"],
        })
    df = pd.DataFrame(data)
    # Destacar a linha com ordem 1 (vez)
    def highlight_vez(row):
        return ['background-color: #fff3cd; font-weight: bold;' if row["Ordem Sugerida"] == 1 else '' for _ in row]
    st.dataframe(df.style.apply(highlight_vez, axis=1))

# Título
st.title("Dashboard de Atendimento - Lavanderia")

# Atualiza status e tabela
atualizar_status()
mostrar_tabela()

# Formulário para adicionar ou remover clientes
with st.form("form_atendimento"):
    nome = st.selectbox("Escolha o atendente:", [at["nome"] for at in st.session_state.atendentes])
    acao = st.radio("Ação:", ("Adicionar cliente", "Remover cliente"))
    submit = st.form_submit_button("Confirmar")

    if submit:
        if acao == "Adicionar cliente":
            adicionar_cliente(nome)
        else:
            remover_cliente(nome)
        atualizar_status()
        mostrar_tabela()
