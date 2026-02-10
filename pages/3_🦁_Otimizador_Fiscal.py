import streamlit as st
import sys
import os
import numpy as np
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
st.set_page_config(layout="wide", page_title="Russinvest - Tax", page_icon="🔷")

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
    
    /* CARDS DE RESULTADO */
    .result-box { 
        padding: 24px; 
        border-radius: 12px; 
        margin-bottom: 20px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
    }
    .result-green { background: #dcfce7; border-left: 5px solid #16a34a; color: #14532d; }
    .result-blue { background: #dbeafe; border-left: 5px solid #2563eb; color: #1e3a8a; }
    .result-warn { background: #ffedd5; border-left: 5px solid #f97316; color: #9a3412; }
    
    /* KPI CARDS */
    .kpi-container { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
    .kpi-card { 
        background-color: #f1f5f9; 
        padding: 15px; 
        border-radius: 8px; 
        text-align: center; 
        border: 1px solid #e2e8f0; 
        flex: 1;
        min-width: 140px; 
    }
    .kpi-label { font-size: 0.8rem; color: #64748b; font-weight: 600; text-transform: uppercase; }
    .kpi-value { font-size: 1.3rem; color: #0f172a; font-weight: 700; margin-top: 5px; }
    
    /* SIDEBAR */
    .sidebar-brand {
        background-color: #f8fafc;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 25px;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    @media (prefers-color-scheme: dark) {
        .sidebar-brand { background-color: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); }
        .brand-title { color: #60a5fa !important; }
    }
    .brand-flex { display: flex; justify-content: center; align-items: center; gap: 10px; margin-bottom: 5px; }
    .brand-icon { font-size: 1.5rem; }
    .brand-title { color: #0066ff; font-size: 1.6rem; font-weight: 800; letter-spacing: -0.5px; margin: 0; }
    .brand-subtitle { color: #94a3b8; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; font-weight: 600; margin-top: 2px; }
    
    /* HELP TEXT */
    .help-title { font-weight: 700; color: #60a5fa; margin-bottom: 5px; margin-top: 10px; display: block;}
    .help-text { font-size: 0.85rem; line-height: 1.5; color: inherit; }
    
    /* Tabela Customizada */
    .dataframe { width: 100% !important; }
</style>
""", unsafe_allow_html=True)

# --- FUNÇÃO FORMATAÇÃO BR ---
def formatar_br(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- HELPERS: CÁLCULOS ESTIMADOS ---
TETO_INSS_MENSAL = 7786.02
def calcular_inss_clt_anual(renda_bruta_anual):
    salario_mensal = renda_bruta_anual / 13.33 
    faixas = [(1412.00, 0.075), (2666.68, 0.09), (4000.03, 0.12), (TETO_INSS_MENSAL, 0.14)]
    inss_mensal = 0; base_anterior = 0; salario_calc = min(salario_mensal, TETO_INSS_MENSAL)
    for limite, aliquota in faixas:
        if salario_calc > base_anterior:
            base_faixa = min(salario_calc, limite) - base_anterior
            inss_mensal += base_faixa * aliquota
            base_anterior = limite
        else: break
    return inss_mensal * 13.33

def calcular_inss_autonomo_anual(renda_bruta_servicos):
    renda_mensal = renda_bruta_servicos / 12
    base_contribuicao = min(renda_mensal, TETO_INSS_MENSAL)
    return (base_contribuicao * 0.20) * 12

def calcular_irpf_anual(base_calculo):
    if base_calculo <= 27000: return 0
    elif base_calculo <= 36000: return (base_calculo * 0.075) - 2000
    elif base_calculo <= 48000: return (base_calculo * 0.15) - 4700
    elif base_calculo <= 60000: return (base_calculo * 0.225) - 8300
    else: return (base_calculo * 0.275) - 11300

# --- GERADOR HTML (ADAPTADO) ---
def gerar_html_tax(cliente, modulo, dados_input, conclusao_html, tabela_html):
    data_hoje = datetime.now().strftime("%d/%m/%Y")
    params_html = ""
    for k, v in dados_input.items():
        params_html += f"<tr><td style='padding: 8px; border-bottom: 1px solid #eee; color: #666;'>{k}</td><td style='padding: 8px; border-bottom: 1px solid #eee; font-weight: 600; text-align: right;'>{v}</td></tr>"

    return f"""
    <html>
    <head><style>
        body {{ font-family: Helvetica, Arial, sans-serif; padding: 40px; color: #333; }}
        .header {{ text-align: center; border-bottom: 2px solid #0066ff; padding-bottom: 20px; margin-bottom: 30px; }}
        .brand {{ color: #0066ff; font-size: 24px; font-weight: 800; }}
        .title {{ font-size: 24px; font-weight: 700; color: #1e293b; margin-bottom: 20px; }}
        .box {{ background: #f8fafc; border-left: 5px solid #0055ff; padding: 20px; margin-bottom: 30px; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 13px; margin-top: 20px; }}
        th {{ background: #f1f5f9; padding: 10px; text-align: right; }}
        td {{ border-bottom: 1px solid #eee; padding: 8px; text-align: right; }}
    </style></head>
    <body>
        <div class="header">
            <div class="brand">Russinvest 🔷</div>
            <div>Otimizador Fiscal</div>
            <div style="font-size: 14px; color: #666; margin-top: 5px;">Cliente: {cliente} | Data: {data_hoje}</div>
        </div>
        <div class="title">Relatório: {modulo}</div>
        <div class="box">{conclusao_html}</div>
        <h3>Premissas</h3>
        <table>{params_html}</table>
        <h3>Detalhamento do Cálculo</h3>
        {tabela_html}
    </body></html>
    """

# --- SIDEBAR ---
with st.sidebar:

    nome_cliente = st.text_input("Nome do Cliente", "Visitante")
    
    # SELETOR DE MÓDULO (A GRANDE MUDANÇA)
    modulo_ativo = st.selectbox(
        "🛠️ Módulo de Análise",
        ["1. Comparador de Regime (Simp. vs Comp.)", "2. Otimizador PGBL (Cálculo do Teto)"]
    )
    
    st.markdown("---")
    perfil = st.selectbox("📂 Perfil Tributário", ["CLT (Assalariado)", "Autônomo (Pessoa Física)", "Híbrido (CLT + Autônomo)"])
    
    # 1. RENDAS E LIVRO CAIXA (Inputs comuns aos dois módulos)
    with st.expander("💰 1. Rendas & INSS", expanded=False):
        renda_clt = 0.0; inss_clt = 0.0; renda_autonomo = 0.0; livro_caixa = 0.0; inss_autonomo = 0.0
        
        if "CLT" in perfil or "Híbrido" in perfil:
            st.markdown("**Vínculo CLT**")
            if st.checkbox("📝 Detalhar Salário?", value=False):
                salario_mensal = st.number_input("Salário Bruto Mensal", 0.0, value=10000.0, step=500.0)
                bonus_anual = st.number_input("Bônus Tributável (Anual)", 0.0, step=1000.0)
                renda_clt = (salario_mensal * 13.33) + bonus_anual
                st.caption(f"Total Anual: {formatar_br(renda_clt)}")
            else:
                renda_clt = st.number_input("Salário Bruto Anual", 0.0, value=150000.0 if "CLT" in perfil else 80000.0, step=1000.0)
            
            if st.checkbox("Estimar INSS CLT?", value=True):
                inss_clt = float(f"{calcular_inss_clt_anual(renda_clt):.2f}")
                st.caption(f"INSS Est.: {formatar_br(inss_clt)}")
            else:
                inss_clt = st.number_input("INSS Retido (Manual)", 0.0, value=15000.0, step=500.0)
            st.markdown("---")
            
        if "Autônomo" in perfil or "Híbrido" in perfil:
            st.markdown("**Atividade Autônoma**")
            renda_autonomo = st.number_input("Receita Bruta Serviços", 0.0, value=200000.0 if "Autônomo" in perfil else 100000.0, step=1000.0)
            livro_caixa = st.number_input("Despesas Livro Caixa", 0.0, value=40000.0 if "Autônomo" in perfil else 10000.0, step=500.0)
            
            if st.checkbox("Estimar INSS Autônomo?", value=True):
                inss_autonomo = float(f"{calcular_inss_autonomo_anual(renda_autonomo):.2f}")
                st.caption(f"INSS Est.: {formatar_br(inss_autonomo)}")
            else:
                inss_autonomo = st.number_input("INSS Pago (Manual)", 0.0, value=12000.0, step=500.0)

    # 2. DEDUÇÕES
    with st.expander("📉 2. Deduções Pessoais", expanded=False):
        num_dependentes = st.number_input("Nº Dependentes", 0, 10, 1)
        gastos_saude = st.number_input("Despesas Médicas", 0.0, value=5000.0, step=500.0)
        gastos_educacao = st.number_input("Despesas Educação", 0.0, value=4000.0, step=500.0)
        
    with st.expander("🏦 3. Previdência Atual", expanded=False):
        pgbl_atual = st.number_input("PGBL já realizado este ano", 0.0, value=0.0, step=500.0)

# --- HEADER ---
col_head, col_empty = st.columns([3, 1])
with col_head:
    st.markdown('<div class="russinvest-header">Otimizador Fiscal</div>', unsafe_allow_html=True)
    if "Comparador" in modulo_ativo:
        st.markdown('<div class="russinvest-sub">Comparador: Simplificado vs Completo</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="russinvest-sub">Calculadora de Aporte PGBL (Modelo Completo)</div>', unsafe_allow_html=True)

# --- CÁLCULOS TRIBUTÁRIOS COMUNS ---
TETO_DESCONTO_SIMPLIFICADO = 16754.34
DEDUCAO_POR_DEPENDENTE = 2275.08
LIMITE_EDUCACAO = 3561.50

renda_autonomo_liquida = max(0, renda_autonomo - livro_caixa)
renda_bruta_total_tributavel = renda_clt + renda_autonomo_liquida
total_inss = inss_clt + inss_autonomo
deducao_dependentes = num_dependentes * DEDUCAO_POR_DEPENDENTE
limite_educacao_total = (num_dependentes + 1) * LIMITE_EDUCACAO
educacao_dedutivel = min(gastos_educacao, limite_educacao_total)
deducoes_legais_base = total_inss + deducao_dependentes + gastos_saude + educacao_dedutivel

# --- LÓGICA MÓDULO 1: COMPARADOR ---
if "Comparador" in modulo_ativo:
    
    # Simplificado
    desconto_simplificado = min(renda_bruta_total_tributavel * 0.20, TETO_DESCONTO_SIMPLIFICADO)
    base_simp = renda_bruta_total_tributavel - desconto_simplificado
    imposto_simp = calcular_irpf_anual(base_simp)
    
    # Completo (Considerando APENAS o PGBL que o cliente JÁ fez)
    base_comp = renda_bruta_total_tributavel - deducoes_legais_base - pgbl_atual
    imposto_comp = calcular_irpf_anual(base_comp)
    
    economia = imposto_simp - imposto_comp
    
    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Imposto Estimado (Simplificado)", formatar_br(imposto_simp))
    col2.metric("Imposto Estimado (Completo)", formatar_br(imposto_comp))
    
    melhor_opcao = "Simplificado" if imposto_simp < imposto_comp else "Completo"
    
    if melhor_opcao == "Simplificado":
        col3.metric("Melhor Opção", "SIMPLIFICADO", delta=f"Economiza {formatar_br(abs(economia))}")
        st.markdown(f"""
        <div class="result-box result-warn">
            <h3 style="margin:0;">⚠️ Veredito: Fique no Simplificado</h3>
            <p>Com as deduções atuais, o desconto padrão de 20% ({formatar_br(desconto_simplificado)}) vale mais a pena.</p>
            <ul>
                <li>Suas deduções comprovadas somam: <b>{formatar_br(deducoes_legais_base + pgbl_atual)}</b></li>
                <li>Diferença a favor do simplificado: <b>{formatar_br(desconto_simplificado - (deducoes_legais_base + pgbl_atual))}</b> de base.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        conclusao_txt = f"Recomendado Modelo SIMPLIFICADO. Economia de {formatar_br(abs(economia))}."
    else:
        col3.metric("Melhor Opção", "COMPLETO", delta=f"Economiza {formatar_br(economia)}")
        st.markdown(f"""
        <div class="result-box result-green">
            <h3 style="margin:0;">✅ Veredito: Declaração Completa</h3>
            <p>Suas despesas dedutíveis já superam o limite do desconto simplificado.</p>
            <ul>
                <li><b>Dica:</b> Vá para o <i>Módulo 2 (Otimizador PGBL)</i> para ver se consegue reduzir ainda mais esse imposto.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        conclusao_txt = f"Recomendado Modelo COMPLETO. Economia de {formatar_br(economia)}."

    # Tabela Comparativa
    df_compare = pd.DataFrame({
        "Conceito": ["(+) Renda Tributável", "(-) Desconto Padrão (20%)", "(-) INSS/Dependentes/Saúde/Edu", "(-) PGBL Efetuado", "(=) Base de Cálculo", "(=) Imposto Devido"],
        "Simplificado": [formatar_br(renda_bruta_total_tributavel), formatar_br(desconto_simplificado), "-", "-", formatar_br(base_simp), formatar_br(imposto_simp)],
        "Completo": [formatar_br(renda_bruta_total_tributavel), "-", formatar_br(deducoes_legais_base), formatar_br(pgbl_atual), formatar_br(base_comp), formatar_br(imposto_comp)]
    })
    st.table(df_compare)
    
    html_export = gerar_html_tax(nome_cliente, "Comparador de Regime", {"Renda Total": formatar_br(renda_bruta_total_tributavel)}, conclusao_txt, df_compare.to_html())

# --- LÓGICA MÓDULO 2: OTIMIZADOR PGBL ---
else:
    teto_pgbl_permitido = renda_bruta_total_tributavel * 0.12
    gap_pgbl = max(0, teto_pgbl_permitido - pgbl_atual)
    restituicao_potencial = gap_pgbl * 0.275
    
    # KPIs PGBL
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Renda Base (Anual)", formatar_br(renda_bruta_total_tributavel))
    kpi2.metric("Limite PGBL (12%)", formatar_br(teto_pgbl_permitido))
    
    if gap_pgbl > 0:
        kpi3.metric("Disponível p/ Aporte", formatar_br(gap_pgbl), delta="Aportar até 31/12")
        
        st.markdown(f"""
        <div class="result-box result-blue">
            <h3 style="margin:0;">🚀 Oportunidade Encontrada</h3>
            <p>Você pode abater mais <b>{formatar_br(gap_pgbl)}</b> da sua base de cálculo.</p>
            <ul>
                <li><b>Benefício Fiscal Estimado:</b> Ao aportar esse valor, você deixa de pagar (ou restitui) aprox. <b>{formatar_br(restituicao_potencial)}</b> (27,5%).</li>
                <li><b>Efeito Prático:</b> É como investir com um "cashback" imediato do Leão.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        conclusao_txt = f"Oportunidade de Aporte PGBL: {formatar_br(gap_pgbl)}. Potencial retorno fiscal: {formatar_br(restituicao_potencial)}."
    else:
        kpi3.metric("Status", "Limite Atingido", delta="Parabéns", delta_color="off")
        st.markdown(f"""
        <div class="result-box result-green">
            <h3 style="margin:0;">✅ Eficiência Máxima Atingida</h3>
            <p>Você já utilizou todo o benefício dos 12%. Novos aportes devem ir para <b>VGBL</b> ou outros investimentos.</p>
        </div>
        """, unsafe_allow_html=True)
        conclusao_txt = "Limite de 12% já atingido. Não aportar mais em PGBL."

    # Waterfall Chart (Visual do PGBL)
    x_data = ["Renda Bruta", "Deduções Legais", "PGBL Atual", "Novo Aporte (Gap)", "Base Final Otimizada"]
    y_data = [renda_bruta_total_tributavel, -deducoes_legais_base, -pgbl_atual, -gap_pgbl, None]
    
    fig = go.Figure(go.Waterfall(
        name = "20", orientation = "v", measure = ["absolute", "relative", "relative", "relative", "total"],
        x = x_data, y = y_data, textposition = "outside", text = [f"{y/1000:.0f}k" if y else "" for y in y_data],
        connector = {"line":{"color":"#cbd5e1"}},
        decreasing = {"marker":{"color":"#ef4444"}}, increasing = {"marker":{"color":"#2563eb"}}, totals = {"marker":{"color":"#16a34a"}}
    ))
    fig.update_layout(
        title="Formação da Base de Cálculo (Modelo Completo)", 
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        yaxis_tickprefix="R$ ", margin=dict(t=30,b=0,l=0,r=0), font=dict(family="Inter", color="#64748b")
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Dados para Exportação
    df_pgbl = pd.DataFrame({
        "Item": x_data[:-1], "Valor": [formatar_br(v) for v in y_data[:-1]]
    })
    html_export = gerar_html_tax(nome_cliente, "Otimização PGBL", {"Limite 12%": formatar_br(teto_pgbl_permitido)}, conclusao_txt, df_pgbl.to_html())

# --- SIDEBAR: EXTRAS ---
with st.sidebar:
    st.markdown("---")
    st.markdown("**Exportar**")
    
    st.download_button(
        label="📄 Baixar Relatório Oficial",
        data=html_export,
        file_name=f"Relatorio_Tax_{nome_cliente.replace(' ', '_')}.html",
        mime="text/html"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("❓ Entenda o Cálculo (Help)"):
        st.markdown("""
        <span class='help-title'>1. PGBL vs VGBL</span>
        <div class='help-text'>
        <b>PGBL:</b> Permite abater até 12% da renda bruta anual da base de cálculo do IR. Indicado para quem faz declaração Completa.<br>
        <b>VGBL:</b> Não tem benefício fiscal na entrada, mas no saque o imposto incide só sobre o lucro. Indicado para quem faz Simplificada ou já estourou os 12%.
        </div>
        
        <span class='help-title'>2. Modelo Simplificado</span>
        <div class='help-text'>
        Substitui todas as deduções (médico, escola, PGBL) por um desconto padrão de 20% da renda, limitado a aprox. R$ 16.754.
        </div>
        
        <span class='help-title'>3. A Armadilha do PGBL</span>
        <div class='help-text'>
        Se suas despesas dedutíveis são baixas, mesmo colocando dinheiro em PGBL, o desconto de 20% do simplificado pode ser maior. Por isso, use sempre o <b>Comparador</b> antes de decidir.
        </div>
        """, unsafe_allow_html=True)
