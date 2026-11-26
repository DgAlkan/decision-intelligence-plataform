import streamlit as st
import pandas as pd
from engine import generate, metrics, scenario
st.set_page_config(page_title="Decision Intelligence",layout="wide")
lang = st.sidebar.radio("Idioma / Language", ["Português", "English"], horizontal=True, key="lab_language")
def tr(en, pt):
    return pt if lang == "Português" else en
st.markdown("""<style>
.stApp {background:#f1f5f9;}
[data-testid="stSidebar"] {background:#142238;}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] h2 {color:#e2e8f0;}
[data-testid="stMetric"] {background:white;border:1px solid #dbe4ef;border-radius:14px;padding:16px;box-shadow:0 3px 12px #10223808;}
[data-testid="stMetricValue"] {font-weight:700;color:#102238;}
[data-testid="stMainBlockContainer"] {padding-top:2rem;max-width:1440px;}
.stTabs [role="tablist"] {gap:12px;}
.stTabs [role="tab"] {font-weight:600;}
.lab-hero {background:linear-gradient(115deg,#0b1526,#193a60);color:white;padding:28px 30px;border-radius:16px;margin-bottom:18px;}
.lab-hero h1 {color:white;font-size:clamp(1.65rem,3vw,2.5rem);margin:8px 0;padding:0;}
.lab-hero p {color:#cbd5e1;margin:0;}
.lab-kicker {color:#7dd3fc;font-size:12px;font-weight:700;letter-spacing:1.8px;}
</style>
<section class="lab-hero"><div class="lab-kicker">ANALYTICS INTELLIGENCE LAB</div><h1>Decision Intelligence Platform</h1><p>__LAB_SUBTITLE__</p></section>""".replace("__LAB_SUBTITLE__", tr("Operational performance · Scenario planning", "Desempenho operacional · Simulação de cenários")), unsafe_allow_html=True)
st.sidebar.header(tr("Workspace", "Área de trabalho"))
st.sidebar.caption(tr("Configure your synthetic demonstration.", "Configure sua demonstração com dados sintéticos."))
st.sidebar.markdown(tr("### Product suite", "### Produtos"))
st.sidebar.markdown("[01 · Data Quality](https://dgalkan-data-quality.streamlit.app)  \n[02 · Decision Intelligence](https://dgalkan-decision-intelligence.streamlit.app)  \n[03 · Customer Journey](https://dgalkan-customer-journey.streamlit.app)")
st.sidebar.divider()
st.sidebar.markdown(tr("### Analysis controls", "### Filtros e parâmetros"))
with st.expander(tr("About this product · methodology", "Sobre o produto · metodologia")):
    st.markdown(tr("Explore operational performance and intervention scenarios.", "Explore o desempenho operacional e cenários de intervenção."))
    st.markdown(tr("No-show rate excludes cancelled appointments. Scenario estimates depend on conversion and value assumptions; they are not causal forecasts.", "A taxa de No-show exclui cancelamentos. As estimativas dependem das premissas de conversão e valor; não são previsões causais."))
    st.markdown(tr("[Technical portfolio](https://github.com/DgAlkan) · Synthetic data only.", "[Portfólio técnico](https://github.com/DgAlkan) · Apenas dados sintéticos."))
st.caption(tr("Synthetic appointments · descriptive analysis, not causal inference", "Agendamentos sintéticos · análise descritiva, não causal"))
volume=st.sidebar.selectbox(tr("Synthetic appointments", "Agendamentos sintéticos"),[12000,50000,100000])
@st.cache_data
def demo(n):
    return generate(n)
