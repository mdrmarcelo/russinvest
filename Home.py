import streamlit as st
from navegacao import sidebar_menu # IMPORTA O MENU

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Russinvest - Home",
    page_icon="🔷",
    layout="wide"
)

# CHAMA O MENU LATERAL
sidebar_menu()

# --- CSS PERSONALIZADO (IDENTIDADE VISUAL RUSSINVEST 10.0) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* HEADER PRINCIPAL */
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -1.5px;
        color: #0f172a;
        margin-bottom: 0px;
        line-height: 1.1;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #64748b;
        margin-bottom: 40px;
        font-weight: 500;
    }
    
    /* SIDEBAR BRANDING */
    .sidebar-brand {
        background-color: #f8fafc;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 25px;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .brand-flex { display: flex; justify-content: center; align-items: center; gap: 10px; margin-bottom: 5px; }
    .brand-title { color: #0066ff; font-size: 1.6rem; font-weight: 800; letter-spacing: -0.5px; margin: 0; }
    .brand-subtitle { color: #94a3b8; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; font-weight: 600; margin-top: 2px; }
    
    /* SECTION HEADERS */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-top: 40px;
        margin-bottom: 20px;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 10px;
    }
    
    /* AJUSTES DARK MODE */
    @media (prefers-color-scheme: dark) {
        .hero-title { color: #e2e8f0; }
        .hero-subtitle { color: #94a3b8; }
        .sidebar-brand { background-color: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); }
        .brand-title { color: #60a5fa !important; }
        .section-header { color: #f1f5f9; border-bottom-color: #334155; }
    }
    
    /* CONTAINER DOS CARDS */
    .module-card {
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        background-color: #ffffff;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        height: 100%;
        transition: transform 0.2s;
    }
    .module-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
    }
    .card-icon { font-size: 40px; margin-bottom: 15px; }
    .card-title { font-size: 1.25rem; font-weight: 700; color: #1e293b; margin-bottom: 10px; }
    .card-desc { font-size: 0.95rem; color: #64748b; line-height: 1.5; margin-bottom: 20px; }
    
    /* Dark mode para os cards */
    @media (prefers-color-scheme: dark) {
        .module-card { background-color: #1e293b; border-color: #334155; }
        .card-title { color: #f8fafc; }
        .card-desc { color: #cbd5e1; }
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    
    st.markdown("### Sobre a Plataforma")
    st.info(
        "Bem-vindo à suíte completa de ferramentas da Russinvest. "
        "Navegue pelos módulos para simular decisões de alto impacto financeiro."
    )
    
    st.markdown("### 🎯 Como Usar")
    st.write("""
    1. **Comece pelo Raio-X** para mapear sua situação atual
    2. **Explore as ferramentas** de acordo com sua necessidade
    3. **Exporte relatórios** profissionais para seus registros
    """)
    
    st.markdown("---")
    st.caption("© 2026 Russinvest Consultoria Financeira")

# --- CONTEÚDO PRINCIPAL ---
st.markdown('<div class="hero-title">Bem-vindo ao Ecossistema Russinvest</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Inteligência financeira para decisões de alto impacto.</div>', unsafe_allow_html=True)

st.divider()

# ========================================
# SEÇÃO 1: DIAGNÓSTICO INICIAL
# ========================================
st.markdown('<div class="section-header">🔍 Diagnóstico Inicial</div>', unsafe_allow_html=True)
st.markdown("*Comece por aqui para entender sua situação financeira atual*")
st.write("")

col_diag = st.columns(1)[0]

with col_diag:
    st.markdown("""
    <div class="module-card">
        <div class="card-icon">🌊</div>
        <div class="card-title">Raio-X Financeiro</div>
        <div class="card-desc">
            Mapeamento visual de Fluxo de Caixa com Diagrama de Sankey interativo. 
            Veja para onde vai cada centavo da sua renda mensal. Inclui assistente 
            inteligente para detalhar gastos por categoria (Moradia, Carro, Mercado).
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.page_link("pages/7_🌊_Fluxo_Financeiro.py", label="Iniciar Diagnóstico", icon="🌊", use_container_width=True)

st.write("")
st.write("")

# ========================================
# SEÇÃO 2: FERRAMENTAS DE PLANEJAMENTO
# ========================================
st.markdown('<div class="section-header">🛠️ Ferramentas de Planejamento</div>', unsafe_allow_html=True)
st.markdown("*Simuladores e calculadoras para decisões estratégicas*")
st.write("")

# Linha 1: Imóveis, Aposentadoria, Fiscal
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="module-card">
        <div class="card-icon">🏠</div>
        <div class="card-title">Real Estate Pro</div>
        <div class="card-desc">
            Simulador completo para decisões imobiliárias. Compare Financiamento vs. Aluguel, 
            analise Consórcios, viabilidade de compra na planta e estratégias de venda antecipada.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.page_link("pages/1_🏠_Simulador_Imoveis.py", label="Acessar Simulador", icon="🏠", use_container_width=True)

with col2:
    st.markdown("""
    <div class="module-card">
        <div class="card-icon">📈</div>
        <div class="card-title">Independência Financeira</div>
        <div class="card-desc">
            Planejamento de Aposentadoria com Juros Reais. Projete suas fases de acumulação 
            e decumulação, defina metas de aporte e visualize quando atingirá sua liberdade.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.page_link("pages/2_📈_Independencia_Financeira.py", label="Planejar Futuro", icon="📈", use_container_width=True)

with col3:
    st.markdown("""
    <div class="module-card">
        <div class="card-icon">🦁</div>
        <div class="card-title">Tax Optimizer</div>
        <div class="card-desc">
            Eficiência tributária para Pessoa Física. Compare declaração Simplificada vs. Completa 
            e calcule o aporte exato de PGBL para maximizar sua restituição de IR.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.page_link("pages/3_🦁_Otimizador_Fiscal.py", label="Otimizar Impostos", icon="🦁", use_container_width=True)

st.write("")

# Linha 2: Renda Fixa, Rebalanceamento, Proteção
col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class="module-card">
        <div class="card-icon">📊</div>
        <div class="card-title">Renda Fixa Pro</div>
        <div class="card-desc">
            Comparador CDB vs LCI/LCA com cálculo de Taxa Equivalente (Gross-up). 
            Descubra qual investimento rende mais no seu bolso após impostos.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.page_link("pages/4_📊_Comparador_Renda_Fixa.py", label="Comparar Taxas", icon="📊", use_container_width=True)

with col5:
    st.markdown("""
    <div class="module-card">
        <div class="card-icon">⚖️</div>
        <div class="card-title">Asset Allocation</div>
        <div class="card-desc">
            Rebalanceador Inteligente de Carteira. Distribua seus aportes para manter 
            a alocação ideal sem giro desnecessário de patrimônio.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.page_link("pages/5_⚖️_Rebalanceador_Carteira.py", label="Rebalancear", icon="⚖️", use_container_width=True)

with col6:
    st.markdown("""
    <div class="module-card">
        <div class="card-icon">🛡️</div>
        <div class="card-title">Gestão de Riscos</div>
        <div class="card-desc">
            Calculadora de Seguro de Vida. Mensure o capital necessário para proteger 
            sua família considerando renda, dívidas e custos sucessórios.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.page_link("pages/6_🛡️_Calculadora_Protecao.py", label="Calcular Proteção", icon="🛡️", use_container_width=True)

st.divider()

# --- RODAPÉ ---
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 0.9rem; margin-top: 40px;">
    <b>Russinvest</b> | Consultoria Financeira Inteligente<br>
    Todas as simulações são estimativas. Consulte um profissional certificado para decisões finais.
</div>
""", unsafe_allow_html=True)
