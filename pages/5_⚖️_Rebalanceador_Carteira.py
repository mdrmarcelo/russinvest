import streamlit as st
import sys
import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
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
st.set_page_config(layout="wide", page_title="Russinvest - Rebalanceador", page_icon="⚖️")

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
</style>
""", unsafe_allow_html=True)

def formatar_br(valor): return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- FUNÇÃO GERADORA DE RELATÓRIO PROFISSIONAL (REBALANCEAMENTO) ---
def gerar_relatorio_rebalanceamento(cliente, total_atual, aporte, total_futuro, df_final):
    data_hoje = datetime.now().strftime("%d/%m/%Y")
    
    # Prepara a tabela para HTML, destacando ações de compra
    rows_html = ""
    for _, row in df_final.iterrows():
        style_acao = "color: #16a34a; font-weight: bold;" if "Comprar" in row['Ação Sugerida'] else "color: #64748b;"
        style_bg = "background-color: #f0fdf4;" if "Comprar" in row['Ação Sugerida'] else ""
        
        rows_html += f"""
        <tr style="{style_bg}">
            <td style="text-align: left;">{row['Ativo']}</td>
            <td style="text-align: right;">{formatar_br(row['Saldo Atual'])}</td>
            <td style="text-align: center;">{row['Meta %']:.1f}%</td>
            <td style="text-align: right; {style_acao}">{row['Ação Sugerida']}</td>
        </tr>
        """

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
            
            .summary-box {{ background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin-bottom: 30px; display: flex; justify-content: space-between; }}
            .summary-item {{ text-align: center; }}
            .summary-lbl {{ font-size: 11px; text-transform: uppercase; color: #64748b; font-weight: bold; margin-bottom: 5px; }}
            .summary-val {{ font-size: 18px; font-weight: 800; color: #0f172a; }}
            .highlight {{ color: #16a34a; }}

            table {{ width: 100%; border-collapse: collapse; font-size: 13px; margin-top: 10px; }}
            th {{ background-color: #f1f5f9; padding: 12px; text-align: left; color: #475569; border-bottom: 2px solid #e2e8f0; }}
            th.center {{ text-align: center; }}
            th.right {{ text-align: right; }}
            td {{ padding: 12px; border-bottom: 1px solid #e2e8f0; color: #334155; }}
            
            .footer {{ margin-top: 50px; text-align: center; font-size: 11px; color: #94a3b8; border-top: 1px solid #e2e8f0; padding-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="brand">Russinvest 🔷</div>
            <div class="sub">Asset Allocation</div>
            <div style="margin-top: 10px; font-size: 14px;">Cliente: <b>{cliente}</b> | Data: {data_hoje}</div>
        </div>

        <div class="title">Plano de Rebalanceamento</div>

        <div class="summary-box">
            <div class="summary-item">
                <div class="summary-lbl">Patrimônio Atual</div>
                <div class="summary-val">{formatar_br(total_atual)}</div>
            </div>
            <div class="summary-item">
                <div class="summary-lbl">Novo Aporte</div>
                <div class="summary-val highlight">+{formatar_br(aporte)}</div>
            </div>
            <div class="summary-item">
                <div class="summary-lbl">Patrimônio Projetado</div>
                <div class="summary-val">{formatar_br(total_futuro)}</div>
            </div>
        </div>

        <h3 style="font-size: 16px; color: #1e293b; margin-bottom: 10px;">Ordem de Alocação</h3>
        <p style="font-size: 13px; color: #666; margin-bottom: 20px;">Sugestão baseada na estratégia de comprar ativos abaixo da meta (Smart Rebalancing).</p>
        
        <table>
            <thead>
                <tr>
                    <th>Classe de Ativo</th>
                    <th class="right">Saldo Atual</th>
                    <th class="center">Meta Alvo</th>
                    <th class="right">Ação Recomendada</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
        
        <div class="footer">
            Relatório gerado pelo Sistema Russinvest. 
            Esta sugestão é matemática e visa aproximar a carteira das metas percentuais definidas.
        </div>
    </body>
    </html>
    """
    return html

# --- SIDEBAR ---
with st.sidebar:

    nome_cliente = st.text_input("Nome do Cliente", "Visitante")
    st.markdown("### 💰 Aporte Novo")
    aporte = st.number_input("Valor disponível para investir hoje", 0.0, value=5000.0, step=500.0)

# --- HEADER ---
st.markdown('<div class="russinvest-header">Rebalanceador Inteligente</div>', unsafe_allow_html=True)
st.markdown('<div class="russinvest-sub">Ajuste de carteira baseado em aporte (Smart Rebalancing)</div>', unsafe_allow_html=True)

