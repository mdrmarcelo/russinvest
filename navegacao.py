import streamlit as st

def sidebar_menu():
    with st.sidebar:
        # LOGO E BRANDING CENTRALIZADO
        st.markdown("""
            <div style="text-align: center; margin-bottom: 30px; padding: 20px; background-color: #f8fafc; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                <div style="font-size: 32px; margin-bottom: 5px;">🔷</div>
                <div style="color: #0f172a; font-weight: 800; font-size: 22px; letter-spacing: -0.5px;">Russinvest</div>
                <div style="color: #64748b; font-size: 11px; text-transform: uppercase; letter-spacing: 2px; font-weight: 600;">Financial Suite</div>
            </div>
        """, unsafe_allow_html=True)
        
        # MENU PERSONALIZADO
        # Usamos st.page_link para navegação rápida e nativa
        
        st.markdown("<div style='color: #94a3b8; font-size: 11px; font-weight: 700; margin-bottom: 10px; padding-left: 10px;'>HOME</div>", unsafe_allow_html=True)
        st.page_link("Home.py", label="Início", icon="🏠")
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True) # Espaçamento
        
        st.markdown("<div style='color: #94a3b8; font-size: 11px; font-weight: 700; margin-bottom: 10px; padding-left: 10px;'>DIAGNÓSTICO</div>", unsafe_allow_html=True)
        st.page_link("pages/7_🌊_Fluxo_Financeiro.py", label="Raio-X Financeiro", icon="🌊")
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        st.markdown("<div style='color: #94a3b8; font-size: 11px; font-weight: 700; margin-bottom: 10px; padding-left: 10px;'>ESTRATÉGIA</div>", unsafe_allow_html=True)
        st.page_link("pages/1_🏠_Simulador_Imoveis.py", label="Imóveis Pro", icon="🏠")
        st.page_link("pages/2_📈_Independencia_Financeira.py", label="Aposentadoria", icon="📈")
        st.page_link("pages/3_🦁_Otimizador_Fiscal.py", label="Fiscal (Tax)", icon="🦁")
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        st.markdown("<div style='color: #94a3b8; font-size: 11px; font-weight: 700; margin-bottom: 10px; padding-left: 10px;'>TÁTICO & RISCO</div>", unsafe_allow_html=True)
        st.page_link("pages/4_📊_Comparador_Renda_Fixa.py", label="Renda Fixa", icon="📊")
        st.page_link("pages/5_⚖️_Rebalanceador_Carteira.py", label="Asset Allocation", icon="⚖️")
        st.page_link("pages/6_🛡️_Calculadora_Protecao.py", label="Seguros (Gap)", icon="🛡️")

        st.divider()
        st.caption("v1.0.0 • Russinvest")
