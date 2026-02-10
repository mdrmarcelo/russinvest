import streamlit as st
import sys
import os
import pandas as pd
import numpy as np
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
st.set_page_config(layout="wide", page_title="Russinvest - Renda Fixa", page_icon="📊")

# --- CSS OTIMIZADO ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .russinvest-header { font-family: 'Inter', sans-serif; font-weight: 800; letter-spacing: -1.5px; line-height: 1.1; color: inherit; }
    @media (min-width: 768px) { .russinvest-header { font-size: 2.8em; } }
    @media (max-width: 767px) { .russinvest-header { font-size: 1.8em; letter-spacing: -0.5px; } .russinvest-sub { font-size: 0.9em !important; margin-bottom: 20px !important; } }
    .russinvest-sub { color: #0066ff; font-size: 1.1em; font-weight: 600; margin-top: 5px; margin-bottom: 35px; border-left: 4px solid #0066ff; padding-left: 12px; }
    .result-box { padding: 24px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .result-green { background: #dcfce7; border-left: 5px solid #16a34a; color: #14532d; }
    .result-blue { background: #dbeafe; border-left: 5px solid #2563eb; color: #1e3a8a; }
    .kpi-container { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
    .kpi-card { background-color: #f1f5f9; padding: 15px; border-radius: 8px; text-align: center; border: 1px solid #e2e8f0; flex: 1; min-width: 140px; }
    .kpi-label { font-size: 0.8rem; color: #64748b; font-weight: 600; text-transform: uppercase; }
    .kpi-value { font-size: 1.3rem; color: #0f172a; font-weight: 700; margin-top: 5px; }
    .sidebar-brand { background-color: #f8fafc; padding: 20px; border-radius: 12px; margin-bottom: 25px; text-align: center; border: 1px solid #e2e8f0; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    @media (prefers-color-scheme: dark) { .sidebar-brand { background-color: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); } .brand-title { color: #60a5fa !important; } }
    .brand-flex { display: flex; justify-content: center; align-items: center; gap: 10px; margin-bottom: 5px; }
    .brand-title { color: #0066ff; font-size: 1.6rem; font-weight: 800; letter-spacing: -0.5px; margin: 0; }
    .brand-subtitle { color: #94a3b8; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; font-weight: 600; margin-top: 2px; }
</style>
""", unsafe_allow_html=True)

def formatar_br(valor): return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
def formatar_pct(valor): return f"{valor*100:.2f}%"

# --- FUNÇÃO GERADORA DE RELATÓRIO PROFISSIONAL ---
def gerar_relatorio_rf(cliente, vencedor, diff, gross_up, df_detalhe):
    data_hoje = datetime.now().strftime("%d/%m/%Y")
    cor_box = "#dcfce7" if "A (" in vencedor else "#dbeafe"
    cor_border = "#16a34a" if "A (" in vencedor else "#2563eb"
    
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
            .winner-box {{ background-color: {cor_box}; border-left: 6px solid {cor_border}; padding: 20px; border-radius: 8px; margin-bottom: 30px; }}
            .winner-title {{ font-weight: bold; font-size: 16px; margin-bottom: 5px; color: #0f172a; }}
            .kpi-row {{ display: flex; gap: 20px; margin-bottom: 30px; }}
            .kpi {{ flex: 1; background: #f8fafc; padding: 15px; border-radius: 6px; text-align: center; border: 1px solid #e2e8f0; }}
            .kpi-lbl {{ font-size: 11px; text-transform: uppercase; color: #64748b; font-weight: bold; }}
            .kpi-val {{ font-size: 18px; font-weight: 700; color: #0f172a; margin-top: 5px; }}
            table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
            th {{ background-color: #f1f5f9; padding: 12px; text-align: left; color: #475569; border-bottom: 2px solid #e2e8f0; }}
            td {{ padding: 10px; border-bottom: 1px solid #f1f5f9; color: #334155; }}
            .footer {{ margin-top: 50px; text-align: center; font-size: 11px; color: #94a3b8; border-top: 1px solid #e2e8f0; padding-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="brand">Russinvest 🔷</div>
            <div class="sub">Fixed Income Analytics</div>
            <div style="margin-top: 10px; font-size: 14px;">Cliente: <b>{cliente}</b> | Data: {data_hoje}</div>
        </div>

        <div class="title">Análise Comparativa de Renda Fixa</div>

        <div class="winner-box">
            <div class="winner-title">🏆 Melhor Opção: {vencedor}</div>
            <div>A vantagem financeira líquida estimada é de <b>{formatar_br(diff)}</b> ao final do período.</div>
        </div>

        <div class="kpi-row">
            <div class="kpi">
                <div class="kpi-lbl">Taxa de Equilíbrio (Gross-up)</div>
                <div class="kpi-val">{gross_up:.2f}% do CDI</div>
                <div style="font-size: 10px; color: #666; margin-top: 3px;">Necessário para empatar</div>
            </div>
            <div class="kpi">
                <div class="kpi-lbl">Diferença Financeira</div>
                <div class="kpi-val" style="color: {cor_border};">+{formatar_br(diff)}</div>
            </div>
        </div>

        <h3 style="font-size: 16px; color: #1e293b; border-bottom: 1px solid #e2e8f0; padding-bottom: 10px;">Detalhamento Técnico</h3>
        {df_detalhe.to_html(index=False, border=0)}
        
        <div class="footer">Relatório gerado pelo Sistema Russinvest. As rentabilidades são estimativas baseadas nas taxas de mercado atuais.</div>
    </body>
    </html>
    """
    return html

# --- SIDEBAR ---
with st.sidebar:

    nome_cliente = st.text_input("Nome do Cliente", "Visitante")
    
    with st.expander("⚙️ Parâmetros de Mercado", expanded=True):
        cdi_meta = st.number_input("CDI/Selic Anual (%)", 0.0, value=10.75, step=0.25) / 100
        dias_uteis = st.slider("Prazo do Investimento (Dias Úteis)", 1, 1500, 365)
    
    with st.expander("🏦 Opção A: Tributável", expanded=True):
        taxa_a_pct = st.number_input("Taxa (% do CDI)", 0.0, value=110.0, step=1.0) / 100
    
    with st.expander("🛡️ Opção B: Isento", expanded=True):
        taxa_b_pct = st.number_input("Taxa (% do CDI) ", 0.0, value=90.0, step=1.0) / 100
        
    valor_investimento = st.number_input("Valor a Investir (R$)", value=10000.0, step=1000.0)

# --- HEADER ---
st.markdown('<div class="russinvest-header">Comparador Renda Fixa</div>', unsafe_allow_html=True)
st.markdown('<div class="russinvest-sub">Tributável (CDB) vs Isento (LCI/LCA)</div>', unsafe_allow_html=True)

# --- CÁLCULO ---
dias_corridos = dias_uteis * 1.4 
if dias_corridos <= 180: aliquota_ir = 0.225
elif dias_corridos <= 360: aliquota_ir = 0.20
elif dias_corridos <= 720: aliquota_ir = 0.175
else: aliquota_ir = 0.15

fator_prazo = dias_uteis / 252
taxa_a_anual = cdi_meta * taxa_a_pct
fator_a_bruto = (1 + taxa_a_anual)**fator_prazo
bruto_a = valor_investimento * fator_a_bruto
lucro_bruto_a = bruto_a - valor_investimento
imposto_a = lucro_bruto_a * aliquota_ir
liquido_a = bruto_a - imposto_a
rentab_liq_a_pct = (liquido_a / valor_investimento) - 1
rentab_liq_a_cdi = (rentab_liq_a_pct / ((1 + cdi_meta)**fator_prazo - 1)) if cdi_meta > 0 else 0

taxa_b_anual = cdi_meta * taxa_b_pct
fator_b = (1 + taxa_b_anual)**fator_prazo
liquido_b = valor_investimento * fator_b
lucro_liquido_b = liquido_b - valor_investimento
imposto_b = 0.0
rentab_liq_b_pct = (liquido_b / valor_investimento) - 1
rentab_liq_b_cdi = (rentab_liq_b_pct / ((1 + cdi_meta)**fator_prazo - 1)) if cdi_meta > 0 else 0

taxa_equivalente_cdi = taxa_b_pct / (1 - aliquota_ir)
diff_financeira = liquido_a - liquido_b
vencedor = "A (Tributável)" if liquido_a > liquido_b else "B (Isento)"

# --- VISUALIZAÇÃO ---
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Alíquota IR (Estimada)", f"{aliquota_ir*100:.1f}%")
kpi2.metric("Rentabilidade Líq. A (CDB)", f"{rentab_liq_a_cdi*100:.1f}% do CDI")
kpi3.metric("Rentabilidade Líq. B (LCI)", f"{rentab_liq_b_cdi*100:.1f}% do CDI")
st.write("")

if vencedor == "A (Tributável)":
    st.markdown(f"""<div class="result-box result-green"><h3 style="margin:0;">🏆 Vencedor: Opção A (CDB/LC)</h3><p>Vantagem de <b>{formatar_br(diff_financeira)}</b> líquidos.</p></div>""", unsafe_allow_html=True)
else:
    st.markdown(f"""<div class="result-box result-blue"><h3 style="margin:0;">🏆 Vencedor: Opção B (LCI/LCA)</h3><p>Vantagem de <b>{formatar_br(abs(diff_financeira))}</b> líquidos.</p></div>""", unsafe_allow_html=True)

fig = go.Figure()
fig.add_trace(go.Bar(x=['Tributável (Bruto)', 'Tributável (Líquido)', 'Isento (Líquido)'], y=[bruto_a, liquido_a, liquido_b], text=[formatar_br(bruto_a), formatar_br(liquido_a), formatar_br(liquido_b)], textposition='auto', marker_color=['#94a3b8', '#2563eb', '#16a34a']))
fig.update_layout(title="Resultado Final no Bolso (R$)", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.2)', tickprefix="R$ "), margin=dict(t=40, b=0, l=0, r=0), font=dict(family="Inter", color="#64748b"))
st.plotly_chart(fig, use_container_width=True)

with st.expander("📋 Detalhamento Numérico", expanded=True):
    df_detalhe = pd.DataFrame({
        "Indicador": ["Valor Investido", "Taxa Bruta (% CDI)", "Valor Final Bruto", "Imposto de Renda", "Valor Final Líquido", "Rentab. Líquida (% CDI)"],
        "Opção A (Tributável)": [formatar_br(valor_investimento), f"{taxa_a_pct*100:.1f}%", formatar_br(bruto_a), f"- {formatar_br(imposto_a)}", f"<b>{formatar_br(liquido_a)}</b>", f"{rentab_liq_a_cdi*100:.1f}%"],
        "Opção B (Isento)": [formatar_br(valor_investimento), f"{taxa_b_pct*100:.1f}%", formatar_br(liquido_b), "Isento", f"<b>{formatar_br(liquido_b)}</b>", f"{rentab_liq_b_cdi*100:.1f}%"]
    })
    st.write(df_detalhe.to_html(escape=False, index=False, classes="dataframe"), unsafe_allow_html=True)

# --- EXPORTAR ---
with st.sidebar:
    st.markdown("---")
    st.markdown("**Exportar**")
    
    html_relatorio = gerar_relatorio_rf(nome_cliente, vencedor, abs(diff_financeira), taxa_equivalente_cdi*100, df_detalhe)
    
    st.download_button("📄 Baixar Relatório Oficial", html_relatorio, f"Relatorio_RF_{nome_cliente}.html", "text/html")
    
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("❓ Entenda o Cálculo"):
        st.info("Gross-up: Taxa necessária num investimento tributável para empatar com o isento.")