df=demo(volume)
units=st.sidebar.multiselect(tr("Unit", "Unidade"),sorted(df.unit.unique()),default=sorted(df.unit.unique()))
services=st.sidebar.multiselect(tr("Service", "Serviço"),sorted(df.service.unique()),default=sorted(df.service.unique()))
dates=st.sidebar.date_input(tr("Period", "Período"),(df.date.min().date(),df.date.max().date()))
if len(dates)!=2: st.stop()
df=df[df.unit.isin(units)&df.service.isin(services)&df.date.between(pd.Timestamp(dates[0]),pd.Timestamp(dates[1]))]
m=metrics(df)
for c,(k,v) in zip(st.columns(4),[(k,m[k]) for k in ["appointments","attended","cancelled","no_show"]]): c.metric(tr(k.replace("_"," ").title(), {"appointments":"Agendamentos","attended":"Atendimentos realizados","cancelled":"Cancelamentos","no_show":"Não comparecimentos"}[k]),v)
if m["rate"] is None: st.info(tr("No eligible appointments", "Nenhum agendamento elegível")); st.stop()
st.metric(tr("No-show rate", "Taxa de No-show"),f'{m["rate"]:.1%}')
monthly=df.assign(month=df.date.dt.to_period("M").astype(str)).groupby("month")[ "status"].apply(lambda s: s.eq("No show").sum()/s.ne("Cancelled").sum() if s.ne("Cancelled").sum() else None)
st.subheader(tr("Monthly no-show trend", "Evolução mensal da taxa de No-show"))
st.line_chart(monthly*100, y_label="No-show (%)", color="#2563EB")
segments=df.groupby("unit").status.apply(lambda s: s.eq("No show").sum()/s.ne("Cancelled").sum() if s.ne("Cancelled").sum() else None)
st.subheader(tr("Unit comparison", "Comparação entre unidades"))
valid_segments = segments.dropna()
if not valid_segments.empty:
    st.info(tr(f"Highest observed unit no-show rate: {valid_segments.idxmax()} ({valid_segments.max():.1%}). Investigate volume and case mix before acting.", f"Maior taxa de No-show observada: {valid_segments.idxmax()} ({valid_segments.max():.1%}). Investigue volume e perfil dos atendimentos antes de agir."))
st.bar_chart(segments*100, y_label="No-show (%)", color="#2563EB")
st.subheader(tr("Appointment status mix", "Distribuição dos agendamentos por status"))
st.bar_chart(df.status.value_counts().rename(index=lambda x: tr(x, {"Attended":"Atendido","Cancelled":"Cancelado","No show":"Não compareceu"}[x])), color="#0F766E")
st.divider()
st.subheader(tr("Scenario simulator", "Simulador de cenários"))
target=st.number_input(tr("Target rate (%)", "Taxa desejada (%)"),0.,float(m["rate"]*100),float(m["rate"]*50))
value=st.number_input(tr("Value per recovered visit (BRL)", "Valor por atendimento recuperado (R$)"),0.,value=150.)
conversion=st.slider(tr("Conversion assumption", "Premissa de conversão"),0.,1.,.8)
s=scenario(m["eligible"],m["rate"],target/100,value,conversion)
st.metric(tr("Potential recovered visits", "Atendimentos potencialmente recuperados"),f'{s["recovered"]:,.1f}')
st.metric(tr("Potential gross value (BRL)", "Valor bruto potencial (R$)"),f'{s["potential_value"]:,.2f}')
st.caption(tr("Not guaranteed revenue or savings. Investigate high-rate segments before intervention.", "Não representa receita ou economia garantida. Investigue os segmentos antes de intervir."))
st.download_button(tr("Export filtered data", "Exportar dados filtrados"),df.to_csv(index=False),"appointments.csv")


st.divider()
st.caption(tr("Rodrigo Alcantara | Analytics Intelligence Lab | Independent synthetic demonstration", "Rodrigo Alcantara | Analytics Intelligence Lab | Demonstração independente com dados sintéticos"))
st.markdown("[Data Quality](https://dgalkan-data-quality.streamlit.app) · [Decision Intelligence](https://dgalkan-decision-intelligence.streamlit.app) · [Customer Journey](https://dgalkan-customer-journey.streamlit.app)")