# --- DADOS ---
st.info("👇 Edite a tabela abaixo com sua carteira atual e suas metas.")
df_inicial = pd.DataFrame([
    {"Ativo": "Renda Fixa Pós (CDI)", "Saldo Atual": 50000.0, "Meta %": 30.0},
    {"Ativo": "Multimercados", "Saldo Atual": 20000.0, "Meta %": 10.0},
    {"Ativo": "FIIs", "Saldo Atual": 30000.0, "Meta %": 25.0},
    {"Ativo": "Ações Brasil", "Saldo Atual": 25000.0, "Meta %": 15.0},
    {"Ativo": "Exterior (Dólar)", "Saldo Atual": 25000.0, "Meta %": 20.0},
])

df_input = st.data_editor(df_inicial, num_rows="dynamic", column_config={"Saldo Atual": st.column_config.NumberColumn(format="R$ %.2f"), "Meta %": st.column_config.NumberColumn(format="%.1f%%", min_value=0, max_value=100)}, use_container_width=True)

# --- CÁLCULO ---
total_atual = df_input["Saldo Atual"].sum()
total_meta_pct = df_input["Meta %"].sum()
patrimonio_final_projetado = total_atual + aporte

if abs(total_meta_pct - 100.0) > 0.1:
    st.error(f"⚠️ Atenção: A soma das metas está em {total_meta_pct:.1f}%. Ajuste para fechar em 100%.")
else:
    df_calc = df_input.copy()
    df_calc["Saldo Ideal"] = (df_calc["Meta %"] / 100) * patrimonio_final_projetado
    df_calc["Diferença"] = df_calc["Saldo Ideal"] - df_calc["Saldo Atual"]
    
    # Lógica de distribuição do aporte
    compras_necessarias = df_calc[df_calc["Diferença"] > 0].copy()
    total_gap_positivo = compras_necessarias["Diferença"].sum()
    
    def calcular_sugestao(row):
        if row["Diferença"] <= 0: return "Manter"
        if total_gap_positivo == 0: return "Manter"
        
        # Proporção do aporte
        valor_comprar = (row["Diferença"] / total_gap_positivo) * aporte
        return f"Comprar {formatar_br(valor_comprar)}"
    
    df_calc["Ação Sugerida"] = df_calc.apply(calcular_sugestao, axis=1)

    # --- VISUALIZAÇÃO ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Patrimônio Atual", formatar_br(total_atual))
    col2.metric("Novo Aporte", formatar_br(aporte))
    col3.metric("Patrimônio Futuro", formatar_br(patrimonio_final_projetado))
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("#### 📊 Como você está hoje")
        fig_atual = px.pie(df_input, values='Saldo Atual', names='Ativo', hole=0.4)
        fig_atual.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_atual, use_container_width=True)
    with col_g2:
        st.markdown("#### 🎯 Onde queremos chegar")
        fig_ideal = px.pie(df_input, values='Meta %', names='Ativo', hole=0.4)
        fig_ideal.update_traces(marker=dict(line=dict(color='#000000', width=2)))
        fig_ideal.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_ideal, use_container_width=True)

    st.markdown("### 🛒 Plano de Ação")
    compras = df_calc[df_calc["Ação Sugerida"].str.contains("Comprar")].sort_values(by="Diferença", ascending=False)
    
    if compras.empty:
        st.success("Sua carteira já está balanceada ou acima da meta.")
    else:
        for index, row in compras.iterrows():
            st.markdown(f"""
            <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 15px; border-radius: 8px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;">
                <div style="font-weight: 600; font-size: 1.1em;">{row['Ativo']}</div>
                <div style="color: #16a34a; font-weight: bold; font-size: 1.2em;">👉 {row['Ação Sugerida']}</div>
            </div>
            """, unsafe_allow_html=True)

    # --- SIDEBAR EXPORT ---
    with st.sidebar:
        st.markdown("---")
        st.markdown("**Exportar**")
        
        html_relatorio = gerar_relatorio_rebalanceamento(nome_cliente, total_atual, aporte, patrimonio_final_projetado, df_calc)
        
        st.download_button("📄 Baixar Plano Oficial", html_relatorio, f"Rebalanceamento_{nome_cliente}.html", "text/html")
        
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("❓ Metodologia"):
            st.info("Método Portfel: Aportar onde falta para atingir a meta, evitando giro de carteira e impostos.")
