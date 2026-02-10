import streamlit as st
import sys
import os
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- IMPORTAÇÃO DO MÓDULO DE NAVEGAÇÃO ---
# Adiciona a pasta pai (raiz) ao caminho do Python para importar 'navegacao.py'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from navegacao import sidebar_menu

# --- CONFIGURAÇÃO DA PÁGINA ---
# (Mantenha o set_page_config original de cada arquivo aqui, com title e icon específicos)
st.set_page_config(layout="wide", page_title="Russinvest...", page_icon="...")

# --- BARRA LATERAL ---
sidebar_menu() # <--- ISSO SUBSTITUI TODO O CÓDIGO ANTIGO DE SIDEBAR

# ... (Resto do código do aplicativo)

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(layout="wide", page_title="Russinvest - Fluxo", page_icon="🌊")

# --- CSS OTIMIZADO ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .russinvest-header { font-family: 'Inter', sans-serif; font-weight: 800; letter-spacing: -1.5px; line-height: 1.1; color: inherit; }
    @media (min-width: 768px) { .russinvest-header { font-size: 2.8em; } }
    @media (max-width: 767px) { .russinvest-header { font-size: 1.8em; letter-spacing: -0.5px; } .russinvest-sub { font-size: 0.9em !important; margin-bottom: 20px !important; } }
    .russinvest-sub { color: #0066ff; font-size: 1.1em; font-weight: 600; margin-top: 5px; margin-bottom: 35px; border-left: 4px solid #0066ff; padding-left: 12px; }
    
    .sidebar-brand { background-color: #f8fafc; padding: 20px; border-radius: 12px; margin-bottom: 25px; text-align: center; border: 1px solid #e2e8f0; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    @media (prefers-color-scheme: dark) { .sidebar-brand { background-color: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); } .brand-title { color: #60a5fa !important; } }
    .brand-flex { display: flex; justify-content: center; align-items: center; gap: 10px; margin-bottom: 5px; }
    .brand-title { color: #0066ff; font-size: 1.6rem; font-weight: 800; letter-spacing: -0.5px; margin: 0; }
    .brand-subtitle { color: #94a3b8; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; font-weight: 600; margin-top: 2px; }
    
    .kpi-card { background-color: #f1f5f9; padding: 15px; border-radius: 8px; text-align: center; border: 1px solid #e2e8f0; }
    .kpi-val { font-size: 1.5rem; font-weight: 800; color: #0f172a; margin-top: 5px; }
    .kpi-lbl { font-size: 0.8rem; text-transform: uppercase; color: #64748b; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

def formatar_br(valor): return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- ESTADO INICIAL (SESSION STATE) ---
if 'df_saidas_data' not in st.session_state:
    st.session_state.df_saidas_data = pd.DataFrame([
        {"Nome": "Moradia (Total)", "Valor": 4000.0},
        {"Nome": "Alimentação (Total)", "Valor": 2500.0},
        {"Nome": "Transporte/Carro", "Valor": 1500.0},
        {"Nome": "Educação", "Valor": 2000.0},
        {"Nome": "Lazer & Restaurantes", "Valor": 1500.0},
        {"Nome": "Investimentos (Aportes)", "Valor": 3000.0},
    ])

# --- DIALOG (O ASSISTENTE MÁGICO 2.0) ---
@st.dialog("🧙‍♂️ Assistente de Detalhamento")
def open_wizard(categoria):
    st.markdown(f"Vamos detalhar seus gastos com **{categoria}**.")
    total_calculado = 0.0
    
    # 1. MORADIA
    if categoria == "Moradia":
        col1, col2 = st.columns(2)
        v1 = col1.number_input("Aluguel", 0.0, step=100.0)
        v2 = col2.number_input("Condomínio", 0.0, step=100.0)
        v3 = col1.number_input("IPTU (Mensal)", 0.0, step=50.0)
        v4 = col2.number_input("Energia/Luz", 0.0, step=50.0)
        v5 = col1.number_input("Água/Esgoto", 0.0, step=50.0)
        v6 = col2.number_input("Internet/TV", 0.0, step=50.0)
        v7 = st.number_input("Gás/Manutenção", 0.0, step=50.0)
        total_calculado = v1+v2+v3+v4+v5+v6+v7

    # 2. ALIMENTAÇÃO
    elif categoria == "Alimentação":
        st.info("💡 Dica: Informe valores semanais se preferir, o sistema multiplica por 4.")
        v1 = st.number_input("Mercado Semanal", 0.0, step=50.0)
        v2 = st.number_input("Feira/Açougue Semanal", 0.0, step=50.0)
        v3 = st.number_input("Compras Mensais (Atacado/Estoque)", 0.0, step=100.0)
        v4 = st.number_input("Padaria/Dia-a-dia", 0.0, step=20.0)
        total_calculado = (v1 * 4) + (v2 * 4) + v3 + v4

    # 3. TRANSPORTE
    elif categoria == "Transporte":
        st.markdown("**Gastos Mensais**")
        c1, c2 = st.columns(2)
        v1 = c1.number_input("Combustível / Uber", 0.0, step=50.0)
        v2 = c2.number_input("Estacionamento / Pedágio", 0.0, step=20.0)
        v3 = c1.number_input("Parcela do Carro", 0.0, step=100.0)
        
        st.markdown("**Gastos Anuais (Dividido por 12)**")
        v4 = st.number_input("IPVA Anual", 0.0, step=100.0)
        v5 = st.number_input("Seguro Auto Anual", 0.0, step=100.0)
        v6 = st.number_input("Manutenção Preventiva (Revisão)", 0.0, step=100.0)
        
        mensal_fixo = v1 + v2 + v3
        mensal_anualizado = (v4 + v5 + v6) / 12
        total_calculado = mensal_fixo + mensal_anualizado
        
        st.caption(f"Fixo: {formatar_br(mensal_fixo)} + Provisão Anual: {formatar_br(mensal_anualizado)}")

    # 4. EDUCAÇÃO
    elif categoria == "Educação":
        v1 = st.number_input("Mensalidade Escolar/Faculdade", 0.0, step=100.0)
        v2 = st.number_input("Cursos Extracurriculares (Inglês/Esportes)", 0.0, step=50.0)
        v3 = st.number_input("Material Escolar (Anual)", 0.0, step=100.0)
        total_calculado = v1 + v2 + (v3 / 12)

    st.markdown("---")
    st.markdown(f"### Média Mensal Final: **{formatar_br(total_calculado)}**")
    
    if st.button("✅ Salvar na Tabela"):
        df_atual = st.session_state.df_saidas_data
        # Busca inteligente (Case insensitive e parcial)
        termo_busca = "Transporte" if categoria == "Transporte" else categoria
        mask = df_atual["Nome"].str.contains(termo_busca, case=False)
        
        if mask.any():
            df_atual.loc[mask, "Valor"] = total_calculado
        else:
            novo_item = pd.DataFrame([{"Nome": f"{categoria} (Total)", "Valor": total_calculado}])
            st.session_state.df_saidas_data = pd.concat([df_atual, novo_item], ignore_index=True)
        st.rerun()

# --- SIDEBAR ---
with st.sidebar:

    nome_cliente = st.text_input("Nome do Cliente", "Visitante")
    st.markdown("---")
    st.info("💡 **Dica:** Use os botões 'Assistente' para calcular gastos complexos (Carro, Mercado) automaticamente.")

# --- HEADER ---
st.markdown('<div class="russinvest-header">Raio-X Financeiro</div>', unsafe_allow_html=True)
st.markdown('<div class="russinvest-sub">Mapeamento visual de Receitas vs Despesas (Sankey)</div>', unsafe_allow_html=True)

col_input1, col_input2 = st.columns(2)

with col_input1:
    st.markdown("### 🟢 Entradas (Receitas)")
    df_receitas_padrao = pd.DataFrame([
        {"Nome": "Salário Líquido", "Valor": 15000.0},
        {"Nome": "Bônus Médio (Mensal)", "Valor": 2000.0},
        {"Nome": "Aluguéis Recebidos", "Valor": 0.0},
    ])
    df_entradas = st.data_editor(df_receitas_padrao, num_rows="dynamic", key="in", column_config={"Valor": st.column_config.NumberColumn(format="R$ %.2f")}, use_container_width=True)

with col_input2:
    st.markdown("### 🔴 Saídas (Destinos)")
    
    # Grid de Botões do Assistente
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("🏠 Moradia"): open_wizard("Moradia")
    if c2.button("🛒 Mercado"): open_wizard("Alimentação")
    if c3.button("🚗 Carro"): open_wizard("Transporte")
    if c4.button("🎓 Educação"): open_wizard("Educação")
    
    # Tabela Principal (Lê do Session State)
    df_saidas = st.data_editor(st.session_state.df_saidas_data, num_rows="dynamic", key="out", column_config={"Valor": st.column_config.NumberColumn(format="R$ %.2f")}, use_container_width=True)
    
    # Sincroniza volta para o Session State (caso usuário edite manualmente)
    st.session_state.df_saidas_data = df_saidas

# --- PROCESSAMENTO ---
total_entradas = df_entradas["Valor"].sum()
total_saidas = df_saidas["Valor"].sum()
saldo = total_entradas - total_saidas
investimentos = df_saidas[df_saidas["Nome"].str.contains("Invest|Aporte|Poupança|Guardar", case=False)]["Valor"].sum()
taxa_poupanca = ((investimentos + (saldo if saldo > 0 else 0)) / total_entradas * 100) if total_entradas > 0 else 0

# --- PREPARAÇÃO SANKEY ---
label = ["Orçamento Mensal"] + df_entradas["Nome"].tolist() + df_saidas["Nome"].tolist()
if saldo > 0: label.append("Saldo Livre (Caixa)")

idx_hub = 0
idx_start_entradas = 1
idx_end_entradas = idx_start_entradas + len(df_entradas)
idx_start_saidas = idx_end_entradas
idx_saldo = len(label) - 1

source = []
target = []
value = []
colors = []

# Cores Profissionais
color_entrada = "#22c55e" # Green
color_invest = "#3b82f6"  # Blue
color_gasto = "#ef4444"   # Red
color_saldo = "#10b981"   # Emerald

for i, row in df_entradas.iterrows():
    source.append(idx_start_entradas + i); target.append(idx_hub); value.append(row["Valor"]); colors.append(color_entrada)

for i, row in df_saidas.iterrows():
    source.append(idx_hub); target.append(idx_start_saidas + i); value.append(row["Valor"])
    colors.append(color_invest if "Invest" in row["Nome"] or "Aporte" in row["Nome"] else color_gasto)

if saldo > 0:
    source.append(idx_hub); target.append(idx_saldo); value.append(saldo); colors.append(color_saldo)

# --- VISUALIZAÇÃO ---
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"<div class='kpi-card'><div class='kpi-lbl'>Receita Total</div><div class='kpi-val'>{formatar_br(total_entradas)}</div></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='kpi-card'><div class='kpi-lbl'>Despesas + Aportes</div><div class='kpi-val'>{formatar_br(total_saidas)}</div></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='kpi-card'><div class='kpi-lbl'>{'Saldo Positivo' if saldo>=0 else 'Déficit'}</div><div class='kpi-val' style='color:{'#16a34a' if saldo>=0 else '#ef4444'}'>{formatar_br(saldo)}</div></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='kpi-card'><div class='kpi-lbl'>Taxa de Poupança</div><div class='kpi-val' style='color:#3b82f6'>{taxa_poupanca:.1f}%</div></div>", unsafe_allow_html=True)

st.markdown("### 🌊 Mapa do Dinheiro")

# GRÁFICO SANKEY (AJUSTE DE FONTE CLARA)
fig = go.Figure(data=[go.Sankey(
    textfont=dict(size=12, color="white", family="Inter"), # Fonte Branca
    node = dict(
      pad = 20,
      thickness = 15,
      line = dict(color = "white", width = 0.5),
      label = label,
      color = "rgba(100, 116, 139, 0.5)"
    ),
    link = dict(source=source, target=target, value=value, color=colors)
)])

fig.update_layout(
    font=dict(size=12, color="#e2e8f0", family="Inter, sans-serif"), # Texto geral claro (Off-white)
    height=600,
    margin=dict(t=40, b=40, l=20, r=20),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    hovermode='x',
)
st.plotly_chart(fig, use_container_width=True)

# --- EXPORT ---
def gerar_relatorio_sankey(cliente, receita, despesa, sobrou, taxa, df_in, df_out):
    # Gerador simples para HTML
    return f"""
    <html><body>
    <h2>Diagnóstico - {cliente}</h2>
    <p>Receita: {formatar_br(receita)} | Despesa: {formatar_br(despesa)} | Saldo: {formatar_br(sobrou)}</p>
    </body></html>
    """

with st.sidebar:
    st.markdown("**Exportar**")
    html_relatorio = gerar_relatorio_sankey(nome_cliente, total_entradas, total_saidas, saldo, taxa_poupanca, df_entradas, df_saidas)
    st.download_button("📄 Baixar Diagnóstico", html_relatorio, f"Diagnostico_{nome_cliente}.html", "text/html")
