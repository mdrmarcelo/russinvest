import streamlit as st
import sys
import os
import numpy as np
import pandas as pd
import plotly.express as px
import numpy_financial as npf
from datetime import datetime, timedelta

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
st.set_page_config(layout="wide", page_title="Russinvest - Independência", page_icon="📈")

# --- CSS OTIMIZADO (IDENTIDADE VISUAL UNIFICADA) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* HEADER RESPONSIVO */
    .russinvest-header { 
        font-family: 'Inter', sans-serif; 
        font-weight: 800; 
        letter-spacing: -1.5px; 
        line-height: 1.1;
        color: inherit; 
    }
    
    @media (min-width: 768px) { .russinvest-header { font-size: 2.8em; } }
    @media (max-width: 767px) { 
        .russinvest-header { font-size: 1.8em; letter-spacing: -0.5px; } 
        .russinvest-sub { font-size: 0.9em !important; margin-bottom: 20px !important; }
    }

    .russinvest-sub { 
        color: #0066ff; 
        font-size: 1.1em; 
        font-weight: 600; 
        margin-top: 5px; 
        margin-bottom: 35px; 
        border-left: 4px solid #0066ff; 
        padding-left: 12px; 
    }
    
    /* CARDS DE RESULTADO (Fundo claro forçado para contraste) */
    .result-box { 
        padding: 24px; 
        border-radius: 12px; 
        margin-bottom: 20px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
        background: #f0fdf4; /* Verde bem claro padrão */
        border-left: 5px solid #16a34a; 
        color: #14532d;
    }
    
    /* KPI CARDS FLEXÍVEIS */
    .kpi-container { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
    .kpi-card { 
        background-color: #f1f5f9; 
        padding: 15px; 
        border-radius: 8px; 
        text-align: center; 
        border: 1px solid #e2e8f0; 
        flex: 1;
        min-width: 140px; /* Garante que não esmague no mobile */
    }
    .kpi-label { font-size: 0.8rem; color: #64748b; font-weight: 600; text-transform: uppercase; }
    .kpi-value { font-size: 1.3rem; color: #0f172a; font-weight: 700; margin-top: 5px; }
    
    /* SIDEBAR (AGORA IGUAL AO IMÓVEIS) */
    .sidebar-brand {
        background-color: #f8fafc;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 25px;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); /* Sombra igual */
    }
    @media (prefers-color-scheme: dark) {
        .sidebar-brand { background-color: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); }
        .brand-title { color: #60a5fa !important; }
    }
    
    /* FLEXBOX DO LOGO (QUE ESTAVA FALTANDO) */
    .brand-flex { display: flex; justify-content: center; align-items: center; gap: 10px; margin-bottom: 5px; }
    .brand-icon { font-size: 1.5rem; }
    .brand-title { color: #0066ff; font-size: 1.6rem; font-weight: 800; letter-spacing: -0.5px; margin: 0; }
    .brand-subtitle { color: #94a3b8; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; font-weight: 600; margin-top: 2px; }
    
    /* HELP TEXT */
    .help-title { font-weight: 700; color: #60a5fa; margin-bottom: 5px; margin-top: 10px; display: block;}
    .help-text { font-size: 0.85rem; line-height: 1.5; color: inherit; }
</style>
""", unsafe_allow_html=True)

def formatar_br(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- FUNÇÃO GERADORA DE RELATÓRIO HTML ---
def gerar_html_aposentadoria(cliente, dados_input, kpis_dict, tabela_html):
    data_hoje = datetime.now().strftime("%d/%m/%Y")
    
    # Gera HTML das premissas
    params_html = ""
    for k, v in dados_input.items():
        params_html += f"<tr><td style='padding: 8px; border-bottom: 1px solid #eee; color: #666;'>{k}</td><td style='padding: 8px; border-bottom: 1px solid #eee; font-weight: 600; text-align: right;'>{v}</td></tr>"

    html_template = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Helvetica', 'Arial', sans-serif; padding: 40px; max-width: 800px; margin: 0 auto; color: #333; background-color: white; }}
            .header {{ text-align: center; margin-bottom: 40px; border-bottom: 2px solid #0066ff; padding-bottom: 20px; }}
            .brand {{ color: #0066ff; font-size: 24px; font-weight: 800; }}
            .sub {{ color: #999; letter-spacing: 2px; text-transform: uppercase; font-size: 10px; font-weight: bold; }}
            .meta {{ margin-top: 10px; font-size: 14px; color: #666; }}
            .title {{ font-size: 28px; font-weight: 700; margin-bottom: 10px; color: #1e293b; }}
            
            .kpi-grid {{ display: flex; gap: 15px; margin-bottom: 30px; }}
            .kpi-box {{ flex: 1; background: #f8fafc; border: 1px solid #e2e8f0; padding: 15px; border-radius: 8px; text-align: center; }}
            .kpi-lbl {{ font-size: 11px; text-transform: uppercase; color: #666; font-weight: bold; }}
            .kpi-val {{ font-size: 18px; font-weight: 800; color: #0f172a; margin-top: 5px; }}
            
            h3 {{ font-size: 16px; border-bottom: 1px solid #ddd; padding-bottom: 5px; margin-bottom: 15px; color: #0f172a; margin-top: 30px; }}
            
            table.main-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
            table.main-table th {{ background-color: #f1f5f9; padding: 10px; text-align: right; color: #475569; }}
            table.main-table td {{ border-bottom: 1px solid #eee; padding: 8px; text-align: right; }}
            
            .footer {{ margin-top: 50px; text-align: center; font-size: 12px; color: #aaa; border-top: 1px solid #eee; padding-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="brand">Russinvest 🔷</div>
            <div class="sub">Consultoria Financeira</div>
            <div class="meta">Cliente: <b>{cliente}</b> | Data: {data_hoje}</div>
        </div>
        
        <div class="title">Planejamento de Independência Financeira</div>
        
        <div class="kpi-grid">
            <div class="kpi-box"><div class="kpi-lbl">Patrimônio na Aposentadoria</div><div class="kpi-val">{kpis_dict['pat_fim']}</div></div>
            <div class="kpi-box"><div class="kpi-lbl">Meta Necessária</div><div class="kpi-val">{kpis_dict['meta_fim']}</div></div>
            <div class="kpi-box"><div class="kpi-lbl">Aporte Sugerido (Ideal)</div><div class="kpi-val" style="color: #16a34a;">{kpis_dict['aporte_ideal']}</div></div>
        </div>

        <div style="display: flex; gap: 40px;">
            <div style="flex: 1;">
                <h3>Premissas Adotadas</h3>
                <table style="width: 100%; border-collapse: collapse; font-size: 13px;">{params_html}</table>
            </div>
        </div>

        <h3>Evolução Anual (Valores Reais - Poder de Compra)</h3>
        <table class="main-table">
            <thead>
                <tr>
                    <th style="text-align: center;">Idade</th>
                    <th style="text-align: center;">Fase</th>
                    <th>Patrimônio Projetado</th>
                    <th>Caminho Ideal</th>
                </tr>
            </thead>
            <tbody>
                {tabela_html}
            </tbody>
        </table>

        <div class="footer">Relatório gerado automaticamente pelo Sistema Russinvest.</div>
    </body>
    </html>
    """
    return html_template

# --- SIDEBAR (AGORA COM O ÍCONE E ESTRUTURA IGUAIS) ---
with st.sidebar:
    
    # 1. Nome do Cliente (Padrão Unificado)
    nome_cliente = st.text_input("Nome do Cliente", "Visitante")
    
    with st.expander("👤 1. Perfil do Cliente", expanded=False):
        idade_atual = st.slider("Idade atual", 18, 80, 35)
        idade_apos = st.slider("Idade Liberdade Financeira", 40, 90, 60)
        idade_fim = st.slider("Expectativa de Vida", 80, 110, 90)
    
    with st.expander("📊 2. Premissas Econômicas", expanded=True):
        taxa_nom = st.number_input("Rentab. Nominal (% a.a.)", 0.0, 30.0, 10.0, format="%.2f", step=0.5) / 100
        inflacao = st.number_input("Inflação Média (% a.a.)", 0.0, 20.0, 4.0, format="%.2f", step=0.5) / 100
        j_real = (1 + taxa_nom) / (1 + inflacao) - 1
        st.caption(f"📉 **Juro Real:** {j_real*100:.2f}% a.a. (Acima da inflação)")

    with st.expander("💰 3. Aportes e Metas", expanded=False):
        saldo_inicial = st.number_input("Saldo Inicial (R$)", min_value=0.0, value=50000.0, step=1000.0)
        renda_mensal = st.number_input("Renda Desejada (Valores de Hoje)", min_value=0.0, value=10000.0, step=500.0) 
        aporte_mensal = st.number_input("Aporte Mensal Atual (R$)", min_value=0.0, value=2000.0, step=100.0)
        aporte_extra = st.number_input("Aporte Extra Anual (Ex: 13º)", min_value=0.0, value=0.0, step=1000.0)

# --- HEADER RESPONSIVO ---
col_head, col_opt = st.columns([3, 1])
with col_head:
    st.markdown('<div class="russinvest-header">Simulador PRO</div>', unsafe_allow_html=True)
    st.markdown('<div class="russinvest-sub">Planejamento de Independência Financeira</div>', unsafe_allow_html=True)
with col_opt:
    st.write("") # Espaçamento
    tipo_visao = st.radio("👁️ Visualização:", ["Reais (Poder de Compra)", "Nominais (Saldo Futuro)"], horizontal=True)
    is_nominal = "Nominais" in tipo_visao

# --- MOTOR DE CÁLCULO ---
anos_acum = idade_apos - idade_atual
anos_decum = idade_fim - idade_apos
meses_acum = int(anos_acum * 12)
meses_decum = int(anos_decum * 12)
meses_total = meses_acum + meses_decum

r_mes_real = (1 + j_real)**(1/12) - 1
r_mes_inf = (1 + inflacao)**(1/12) - 1 

pat_real = np.zeros(meses_total+1)
pat_sem_nom = np.zeros(meses_total+1) 

pat_real[0] = saldo_inicial
pat_sem_nom[0] = saldo_inicial
ap_total_anual = aporte_mensal * 12 + aporte_extra

# 1. Cálculo Forward (Projeção do Cliente)
for m in range(1, meses_total+1):
    if m <= meses_acum:
        fluxo = aporte_mensal
        if m % 12 == 0: fluxo += aporte_extra
        juros = pat_real[m-1] * r_mes_real
        pat_real[m] = pat_real[m-1] + juros + fluxo
        pat_sem_nom[m] = pat_sem_nom[m-1] + fluxo 
    else:
        # Fase Decumulação (Retirada)
        juros = pat_real[m-1] * r_mes_real
        pat_real[m] = pat_real[m-1] + juros - renda_mensal
        if pat_real[m] < 0: pat_real[m] = 0
        pat_sem_nom[m] = pat_sem_nom[m-1] - renda_mensal
        if pat_sem_nom[m] < 0: pat_sem_nom[m] = 0

# 2. Cálculo Backward (Caminho Ideal/Target)
pat_ideal_real = np.zeros(meses_total+1)
pat_ideal_real[meses_total] = 0
# Trazendo do fim da vida até a aposentadoria
for m in range(meses_total-1, meses_acum, -1):
    pat_ideal_real[m] = (pat_ideal_real[m+1] + renda_mensal) / (1 + r_mes_real)
# O saldo no mês da aposentadoria precisa cobrir o mês seguinte
pat_ideal_real[meses_acum] = (pat_ideal_real[meses_acum+1] + renda_mensal) / (1 + r_mes_real)

target_acum_real = pat_ideal_real[meses_acum]

# Calcula o aporte necessário (PMT) para chegar no target
aporte_ideal_fixo = npf.pmt(r_mes_real, meses_acum, saldo_inicial, -target_acum_real)

# Recalcula a curva ideal partindo do zero com o aporte ideal
pat_ideal_real[0] = saldo_inicial
for m in range(1, meses_acum+1):
    pat_ideal_real[m] = pat_ideal_real[m-1] * (1 + r_mes_real) + aporte_ideal_fixo

# Conversão Real/Nominal para Visualização
fator_inflacao = np.array([(1 + r_mes_inf)**m for m in range(meses_total+1)])

if is_nominal:
    curve_pat = pat_real * fator_inflacao
    curve_ideal = pat_ideal_real * fator_inflacao
    curve_sem = pat_sem_nom 
    lbl_legenda = "Valores Nominais"
else:
    curve_pat = pat_real
    curve_ideal = pat_ideal_real
    curve_sem = pat_sem_nom / fator_inflacao
    lbl_legenda = "Valores Reais"

# --- VISUALIZAÇÃO ---

# 1. KPIs (Layout Mobile Friendly)
val_pat_fim = curve_pat[meses_acum]
val_meta_fim = curve_ideal[meses_acum]
status_texto = "✅ No Caminho" if val_pat_fim >= val_meta_fim else "⚠️ Falta Capital"
cor_status = "#16a34a" if val_pat_fim >= val_meta_fim else "#ea580c"

kpi_html = f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-label">Patrimônio na Aposentadoria</div>
        <div class="kpi-value">{formatar_br(val_pat_fim)}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Meta Necessária</div>
        <div class="kpi-value" style="color: {cor_status};">{formatar_br(val_meta_fim)}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Aporte Atual (Ano)</div>
        <div class="kpi-value">{formatar_br(ap_total_anual)}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Juro Real Efetivo</div>
        <div class="kpi-value">{j_real*100:.2f}% a.a.</div>
    </div>
</div>
"""
st.markdown(kpi_html, unsafe_allow_html=True)

# 2. Box Insight (Estilo Russinvest 10.0)
st.markdown(f"""
<div class="result-box">
    <h3 style="margin:0; font-size: 1.1em; display:flex; align-items:center; gap:8px;">💡 Caminho para a Independência</h3>
    <p style="margin:10px 0 0 0;">
        Para garantir uma renda vitalícia de <b>{formatar_br(renda_mensal)}</b> (poder de compra atual) até os {idade_fim} anos, o aporte mensal sugerido é:
    </p>
    <div style="font-size: 2em; font-weight: 800; margin: 10px 0;">
        {formatar_br(aporte_ideal_fixo)} <span style="font-size: 0.5em; color: #666; font-weight: 600;">/mês</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 3. Gráfico (Plotly Transparente e Otimizado)
indices_anuais = np.arange(0, meses_total+1, 12)
idades_anuais = np.array([idade_atual + m/12 for m in indices_anuais])

df_grafico = pd.DataFrame({
    "Idade": idades_anuais,
    "Seu Plano": curve_pat[indices_anuais],
    "Caminho Ideal": curve_ideal[indices_anuais],
    "Apenas Aportes": curve_sem[indices_anuais]
})

df_melt = df_grafico.melt('Idade', var_name='Cenário', value_name='Valor')
color_map = { "Seu Plano": "#2563eb", "Caminho Ideal": "#16a34a" if not is_nominal else "#059669", "Apenas Aportes": "#94a3b8" }

fig = px.line(df_melt, x="Idade", y="Valor", color='Cenário', color_discrete_map=color_map)

fig.update_traces(mode="lines", line=dict(width=2), fill='tozeroy')
# Opacidade nos preenchimentos
fig.data[0].update(fillcolor="rgba(37, 99, 235, 0.1)")
fig.data[1].update(fillcolor="rgba(22, 163, 74, 0.1)")
fig.data[2].update(fillcolor="rgba(148, 163, 184, 0.1)")

fig.update_layout(
    yaxis_tickprefix="R$ ", 
    plot_bgcolor="rgba(0,0,0,0)", # Transparente para Dark Mode
    paper_bgcolor="rgba(0,0,0,0)",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title=""), 
    margin=dict(t=50, l=10, r=10, b=10),
    font=dict(family="Inter, sans-serif", color="#64748b"), # Texto cinza neutro
    hovermode="x unified"
)
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
fig.add_vline(x=idade_apos, line_width=1, line_dash="dash", line_color="#ef4444", annotation_text="Aposentadoria")

st.markdown(f"**Evolução Patrimonial - {lbl_legenda}**")
st.plotly_chart(fig, use_container_width=True)

# --- TABELA MENSAL ---
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("📋 Detalhamento Mensal (Tabela)", expanded=False):
    idades_mensal = [idade_atual + m/12 for m in range(meses_total+1)]
    datas_mensal = [datetime.now() + timedelta(days=30*m) for m in range(meses_total+1)]
    
    df_mensal = pd.DataFrame({
        "Mês": range(meses_total+1),
        "Data Aprox.": [d.strftime("%m/%Y") for d in datas_mensal],
        "Idade": [f"{i:.2f}" for i in idades_mensal],
        "Seu Plano": curve_pat,
        "Caminho Ideal": curve_ideal,
    })
    
    # Configuração de Colunas para R$
    cols_cfg = {
        "Seu Plano": st.column_config.NumberColumn(format="R$ %.2f"),
        "Caminho Ideal": st.column_config.NumberColumn(format="R$ %.2f")
    }
    st.dataframe(df_mensal, use_container_width=True, column_config=cols_cfg, hide_index=True)

# --- SIDEBAR EXTRAS (HELP + EXPORT) ---
with st.sidebar:
    st.markdown("---")
    st.markdown("**Exportar**")
    
    # Preparando dados para o Relatório HTML
    rows_html = ""
    for i in indices_anuais:
        idade_row = int(idades_anuais[int(i/12)])
        val_real = pat_real[i]
        val_ideal = pat_ideal_real[i]
        fase = "Acumulação" if idade_row < idade_apos else "Decumulação"
        cor_fase = "#16a34a" if fase == "Acumulação" else "#ea580c"
        
        rows_html += f"""
        <tr>
            <td style="text-align: center;">{idade_row} anos</td>
            <td style="text-align: center; color: {cor_fase}; font-weight: bold; font-size: 11px;">{fase}</td>
            <td>{formatar_br(val_real)}</td>
            <td>{formatar_br(val_ideal)}</td>
        </tr>
        """
    
    dados_input_relatorio = {
        "Idade Atual / Aposentadoria": f"{idade_atual} / {idade_apos} anos",
        "Rentabilidade Real": f"{j_real*100:.2f}% a.a.",
        "Renda Desejada": formatar_br(renda_mensal),
        "Aporte Atual": formatar_br(aporte_mensal)
    }
    
    kpis_relatorio = {
        "pat_fim": formatar_br(pat_real[meses_acum]),
        "meta_fim": formatar_br(target_acum_real),
        "aporte_ideal": formatar_br(aporte_ideal_fixo)
    }
    
    html_relatorio = gerar_html_aposentadoria(nome_cliente, dados_input_relatorio, kpis_relatorio, rows_html)
    
    st.download_button(
        label="📄 Baixar Relatório Oficial",
        data=html_relatorio,
        file_name=f"Relatorio_Aposentadoria_{nome_cliente.replace(' ', '_')}.html",
        mime="text/html"
    )

    # --- HELP DISCRETO ---
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("❓ Entenda o Cálculo (Help)"):
        st.markdown("""
        <span class='help-title'>1. Juro Real vs. Nominal</span>
        <div class='help-text'>
        O simulador foca no <b>Juro Real</b> (Rentabilidade - Inflação). Isso é crucial porque R$ 10 mil daqui a 30 anos não comprarão as mesmas coisas que hoje. Ao descontar a inflação, vemos o <b>Poder de Compra</b> real do patrimônio.
        </div>
        
        <span class='help-title'>2. Cálculo "Caminho Ideal"</span>
        <div class='help-text'>
        Fazemos o cálculo de trás para frente (Backward). Primeiro calculamos quanto dinheiro você precisa ter no dia da aposentadoria para pagar sua renda até os {idade_fim} anos. Depois, calculamos quanto precisa investir por mês hoje para chegar nesse montante.
        </div>
        
        <span class='help-title'>3. Fase de Decumulação</span>
        <div class='help-text'>
        Após a aposentadoria, o dinheiro continua rendendo juros reais, mas sofre saques mensais para pagar seu custo de vida. O objetivo é que o saldo chegue a zero (ou perto disso) apenas na idade final estipulada.
        </div>
        """, unsafe_allow_html=True)
