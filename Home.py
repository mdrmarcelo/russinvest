import streamlit as st

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Russinvest - Home",
    page_icon="🔷",
    layout="wide"
)

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
    
    /* AJUSTES DARK MODE */
    @media (prefers-color-scheme: dark) {
        .hero-title { color: #e2e8f0; }
        .hero-subtitle { color: #94a3b8; }
        .sidebar-brand { background-color: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); }
        .brand-title { color: #60a5fa !important; }
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
    st.markdown("""
        <div class="sidebar-brand">
            <div class="brand-flex">
                <span class="brand-icon">🔷</span>
                <span class="brand-title">Russinvest</span>
            </div>
            <div class="brand-subtitle">Ecossistema Financeiro</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Sobre")
    st.info(
        "Bem-vindo à suíte de ferramentas da Russinvest. "
        "Selecione um módulo ao lado ou nos cartões para iniciar sua simulação."
    )
    st.markdown("---")
    st.caption("© 2025 Russinvest Consultoria")

# --- CONTEÚDO PRINCIPAL ---
st.markdown('<div class="hero-title">Bem-vindo ao Ecossistema Russinvest</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Inteligência financeira para decisões de alto impacto.</div>', unsafe_allow_html=True)

st.divider()

# GRID DE NAVEGAÇÃO
col1, col2, col3 = st.columns(3)

# Módulo 1: Imóveis
with col1:
    st.markdown("""
    <div class="module-card">
        <div class="card-icon">🏠</div>
        <div class="card-title">Real Estate Pro</div>
        <div class="card-desc">
            Simulador completo para decisões imobiliárias. Compare Financiamento vs. Aluguel, 
            analise Consórcios, viabilidade de compra na planta e estratégias de venda.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("") # Espaço
    st.page_link("pages/1_🏠_Simulador_Imoveis.py", label="Acessar Simulador", icon="🏠", use_container_width=True)

# Módulo 2: Aposentadoria
with col2:
    st.markdown("""
    <div class="module-card">
        <div class="card-icon">📈</div>
        <div class="card-title">Independência Financeira</div>
        <div class="card-desc">
            Planejamento de longo prazo. Projete sua aposentadoria com base em Juros Reais, 
            defina metas de aporte e visualize as fases de acumulação e decumulação.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.page_link("pages/2_📈_Independencia_Financeira.py", label="Planejar Futuro", icon="📈", use_container_width=True)

# Módulo 3: Fiscal
with col3:
    st.markdown("""
    <div class="module-card">
        <div class="card-icon">🦁</div>
        <div class="card-title">Tax Optimizer</div>
        <div class="card-desc">
            Eficiência tributária para PF. Compare declaração Simplificada vs. Completa e 
            calcule o aporte exato de PGBL para maximizar sua restituição de imposto.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.page_link("pages/3_🦁_Otimizador_Fiscal.py", label="Otimizar Impostos", icon="🦁", use_container_width=True)

st.divider()
