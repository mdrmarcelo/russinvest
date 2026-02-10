import streamlit as st
import sys
import os
import numpy as np
import pandas as pd
import plotly.express as px
import numpy_financial as npf
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

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(layout="wide", page_title="Russinvest", page_icon="🏠")

# --- CSS OTIMIZADO (DARK MODE + MOBILE) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Fontes Globais */
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* HEADER RESPONSIVO */
    .russinvest-header { 
        font-family: 'Inter', sans-serif; 
        font-weight: 800; 
        letter-spacing: -1.5px; 
        line-height: 1.1;
        /* Adapta cor ao tema (herda do Streamlit) */
        color: inherit; 
    }
    
    /* Ajuste de tamanho para Desktop */
    @media (min-width: 768px) {
        .russinvest-header { font-size: 2.8em; }
    }
    
    /* Ajuste de tamanho para Mobile */
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
    
    /* CARDS DE RESULTADO (Fixed Light Theme for Readability) 
       Forçamos um fundo claro e texto escuro nos cards para garantir contraste 
       independente se o app está em Dark ou Light mode. */
    .result-box { 
        padding: 24px; 
        border-radius: 12px; 
        margin-bottom: 20px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
        color: #1e293b; /* Texto sempre escuro dentro do card */
    }
    .result-green { background: #dcfce7; border-left: 5px solid #16a34a; color: #14532d; }
    .result-blue { background: #dbeafe; border-left: 5px solid #2563eb; color: #1e3a8a; }
    
    /* KPI CARDS */
    .kpi-container { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
    .kpi-card { 
        background-color: #f1f5f9; /* Cinza bem claro */
        padding: 15px; 
        border-radius: 8px; 
        text-align: center; 
        border: 1px solid #e2e8f0; 
        flex: 1;
        min-width: 150px; /* Garante tamanho mínimo no mobile */
    }
    .kpi-label { font-size: 0.8rem; color: #64748b; font-weight: 600; text-transform: uppercase; }
    .kpi-value { font-size: 1.3rem; color: #0f172a; font-weight: 700; margin-top: 5px; }
    
    /* SIDEBAR BRANDING */
    .sidebar-brand {
        background-color: #f8fafc; /* Fundo claro na sidebar brand */
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 25px;
        text-align: center;
        border: 1px solid #e2e8f0;
    }
    /* No Dark mode, ajusta levemente a sidebar brand para não ofuscar */
    @media (prefers-color-scheme: dark) {
        .sidebar-brand { background-color: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); }
        .brand-title { color: #60a5fa !important; } /* Azul mais claro no dark */
    }

    .brand-flex { display: flex; justify-content: center; align-items: center; gap: 10px; margin-bottom: 5px; }
    .brand-icon { font-size: 1.5rem; }
    .brand-title { color: #0066ff; font-size: 1.6rem; font-weight: 800; letter-spacing: -0.5px; margin: 0; }
    .brand-subtitle { color: #94a3b8; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; font-weight: 600; margin-top: 2px; }
    
    .caption-value { font-size: 0.85em; color: #64748b; background-color: #f1f5f9; padding: 4px 8px; border-radius: 6px; font-weight: 500; margin-top: -10px; margin-bottom: 12px; display: inline-block; border: 1px solid #e2e8f0; }

    /* HELP TEXT */
    .help-title { font-weight: 700; color: #60a5fa; margin-bottom: 5px; margin-top: 10px; display: block;}
    .help-text { font-size: 0.85rem; line-height: 1.5; color: inherit; }
</style>
""", unsafe_allow_html=True)

def formatar_br(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- FUNÇÃO GERADORA DE RELATÓRIO HTML ---
def gerar_html(cliente, modulo, dados_input, resultado_texto, pl_a, pl_b, diff, vencedor):
    data_hoje = datetime.now().strftime("%d/%m/%Y")
    cor_vencedor = "#16a34a" if vencedor == dados_input.get("label_a", "A") else "#2563eb"
    params_html = ""
    for k, v in dados_input.items():
        if k not in ["label_a", "label_b"]:
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
            .result-card {{ background-color: #f8fafc; border-left: 6px solid {cor_vencedor}; padding: 25px; border-radius: 8px; margin-bottom: 40px; }}
            .winner {{ color: {cor_vencedor}; font-size: 14px; font-weight: 700; text-transform: uppercase; margin-bottom: 5px; }}
            .winner-val {{ font-size: 32px; font-weight: 800; margin: 0; }}
            .diff {{ font-size: 14px; color: #64748b; margin-top: 5px; }}
            .cols {{ display: flex; gap: 40px; margin-bottom: 40px; }}
            .col {{ flex: 1; }}
            table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
            h3 {{ font-size: 16px; border-bottom: 1px solid #ddd; padding-bottom: 5px; margin-bottom: 15px; color: #0f172a; }}
            .footer {{ margin-top: 50px; text-align: center; font-size: 12px; color: #aaa; border-top: 1px solid #eee; padding-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="brand">Russinvest 🔷</div>
            <div class="sub">Consultoria Real Estate</div>
            <div class="meta">Cliente: <b>{cliente}</b> | Data: {data_hoje}</div>
        </div>
        <div class="title">{modulo}</div>
        <div class="result-card">
            <div class="winner">Melhor Opção Financeira</div>
            <div class="winner-val">{vencedor}</div>
            <p style="margin-top: 10px; font-size: 16px;">Vantagem patrimonial de <b>{diff}</b> ao final do período.</p>
        </div>
        <div class="cols">
            <div class="col">
                <h3>Resultado Final (Patrimônio)</h3>
                <div style="margin-bottom: 15px;">
                    <span style="display:block; font-size: 12px; color: #666;">{dados_input.get('label_a')}</span>
                    <span style="font-size: 20px; font-weight: 600;">{pl_a}</span>
                </div>
                <div>
                    <span style="display:block; font-size: 12px; color: #666;">{dados_input.get('label_b')}</span>
                    <span style="font-size: 20px; font-weight: 600;">{pl_b}</span>
                </div>
            </div>
            <div class="col">
                <h3>Premissas Utilizadas</h3>
                <table>{params_html}</table>
            </div>
        </div>
        <div class="footer">Relatório gerado automaticamente pelo Sistema Russinvest.</div>
    </body>
    </html>
    """
    return html_template

# --- SIDEBAR ---
with st.sidebar:
	
    nome_cliente = st.text_input("Nome do Cliente", "Visitante")
    
    modo_simulacao = st.selectbox(
        "Objetivo",
        [
            "Quero Comprar (Financiamento vs Aluguel)", 
            "Quero Comprar (Financiamento vs Consórcio)",
            "Investidor (Comprar p/ Alugar vs Investir)",
            "Tenho Imóvel (Vender vs Manter)",
            "Tenho Dívida (Amortizar vs Investir)"
        ]
    )
    
    # Flags Booleanas
    is_investor = "Investidor" in modo_simulacao
    is_comprar = "Quero Comprar" in modo_simulacao
    is_consorcio = "Consórcio" in modo_simulacao
    is_divida = "Tenho Dívida" in modo_simulacao
    is_imovel = "Tenho Imóvel" in modo_simulacao
    
    # --- INICIALIZAÇÃO SEGURA (Valores padrão) ---
    sistema_amort = "SAC"; entrada_pct = 0.20; taxa_fin = 0.10
    prazo_anos = 30; prazo_cons_meses = 180; prazo_fin_anos = 35
    taxa_adm_total = 0.16; lance_consorcio = 0.0; reajuste_carta = 0.05
    tipo_financiamento_obra = "Chaves"; tipo_imovel = "Pronto"; prazo_obra = 0
    incc_estimado = 0.0; ir_aluguel = 0.275; taxa_adm = 0.10; vacancia_meses = 1
    custo_venda = 0.06; ir_gc = 0.15; valor_aquisicao = 0.0; mes_contemplacao = 1
    tem_parcela_reduzida = False; pct_parcela_reduzida = 1.0
    tipo_lance_consorcio = "Reduzir Prazo"
    custo_manutencao = 0.005; custo_iptu = 0.01; condominio_mensal = 0.0
    tipo_amortizacao = "Reduzir Prazo"; saldo_devedor_atual = 200000.0; valor_aporte = 50000.0
    valorizacao_imovel = 0.0; valor_imovel = 0.0; valor_aluguel = 0.0

    # 1. DADOS DO IMÓVEL (Oculto se for Amortização)
    if not is_divida:
        with st.expander("🏠 1. Dados do Imóvel", expanded=True):
            if 'valor_imovel_input' not in st.session_state: st.session_state.valor_imovel_input = 800000.0
            valor_imovel = st.number_input("Valor de Mercado", min_value=0.0, step=10000.0, key="valor_imovel_input")
            valorizacao_imovel = st.number_input("Valorização (% a.a.)", 0.0, value=4.0, step=0.5) / 100
            
            # Planta
            if not is_imovel and not is_consorcio:
                st.markdown("---")
                tipo_imovel = st.radio("Condição", ["Pronto", "Na Planta"], horizontal=True)
                if tipo_imovel == "Na Planta":
                    prazo_obra = st.number_input("Obras (Meses)", 12, 60, 36)
                    tipo_financiamento_obra = st.selectbox("Tipo Finan. Obra", ["Financiamento na Entrega", "Crédito Associativo"])
                    disable_incc = (tipo_financiamento_obra == "Crédito Associativo")
                    val_incc = 0.0 if disable_incc else 6.0
                    incc_estimado = st.number_input("INCC Estimado (% a.a.)", 0.0, value=val_incc, step=0.5, disabled=disable_incc) / 100
                    if disable_incc: st.caption("ℹ️ Crédito Associativo congela o saldo (sem INCC).")

            # CUSTOS DE PROPRIEDADE
            if is_imovel or is_investor:
                 st.markdown("---")
                 st.markdown("**Despesas do Proprietário**")
                 custo_manutencao = st.number_input("Manutenção/Fundo (% a.a.)", 0.0, value=0.5, step=0.1) / 100
                 custo_iptu = st.number_input("IPTU (% a.a.)", 0.0, value=1.0, step=0.1) / 100
                 condominio_mensal = st.number_input("Condomínio (R$)", 0.0, value=800.0, step=100.0)
                 c_manut_mes = (valor_imovel * custo_manutencao)/12
                 c_iptu_mes = (valor_imovel * custo_iptu)/12
                 st.markdown(f"<div class='caption-value'>Custo Fixo Mensal: {formatar_br(c_manut_mes + c_iptu_mes + condominio_mensal)}</div>", unsafe_allow_html=True)

            st.markdown("---")
            if is_comprar: lbl = "Aluguel Equivalente"
            elif is_investor: lbl = "Aluguel Esperado (Bruto)"
            else: lbl = "Aluguel Novo Lar"
            valor_aluguel = st.number_input(lbl, min_value=0.0, value=valor_imovel*0.0084, step=100.0)
            
            if is_investor:
                st.markdown("**Taxas sobre Aluguel**")
                ir_aluguel = st.number_input("IR Aluguel (% sobre Receita)", 0.0, value=27.5, step=2.5)/100
                taxa_adm = st.number_input("Taxa Imobiliária (% sobre Receita)", 0.0, value=10.0, step=1.0)/100
                vacancia_meses = st.number_input("Vacância Média (Meses/Ano)", 0.0, value=1.0, step=0.5)
    
    # 2. DADOS FINANCEIROS
    if is_divida:
        with st.expander("💳 2. Dados da Dívida", expanded=True):
            saldo_devedor_atual = st.number_input("Saldo Devedor Atual", min_value=0.0, value=200000.0, step=1000.0)
            prazo_anos = st.number_input("Prazo Restante (Meses)", min_value=1, value=300)
            taxa_fin = st.number_input("Taxa de Juros (% a.a.)", 0.0, value=10.5, step=0.1) / 100
            sistema_amort = st.selectbox("Sistema de Amortização", ["SAC", "Price"])
            st.markdown("---")
            st.markdown("**Estratégia**")
            valor_aporte = st.number_input("Valor disponível p/ Aporte", min_value=0.0, value=50000.0, step=1000.0)
            tipo_amortizacao = st.radio("Se amortizar, o que fazer?", ["Reduzir Prazo", "Reduzir Parcela"], horizontal=True)

    elif is_consorcio:
        with st.expander("🆚 2. Financiamento vs Consórcio", expanded=True):
            st.markdown("**Financiamento**")
            prazo_fin_anos = st.slider("Prazo Finan (Anos)", 5, 40, 35)
            entrada_pct = st.slider("% Entrada", 0, 90, 20) / 100
            st.markdown(f"<div class='caption-value'>Valor: {formatar_br(valor_imovel * entrada_pct)}</div>", unsafe_allow_html=True)
            taxa_fin = st.number_input("Taxa Banco (% a.a.)", 0.0, value=10.5, step=0.1) / 100
            sistema_amort = st.selectbox("Amortização", ["SAC", "Price"])
            st.markdown("---")
            st.markdown("**Consórcio**")
            prazo_cons_meses = st.number_input("Prazo (Meses)", 12, 360, 180)
            taxa_adm_total = st.number_input("Taxa Adm Total (%)", 0.0, value=18.0, step=1.0) / 100
            st.markdown(f"<div class='caption-value'>Custo Total: {formatar_br(valor_imovel * taxa_adm_total)}</div>", unsafe_allow_html=True)
            lance_consorcio = st.number_input("Lance (R$)", 0.0, value=valor_imovel*0.4, step=5000.0)
            if lance_consorcio > 0: tipo_lance_consorcio = st.radio("Após o Lance:", ["Reduzir Prazo", "Reduzir Parcela"], horizontal=True)
            reajuste_carta = st.number_input("Reajuste Carta (% a.a.)", 0.0, value=5.0, step=0.5) / 100
            mes_contemplacao = st.number_input("Mês Contemplação", 1, prazo_cons_meses, 1)
            tem_parcela_reduzida = st.checkbox("Parcela Reduzida?")
            if tem_parcela_reduzida:
                pct_reducao = st.slider("Paga quanto % da parcela?", 50, 90, 50); pct_parcela_reduzida = pct_reducao / 100
            
    elif is_comprar or is_investor:
        with st.expander("🏦 2. Financiamento", expanded=True):
            entrada_pct = st.slider("% Entrada", 10, 90, 20) / 100
            st.markdown(f"<div class='caption-value'>Valor: {formatar_br(valor_imovel * entrada_pct)}</div>", unsafe_allow_html=True)
            prazo_anos = st.slider("Prazo (Anos)", 5, 35, 30)
            taxa_fin = st.number_input("Taxa Juros (% a.a.)", 0.0, value=10.5, step=0.1) / 100
            sistema_amort = st.selectbox("Sistema", ["SAC", "Price"])
            
    elif is_imovel:
        with st.expander("💰 2. Custos Venda", expanded=True):
            prazo_anos = st.slider("Prazo (Anos)", 5, 35, 30)
            valor_aquisicao = st.number_input("Vl Aquisição Histórico", value=valor_imovel*0.6)
            custo_venda = st.number_input("Corretagem (%)", 0.0, value=6.0)/100
            st.markdown(f"<div class='caption-value'>Valor: {formatar_br(valor_imovel * custo_venda)}</div>", unsafe_allow_html=True)
            ir_gc = st.number_input("IR Ganho Capital (%)", 0.0, value=15.0)/100
            if valor_imovel > valor_aquisicao:
                lucro_est = valor_imovel - valor_aquisicao; st.markdown(f"<div class='caption-value'>Est. Imposto: {formatar_br(lucro_est * ir_gc)}</div>", unsafe_allow_html=True)

    # 3. CENÁRIO
    with st.expander("📈 3. Cenário Econômico", expanded=True):
        rentabilidade_invest = st.number_input("Rendimento Inv. (% a.a.)", 0.0, value=10.0, step=0.5) / 100
        disable_idx_aluguel = False
        if is_divida: disable_idx_aluguel = True
        elif is_consorcio and mes_contemplacao <= 12: disable_idx_aluguel = True
        val_idx = 0.0 if disable_idx_aluguel and is_divida else 4.5
        reajuste_aluguel_idx = st.number_input("Índice Aluguel (% a.a.)", 0.0, value=val_idx, step=0.5, disabled=disable_idx_aluguel) / 100
        if is_consorcio and disable_idx_aluguel: st.caption("ℹ️ Contemplação rápida (<1 ano) evita reajuste de aluguel.")

# --- HEADER (TITULO) ---
st.markdown(f'<div class="russinvest-header">{modo_simulacao.split("(")[0]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="russinvest-sub">{modo_simulacao.split("(")[1].replace(")", "")}</div>', unsafe_allow_html=True)

# --- MOTOR DE CÁLCULO GERAL ---
if is_consorcio: meses = max(prazo_fin_anos * 12, prazo_cons_meses)
elif is_divida: meses = int(prazo_anos) 
else: meses = prazo_anos * 12

taxa_mes_inv = (1 + rentabilidade_invest)**(1/12) - 1
valorizacao_mes = (1 + valorizacao_imovel)**(1/12) - 1
reajuste_mes_aluguel = (1 + reajuste_aluguel_idx)**(1/12) - 1
incc_mes = (1 + incc_estimado)**(1/12) - 1
taxa_mes_fin = (1 + taxa_fin)**(1/12) - 1
custo_manut_mensal_pct = custo_manutencao / 12
custo_iptu_mensal_pct = custo_iptu / 12

cenario_a, cenario_b = [], []
dados_tabela = []

# --- LÓGICA DE SIMULAÇÃO ---
if is_divida:
    label_a, label_b = "Amortizar (PL)", "Investir Aporte (PL)"
    saldo_dev_a = max(0, saldo_devedor_atual - valor_aporte); prazo_restante_a = meses
    if "SAC" in sistema_amort: amort_orig = saldo_devedor_atual / meses; juros_orig = saldo_devedor_atual * taxa_mes_fin; parc_original_inicial = amort_orig + juros_orig
    else: parc_original_inicial = npf.pmt(taxa_mes_fin, meses, -saldo_devedor_atual)
    saldo_invest_a = 0 
    if tipo_amortizacao == "Reduzir Prazo":
        if "Price" in sistema_amort: novo_nper = npf.nper(taxa_mes_fin, -parc_original_inicial, saldo_dev_a); prazo_restante_a = int(novo_nper) if not np.isnan(novo_nper) else 0
        else: prazo_restante_a = int(meses * (saldo_dev_a / saldo_devedor_atual))
    saldo_dev_b = saldo_devedor_atual; saldo_invest_b = valor_aporte 
    for m in range(1, meses + 1):
        if m <= meses:
            if "SAC" in sistema_amort: amort_b = saldo_dev_b / (meses - m + 1); juros_b = saldo_dev_b * taxa_mes_fin; parc_b = amort_b + juros_b
            else: parc_b = npf.pmt(taxa_mes_fin, meses - m + 1, -saldo_dev_b); amort_b = parc_b - (saldo_dev_b * taxa_mes_fin)
            saldo_dev_b = max(0, saldo_dev_b - amort_b)
        else: parc_b = 0
        saldo_invest_b *= (1 + taxa_mes_inv)
        parc_a = 0
        if m <= prazo_restante_a:
            if "SAC" in sistema_amort: amort_a = saldo_dev_a / (prazo_restante_a - m + 1); juros_a = saldo_dev_a * taxa_mes_fin; parc_a = amort_a + juros_a
            else: parc_a = npf.pmt(taxa_mes_fin, prazo_restante_a - m + 1, -saldo_dev_a); amort_a = parc_a - (saldo_dev_a * taxa_mes_fin)
            saldo_dev_a = max(0, saldo_dev_a - amort_a)
        fluxo_disponivel = parc_b; sobra_a = fluxo_disponivel - parc_a; saldo_invest_a = saldo_invest_a * (1 + taxa_mes_inv) + sobra_a
        pl_a = saldo_invest_a - saldo_dev_a; pl_b = saldo_invest_b - saldo_dev_b
        cenario_a.append(pl_a); cenario_b.append(pl_b)
        dados_tabela.append({"Mês": m, "Invest. (Amortizou)": saldo_invest_a, "Invest. (Não Amortizou)": saldo_invest_b, "PL Amortizou": pl_a, "PL Investiu": pl_b})

elif (is_comprar or is_investor) and not is_consorcio:
    if is_comprar: label_a, label_b = "Comprar", "Alugar"
    else: label_a, label_b = "Imóvel+Renda", "Investimento"
    valor_entrada = valor_imovel * entrada_pct; saldo_a_financiar_inicial = valor_imovel - valor_entrada
    divida_banco = 0; divida_construtora = saldo_a_financiar_inicial 
    if tipo_imovel == "Pronto": divida_banco = saldo_a_financiar_inicial; divida_construtora = 0
    pl_imovel_a = valor_entrada; saldo_invest_a = 0; saldo_invest_b = valor_entrada if is_comprar else valor_imovel
    valor_imovel_atual = valor_imovel; aluguel_atual = valor_aluguel; repasse_mensal = saldo_a_financiar_inicial / prazo_obra if prazo_obra > 0 else 0
    total_juros_pago_a = 0 
    for m in range(1, meses + 1):
        custo_mensal_a = 0; parcela_a = 0      
        if tipo_imovel == "Na Planta" and m <= prazo_obra:
            valor_imovel_atual *= (1 + valorizacao_mes)
            if tipo_financiamento_obra == "Crédito Associativo": 
                divida_banco += repasse_mensal; divida_construtora -= repasse_mensal; 
                juros_obra = divida_banco * taxa_mes_fin; total_juros_pago_a += juros_obra 
                custo_mensal_a = juros_obra
            else: 
                divida_construtora *= (1 + incc_mes); custo_mensal_a = 0; 
                if m == prazo_obra: divida_banco = divida_construtora; divida_construtora = 0
            if is_comprar: custo_total_fluxo_a = custo_mensal_a + aluguel_atual
            else: 
                saldo_invest_a = saldo_invest_a * (1 + taxa_mes_inv) - custo_mensal_a
                custo_total_fluxo_a = custo_mensal_a
        else:
            valor_imovel_atual *= (1 + valorizacao_mes); divida_total = divida_banco + divida_construtora
            juros = divida_total * taxa_mes_fin; total_juros_pago_a += juros 
            prazo_restante = meses - (m if tipo_imovel=="Pronto" else prazo_obra)
            if "SAC" in sistema_amort: amort = divida_total / prazo_restante if prazo_restante > 0 else divida_total; parcela_a = amort + juros
            else: parcela_a = npf.pmt(taxa_mes_fin, prazo_restante, -divida_total) if prazo_restante > 0 else 0; amort = parcela_a - juros
            if divida_banco > 0: divida_banco -= amort
            elif divida_construtora > 0: divida_construtora -= amort
            custo_total_fluxo_a = parcela_a
            if is_investor:
                fator_ocupacao = (12.0 - vacancia_meses) / 12.0
                receita_liq = (aluguel_atual * fator_ocupacao) * (1.0 - taxa_adm - ir_aluguel)
                custo_manut_mensal = valor_imovel_atual * custo_manut_mensal_pct
                custo_vazio = (condominio_mensal + (valor_imovel_atual * custo_iptu_mensal_pct)) * (1.0 - fator_ocupacao)
                despesas_totais = custo_manut_mensal + custo_vazio
                fluxo_caixa_mes = receita_liq - parcela_a - despesas_totais
                saldo_invest_a = saldo_invest_a * (1 + taxa_mes_inv) + fluxo_caixa_mes
        if m > 1 and (m-1) % 12 == 0: aluguel_atual *= (1 + reajuste_mes_aluguel)
        if is_comprar:
            saldo_invest_b = saldo_invest_b * (1 + taxa_mes_inv) + (custo_total_fluxo_a - aluguel_atual)
            val_final_a = valor_imovel_atual - (divida_banco + divida_construtora); val_final_b = saldo_invest_b
        else:
            saldo_invest_b *= (1 + taxa_mes_inv)
            val_final_a = valor_imovel_atual - (divida_banco + divida_construtora) + saldo_invest_a
            val_final_b = saldo_invest_b
        cenario_a.append(val_final_a); cenario_b.append(val_final_b)
        dados_tabela.append({"Mês": m, "PL A": val_final_a, "PL B": val_final_b})

elif is_consorcio:
    label_a, label_b = "Financiamento", "Consórcio"
    entrada_fin = valor_imovel * entrada_pct; divida_fin = valor_imovel - entrada_fin
    carta = valor_imovel; total_cons = carta * (1 + taxa_adm_total); parcela_cons_base = total_cons / prazo_cons_meses
    caixa_inicial = max(entrada_fin, lance_consorcio)
    saldo_invest_fin = 0; saldo_invest_cons = 0
    valor_imovel_fin = valor_imovel; valor_imovel_cons = 0; aluguel_atual_cons = valor_aluguel; divida_cons_restante = total_cons
    prazo_cons_atual = prazo_cons_meses
    if "SAC" in sistema_amort: p_max_fin = (divida_fin / (prazo_fin_anos*12)) + (divida_fin * taxa_mes_fin)
    else: p_max_fin = npf.pmt(taxa_mes_fin, prazo_fin_anos*12, -divida_fin)
    p_max_cons = parcela_cons_base
    fluxo_mensal_disponivel = max(p_max_fin, p_max_cons + aluguel_atual_cons)
    total_juros_fin_acumulado = 0; total_taxas_cons_acumulado = 0; ratio_taxa_cons = taxa_adm_total / (1 + taxa_adm_total)
    for m in range(1, meses + 1):
        if m <= prazo_fin_anos * 12:
            if "SAC" in sistema_amort: amort = divida_fin / (prazo_fin_anos*12 - m + 1); juros = divida_fin * taxa_mes_fin; parc_fin = amort + juros
            else: parc_fin = npf.pmt(taxa_mes_fin, prazo_fin_anos*12 - m + 1, -divida_fin); juros = divida_fin * taxa_mes_fin; amort = parc_fin - juros
            divida_fin = max(0, divida_fin - amort); total_juros_fin_acumulado += juros
        else: parc_fin = 0
        valor_imovel_fin *= (1 + valorizacao_mes)
        if m > 1 and (m-1) % 12 == 0: 
            parcela_cons_base *= (1 + reajuste_carta); divida_cons_restante *= (1 + reajuste_carta); aluguel_atual_cons *= (1 + reajuste_mes_aluguel) 
        parc_c = 0; eh_contemplacao = (m == mes_contemplacao)
        if eh_contemplacao:
            taxa_no_lance = lance_consorcio * ratio_taxa_cons; total_taxas_cons_acumulado += taxa_no_lance
            divida_cons_restante -= lance_consorcio; valor_imovel_cons = valor_imovel_fin 
            meses_restantes = prazo_cons_meses - m + 1
            if meses_restantes > 0:
                if tipo_lance_consorcio == "Reduzir Prazo": novo_prazo = int(divida_cons_restante / parcela_cons_base); prazo_cons_atual = m + novo_prazo - 1 
                else: parcela_cons_base = divida_cons_restante / meses_restantes
        if divida_cons_restante > 0 and m <= prazo_cons_atual:
            parc_c = parcela_cons_base * pct_parcela_reduzida if (m < mes_contemplacao and tem_parcela_reduzida) else parcela_cons_base
            if parc_c > divida_cons_restante: parc_c = divida_cons_restante
            divida_cons_restante -= parc_c; total_taxas_cons_acumulado += (parc_c * ratio_taxa_cons)
        custo_moradia_cons = aluguel_atual_cons if m < mes_contemplacao else 0
        valor_imovel_cons *= (1 + valorizacao_mes)
        sobra_fin = fluxo_mensal_disponivel - parc_fin; sobra_cons = fluxo_mensal_disponivel - (parc_c + custo_moradia_cons)
        saldo_invest_fin = saldo_invest_fin * (1 + taxa_mes_inv) + sobra_fin; saldo_invest_cons = saldo_invest_cons * (1 + taxa_mes_inv) + sobra_cons
        if eh_contemplacao: saldo_invest_cons -= lance_consorcio
        if m == 1: saldo_invest_fin -= entrada_fin
        pl_fin = valor_imovel_fin - divida_fin + saldo_invest_fin; pl_cons = valor_imovel_cons + saldo_invest_cons 
        cenario_a.append(pl_fin); cenario_b.append(pl_cons)
        dados_tabela.append({"Mês": m, "PL Fin": pl_fin, "PL Cons": pl_cons})

elif is_imovel:
    label_a, label_b = "Manter Imóvel", "Vender"
    val_im = valor_imovel; lucro = valor_imovel - valor_aquisicao; ir_pagar = max(0, lucro * ir_gc)
    saldo_inv_a = 0; saldo_inv_b = valor_imovel - ir_pagar - (valor_imovel * custo_venda)
    aluguel_atual = valor_aluguel
    for m in range(1, meses + 1):
        val_im *= (1 + valorizacao_mes)
        if m > 1 and (m-1) % 12 == 0: aluguel_atual *= (1 + reajuste_mes_aluguel)
        custo_a = (val_im * (custo_manut_mensal_pct + custo_iptu_mensal_pct)) + condominio_mensal; custo_b = aluguel_atual
        saldo_inv_a = saldo_inv_a * (1 + taxa_mes_inv) - custo_a; saldo_inv_b = saldo_inv_b * (1 + taxa_mes_inv) - custo_b
        cenario_a.append(val_im + saldo_inv_a); cenario_b.append(saldo_inv_b)
        dados_tabela.append({"Mês": m, "PL Manter": val_im + saldo_inv_a, "PL Vender": saldo_inv_b})

# --- VISUALIZAÇÃO ---
pl_a = cenario_a[-1]; pl_b = cenario_b[-1]; diff = abs(pl_a - pl_b)
vencedor = label_a if pl_a > pl_b else label_b

col1, col2, col3 = st.columns(3)
col1.metric(f"Final {label_a}", formatar_br(pl_a))
col2.metric(f"Final {label_b}", formatar_br(pl_b))
col3.metric("Diferença", formatar_br(diff), delta="Vantagem")

# BOX DO VENCEDOR
if vencedor == label_a: cor="result-green"; icone="🏠"; txt=label_a
else: cor="result-blue"; icone="📈"; txt=label_b
html = f"""<div class="result-box {cor}"><h3 style="margin:0;">{icone} Vencedor: {txt}</h3><p>Vantagem de <b>{formatar_br(diff)}</b>.</p></div>"""
st.markdown(html, unsafe_allow_html=True)

# KPIS ESPECÍFICOS (Layout Flex para Mobile)
if is_comprar and not is_consorcio:
    kpi_html = f"""<div class="kpi-container"><div class="kpi-card"><div class="kpi-label">Juros Totais Pagos</div><div class="kpi-value" style="color: #ef4444;">{formatar_br(total_juros_pago_a)}</div></div><div class="kpi-card"><div class="kpi-label">Valorização do Imóvel</div><div class="kpi-value" style="color: #22c55e;">+{formatar_br(val_final_a - valor_imovel)}</div></div></div>"""
    st.markdown(kpi_html, unsafe_allow_html=True)
if is_consorcio:
    kpi_cons_html = f"""<div class="kpi-container"><div class="kpi-card"><div class="kpi-label">Total Juros (Financ.)</div><div class="kpi-value" style="color: #ef4444;">{formatar_br(total_juros_fin_acumulado)}</div></div><div class="kpi-card"><div class="kpi-label">Total Taxas (Consórcio)</div><div class="kpi-value" style="color: #f59e0b;">{formatar_br(total_taxas_cons_acumulado)}</div></div></div>"""
    st.markdown(kpi_cons_html, unsafe_allow_html=True)

df = pd.DataFrame({"Ano": np.arange(1/12, meses/12 + 1/12, 1/12)[:len(cenario_a)], label_a: cenario_a, label_b: cenario_b})
fig = px.line(df.melt('Ano'), x="Ano", y="value", color='variable', color_discrete_map={label_a: "#0055ff", label_b: "#2ecc71"})

# [AJUSTE PLOTLY] Fundo Transparente para Dark Mode
fig.update_layout(
    yaxis_tickprefix="R$ ", 
    plot_bgcolor="rgba(0,0,0,0)",  # Transparente
    paper_bgcolor="rgba(0,0,0,0)", # Transparente
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title=""), 
    margin=dict(t=50),
    font=dict(color="#64748b") # Cor neutra para texto do gráfico
)
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')

st.plotly_chart(fig, use_container_width=True)

# --- TABELA DETALHADA ---
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("📋 Tabela Detalhada (Mês a Mês)", expanded=False):
    df_det = pd.DataFrame(dados_tabela)
    cols_config = {col: st.column_config.NumberColumn(format="R$ %.2f") for col in df_det.columns if col not in ["Mês", "Ano"]}
    st.dataframe(df_det, use_container_width=True, column_config=cols_config, hide_index=True)

# --- SIDEBAR DOWNLOAD ---
with st.sidebar:
    st.markdown("---")
    st.markdown("**Exportar**")
    
    dados_relatorio = {
        "label_a": label_a, "label_b": label_b, "Valor Imóvel": formatar_br(valor_imovel), 
        "Rentabilidade Inv.": f"{rentabilidade_invest*100:.2f}% a.a.", "Prazo (Anos)": f"{meses/12:.1f}"
    }
    if is_divida: dados_relatorio.update({"Saldo Devedor": formatar_br(saldo_devedor_atual), "Taxa Dívida": f"{taxa_fin*100:.2f}%"})
    elif is_consorcio: dados_relatorio.update({"Taxa Consórcio": f"{taxa_adm_total*100:.2f}%", "Lance": formatar_br(lance_consorcio)})
    else: dados_relatorio.update({"Taxa Financiamento": f"{taxa_fin*100:.2f}%"})
    
    html_relatorio = gerar_html(nome_cliente, modo_simulacao, dados_relatorio, html, formatar_br(pl_a), formatar_br(pl_b), formatar_br(diff), vencedor)
    
    st.download_button(
        label="📄 Baixar Relatório Oficial",
        data=html_relatorio,
        file_name=f"Relatorio_Russinvest_{nome_cliente.replace(' ', '_')}.html",
        mime="text/html"
    )
    
    # --- HELP DISCRETO ---
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("❓ Entenda o Cálculo (Help)"):
        help_text = ""
        if is_comprar:
            help_text = f"""
            <span class='help-title'>Comparativo Comprar vs Alugar</span>
            <div class='help-text'>
            1. <b>Cenário Comprar ({label_a}):</b> Considera a aquisição com {entrada_pct*100}% de entrada. O custo mensal é a Parcela do Financiamento. Ao final, você tem o Imóvel Quitado (valorizado a {valorizacao_imovel*100}% a.a.) menos juros pagos.<br>
            2. <b>Cenário Alugar ({label_b}):</b> A entrada é investida. A diferença entre a Parcela do Financiamento (geralmente mais cara) e o Aluguel é aportada mensalmente na aplicação.<br>
            3. <b>Veredito:</b> Vence quem tiver o maior Patrimônio Líquido (Bens + Dinheiro) no final do prazo.
            </div>
            """
        elif is_consorcio:
            help_text = f"""
            <span class='help-title'>Consórcio vs Financiamento</span>
            <div class='help-text'>
            1. <b>O "Segredo" do Consórcio:</b> Diferente do banco, o consórcio não cobra juros compostos. Ele cobra Taxa de Administração sobre o valor da carta.<br> 
            2. <b>Impacto da Inflação:</b> Se você não quita rápido (Reduz Prazo), sua dívida é reajustada anualmente pelo INCC/IGPM, o que aumenta o valor em reais da taxa de administração paga.<br>
            3. <b>Custo de Oportunidade:</b> O simulador considera que, enquanto você não é contemplado, continua pagando Aluguel. Isso é debitado do resultado do Consórcio.
            </div>
            """
        elif is_investor:
            help_text = f"""
            <span class='help-title'>Lógica do Investidor</span>
            <div class='help-text'>
            1. <b>Receita Real:</b> O Aluguel Bruto ({formatar_br(valor_aluguel)}) sofre descontos de Taxa de Adm ({taxa_adm*100}%) e Imposto de Renda ({ir_aluguel*100}%) antes de entrar no caixa.<br>
            2. <b>Vacância Inteligente:</b> Consideramos {vacancia_meses} meses vazios por ano. Nesses meses, a receita é zero E o proprietário paga Condomínio + IPTU do bolso.<br>
            3. <b>Fluxo de Caixa:</b> A cada mês, (Receita Líquida - Parcela) é reinvestido. Se negativo, o investidor aporta do bolso.
            </div>
            """
        elif is_divida:
            help_text = f"""
            <span class='help-title'>Amortizar ou Investir?</span>
            <div class='help-text'>
            1. <b>Custo Efetivo:</b> Comparamos a taxa de juros da sua dívida ({taxa_fin*100}%) contra a rentabilidade líquida dos seus investimentos ({rentabilidade_invest*100}%).<br>
            2. <b>Alavancagem:</b> Se seus investimentos rendem mais que o custo da dívida, matematicamente vale a pena manter a dívida e acumular capital (Lado B).<br>
            3. <b>Risco:</b> O simulador é puramente matemático.
            </div>
            """
        elif is_imovel:
            help_text = f"""
            <span class='help-title'>Vender ou Manter?</span>
            <div class='help-text'>
            1. <b>Custo de Oportunidade:</b> Se vender o imóvel (Lado B), o dinheiro líquido (descontado IR Ganho Capital e Corretagem) vai para uma aplicação rendendo {rentabilidade_invest*100}%.<br>
            2. <b>Manter o Imóvel (Lado A):</b> Você ganha de duas formas: Valorização do Imóvel ({valorizacao_imovel*100}% a.a.) + Aluguel Líquido mensal reinvestido.<br>
            3. <b>Conclusão:</b> Geralmente, manter imóvel ganha se a valorização + aluguel superarem a taxa Selic/CDI líquida.
            </div>
            """
        st.markdown(help_text, unsafe_allow_html=True)
