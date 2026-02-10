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
st.set_page_config(layout="wide", page_title="Russinvest - Proteção", page_icon="🛡️")

# --- CSS OTIMIZADO (IDENTIDADE UNIFICADA) ---
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
    
    /* Result Boxes */
    .result-box { padding: 24px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .result-alert { background: #fee2e2; border-left: 5px solid #ef4444; color: #991b1b; }
    .result-success { background: #dcfce7; border-left: 5px solid #16a34a; color: #14532d; }
</style>
""", unsafe_allow_html=True)

def formatar_br(valor): return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- FUNÇÃO GERADORA DE RELATÓRIO PROFISSIONAL (PROTEÇÃO) ---
def gerar_relatorio_protecao(cliente, gap, total_nec, total_disp, df_detalhe):
    data_hoje = datetime.now().strftime("%d/%m/%Y")
    
    status_color = "#ef4444" if gap > 0 else "#16a34a"
    status_bg = "#fee2e2" if gap > 0 else "#dcfce7"
    status_msg = "DÉFICIT DE PROTEÇÃO DETECTADO" if gap > 0 else "FAMÍLIA FINANCEIRAMENTE PROTEGIDA"
    
    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Helvetica', 'Arial', sans-serif; padding: 40px; color: #333; max-width: 800px; margin: 0 auto; }}
            .header {{ text-align: center; border-bottom: 2px solid #0066ff; padding-bottom: 20px; margin-bottom: 30px; }}
            .brand {{ color: #0066ff; font-size: 24px; font-weight: 800; }}
            .sub {{ font-size: 12px; text-transform: uppercase; letter-spacing: 2px; color: #666; }}
            .title {{ font-size: 22px; font-weight: 700; color: #1e293b; margin-bottom: 15px; }}
            
            .alert-box {{ background-color: {status_bg}; border-left: 6px solid {status_color}; padding: 25px; border-radius: 8px; margin-bottom: 30px; }}
            .alert-title {{ font-weight: 800; font-size: 16px; margin-bottom: 5px; color: {status_color}; letter-spacing: 1px; }}
            .alert-val {{ font-size: 32px; font-weight: 800; color: #1e293b; margin: 10px 0; }}
            
            .cols {{ display: flex; gap: 30px; margin-bottom: 30px; }}
            .col {{ flex: 1; background: #f8fafc; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; }}
            .col-lbl {{ font-size: 11px; text-transform: uppercase; color: #64748b; font-weight: bold; margin-bottom: 5px; }}
            .col-val {{ font-size: 20px; font-weight: 700; color: #0f172a; }}
            
            table {{ width: 100%; border-collapse: collapse; font-size: 13px; margin-top: 10px; }}
            th {{ background-color: #f1f5f9; padding: 12px; text-align: left; color: #475569; border-bottom: 2px solid #e2e8f0; }}
            td {{ padding: 12px; border-bottom: 1px solid #e2e8f0; color: #334155; }}
            tr.subtotal {{ background-color: #f8fafc; font-weight: bold; }}
            
            .footer {{ margin-top: 50px; text-align: center; font-size: 11px; color: #94a3b8; border-top: 1px solid #e2e8f0; padding-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="brand">Russinvest 🔷</div>
            <div class="sub">Gestão de Riscos</div>
            <div style="margin-top: 10px; font-size: 14px;">Cliente: <b>{cliente}</b> | Data: {data_hoje}</div>
        </div>

        <div class="title">Análise de Necessidade de Proteção</div>

        <div class="alert-box">
            <div class="alert-title">{status_msg}</div>
            <div style="margin-bottom: 5px;">Capital Segurado Recomendado (Gap):</div>
            <div class="alert-val">{formatar_br(gap)}</div>
            <div style="font-size: 14px; opacity: 0.8;">Este é o valor necessário para cobrir o padrão de vida e custos na ausência do titular.</div>
        </div>

        <div class="cols">
            <div class="col">
                <div class="col-lbl">Necessidade Total</div>
                <div class="col-val">{formatar_br(total_nec)}</div>
            </div>
            <div class="col">
                <div class="col-lbl">Recursos Disponíveis</div>
                <div class="col-val" style="color: #16a34a;">{formatar_br(total_disp)}</div>
            </div>
        </div>

        <h3 style="font-size: 16px; color: #1e293b; margin-bottom: 10px;">Detalhamento do Cálculo</h3>
        {df_detalhe.to_html(index=False, border=0)}
        
        <div class="footer">
            Relatório gerado pelo Sistema Russinvest. 
            A sugestão de capital segurado visa manter a dignidade financeira da família e a sucessão patrimonial.
        </div>
    </body>
    </html>
    """
    return html

# --- SIDEBAR ---
with st.sidebar:

    nome_cliente = st.text_input("Nome do Cliente", "Visitante")
    
    st.markdown("### 1. Manutenção da Família")
    despesa_mensal = st.number_input("Custo de Vida Mensal (R$)", 0.0, value=15000.0, step=1000.0, help="Valor para manter o padrão de vida da família.")
    anos_protecao = st.slider("Anos de Proteção", 1, 30, 10, help="Geralmente até o filho mais novo completar 24 anos.")
    
    st.markdown("### 2. Projetos & Dívidas")
    dividas_total = st.number_input("Saldo Devedor (Financ/Empréstimos)", 0.0, value=400000.0, step=5000.0, help="Para quitar casa, carro, etc.")
    educacao_filhos = st.number_input("Fundo Educacional (Faculdade)", 0.0, value=200000.0, step=5000.0, help="Valor total estimado para educação futura.")
    
    st.markdown("### 3. Recursos Atuais")
    patrimonio_liquido = st.number_input("Investimentos Líquidos (Resgatáveis)", 0.0, value=150000.0, step=5000.0, help="Não conte o imóvel de moradia.")
    seguro_vigente = st.number_input("Seguro de Vida Atual (Morte)", 0.0, value=0.0, step=5000.0)

# --- HEADER ---
st.markdown('<div class="russinvest-header">Calculadora de Proteção</div>', unsafe_allow_html=True)
st.markdown('<div class="russinvest-sub">Blindagem Patrimonial e Sucessão</div>', unsafe_allow_html=True)

# --- CÁLCULOS ---
# 1. Necessidades
total_custo_vida = despesa_mensal * 12 * anos_protecao
custo_inventario_estimado = (patrimonio_liquido + dividas_total) * 0.10 # Est. 10% sobre bens para inventário/advogado (Simplificado)

# Ajuste visual do inventário (se tiver imóvel financiado, o inventário é sobre o valor do bem, não da dívida. 
# Aqui assumimos uma simplificação onde 'dividas_total' reflete parte de um bem imobilizado)
total_necessidade = total_custo_vida + dividas_total + educacao_filhos + custo_inventario_estimado

# 2. Disponibilidades
total_disponivel = patrimonio_liquido + seguro_vigente

# 3. Gap
gap = total_necessidade - total_disponivel
gap_final = max(0, gap)

# --- VISUALIZAÇÃO ---

# 1. Box de Resultado Principal
if gap_final > 0:
    st.markdown(f"""
    <div class="result-box result-alert">
        <h3 style="margin:0; display:flex; align-items:center; gap:10px;">⚠️ Déficit de Proteção (GAP)</h3>
        <p style="margin-top:10px; margin-bottom:5px;">Para garantir a segurança da sua família, é necessário um capital adicional de:</p>
        <div style="font-size: 2.5em; font-weight: 800; color: #b91c1c;">{formatar_br(gap_final)}</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="result-box result-success">
        <h3 style="margin:0; display:flex; align-items:center; gap:10px;">✅ Família Protegida</h3>
        <p style="margin-top:10px;">
            Seus recursos atuais ({formatar_br(total_disponivel)}) superam a necessidade calculada ({formatar_br(total_necessidade)}).
            Você tem um excedente de segurança de <b>{formatar_br(abs(gap))}</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)

# 2. Gráfico Waterfall (O Visualizador de Gap)
# Lógica: Necessidades sobem, Recursos descem. O que sobrar é o Gap.

measure = ["absolute", "relative", "relative", "relative", "total", "relative", "relative", "total"]
x_labels = ["Manutenção Vida", "Dívidas", "Educação", "Inv./Sucessão", "Necessidade Total", "Investimentos (-)", "Seguro Atual (-)", "GAP FINAL"]
y_values = [
    total_custo_vida, 
    dividas_total, 
    educacao_filhos, 
    custo_inventario_estimado, 
    None, 
    -patrimonio_liquido, 
    -seguro_vigente, 
    None
]
text_values = [
    formatar_br(total_custo_vida), 
    formatar_br(dividas_total), 
    formatar_br(educacao_filhos), 
    formatar_br(custo_inventario_estimado), 
    formatar_br(total_necessidade), 
    f"- {formatar_br(patrimonio_liquido)}", 
    f"- {formatar_br(seguro_vigente)}", 
    formatar_br(gap_final)
]

fig = go.Figure(go.Waterfall(
    name = "Proteção", orientation = "v",
    measure = measure,
    x = x_labels,
    textposition = "outside",
    text = [f"{v/1000:.0f}k" if isinstance(v, (int, float)) and v != 0 else v for v in y_values],
    y = y_values,
    connector = {"line":{"color":"#94a3b8"}},
    decreasing = {"marker":{"color":"#16a34a"}}, # Verde para recursos (diminuem a necessidade)
    increasing = {"marker":{"color":"#ef4444"}}, # Vermelho para custos
    totals = {"marker":{"color":"#1e293b"}}      # Cinza para totais
))

# Pintar a barra de GAP de cor diferente se for > 0
fig.update_layout(
    title="Composição da Necessidade Financeira",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.2)', tickprefix="R$ "),
    margin=dict(t=40, b=0, l=0, r=0),
    font=dict(family="Inter", color="#64748b")
)
st.plotly_chart(fig, use_container_width=True)

# 3. Tabela de Dados para Relatório
df_display = pd.DataFrame([
    {"Categoria": "1. Manutenção Padrão Vida", "Detalhe": f"{anos_protecao} anos x {formatar_br(despesa_mensal)}/mês", "Valor": formatar_br(total_custo_vida)},
    {"Categoria": "2. Quitação de Dívidas", "Detalhe": "Saldo Devedor Total", "Valor": formatar_br(dividas_total)},
    {"Categoria": "3. Projetos Futuros", "Detalhe": "Fundo Educacional", "Valor": formatar_br(educacao_filhos)},
    {"Categoria": "4. Custos Sucessórios", "Detalhe": "Est. 10% (Inventário/ITCMD)", "Valor": formatar_br(custo_inventario_estimado)},
    {"Categoria": "TOTAL NECESSÁRIO", "Detalhe": "", "Valor": formatar_br(total_necessidade)},
    {"Categoria": "(-) Investimentos Líquidos", "Detalhe": "Reserva Financeira", "Valor": formatar_br(patrimonio_liquido)},
    {"Categoria": "(-) Seguro Atual", "Detalhe": "Apólices Vigentes", "Valor": formatar_br(seguro_vigente)},
    {"Categoria": "GAP (CAPITAL A CONTRATAR)", "Detalhe": "Déficit Descoberto", "Valor": formatar_br(gap_final)},
])

# Mostra tabela simples na tela
with st.expander("📋 Detalhamento dos Valores", expanded=True):
    st.table(df_display)

# --- SIDEBAR EXPORT ---
with st.sidebar:
    st.markdown("---")
    st.markdown("**Exportar**")
    
    html_relatorio = gerar_relatorio_protecao(nome_cliente, gap_final, total_necessidade, total_disponivel, df_display)
    
    st.download_button("📄 Baixar Estudo de Proteção", html_relatorio, f"Protecao_{nome_cliente}.html", "text/html")
    
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("❓ Metodologia"):
        st.info(
            "O cálculo considera a recomposição de renda pelo tempo estipulado, "
            "quitação total de passivos e custos de inventário, deduzindo a liquidez atual."
        )
