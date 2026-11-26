import streamlit as st
import pandas as pd
from engine import generate, metrics, scenario
st.set_page_config(page_title="Decision Intelligence",layout="wide")
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
<section class="lab-hero"><div class="lab-kicker">ANALYTICS INTELLIGENCE LAB / 02 / V2.2</div><h1>Decision Intelligence Platform</h1><p>Operational performance · Scenario planning</p></section>""", unsafe_allow_html=True)
st.sidebar.header("Workspace")
st.sidebar.caption("Configure your synthetic demonstration.")
st.sidebar.markdown("### Product suite")
st.sidebar.markdown("[01 · Data Quality](https://dgalkan-data-quality.streamlit.app)  \n[02 · Decision Intelligence](https://dgalkan-decision-intelligence.streamlit.app)  \n[03 · Customer Journey](https://dgalkan-customer-journey.streamlit.app)")
st.sidebar.divider()
st.sidebar.markdown("### Analysis controls")
with st.expander("About this product · methodology"):
    st.markdown("Explore operational performance and intervention scenarios.")
    st.markdown("No-show rate excludes cancelled appointments. Scenario estimates depend on conversion and value assumptions; they are not causal forecasts.")
    st.markdown("[Technical portfolio](https://github.com/DgAlkan) · Synthetic data only.")
st.caption("Synthetic appointments · descriptive analysis, not causal inference")
volume=st.sidebar.selectbox("Synthetic appointments",[12000,50000,100000])
@st.cache_data
def demo(n):
    return generate(n)
df=demo(volume)
units=st.sidebar.multiselect("Unit",sorted(df.unit.unique()),default=sorted(df.unit.unique()))
services=st.sidebar.multiselect("Service",sorted(df.service.unique()),default=sorted(df.service.unique()))
dates=st.sidebar.date_input("Period",(df.date.min().date(),df.date.max().date()))
if len(dates)!=2: st.stop()
df=df[df.unit.isin(units)&df.service.isin(services)&df.date.between(pd.Timestamp(dates[0]),pd.Timestamp(dates[1]))]
m=metrics(df)
for c,(k,v) in zip(st.columns(4),[(k,m[k]) for k in ["appointments","attended","cancelled","no_show"]]): c.metric(k.replace("_"," ").title(),v)
if m["rate"] is None: st.info("No eligible appointments"); st.stop()
st.metric("No-show rate",f'{m["rate"]:.1%}')
monthly=df.assign(month=df.date.dt.to_period("M").astype(str)).groupby("month")[ "status"].apply(lambda s: s.eq("No show").sum()/s.ne("Cancelled").sum() if s.ne("Cancelled").sum() else None)
st.subheader("Monthly no-show trend")
st.line_chart(monthly*100, y_label="No-show (%)", color="#2563EB")
segments=df.groupby("unit").status.apply(lambda s: s.eq("No show").sum()/s.ne("Cancelled").sum() if s.ne("Cancelled").sum() else None)
st.subheader("Unit comparison")
valid_segments = segments.dropna()
if not valid_segments.empty:
    st.info(f"Highest observed unit no-show rate: {valid_segments.idxmax()} ({valid_segments.max():.1%}). Investigate volume and case mix before acting.")
st.bar_chart(segments*100, y_label="No-show (%)", color="#2563EB")
st.subheader("Appointment status mix")
st.bar_chart(df.status.value_counts(), color="#0F766E")
st.divider()
st.subheader("Scenario simulator")
target=st.number_input("Target rate (%)",0.,float(m["rate"]*100),float(m["rate"]*50))
value=st.number_input("Value per recovered visit (BRL)",0.,value=150.)
conversion=st.slider("Conversion assumption",0.,1.,.8)
s=scenario(m["eligible"],m["rate"],target/100,value,conversion)
st.metric("Potential recovered visits",f'{s["recovered"]:,.1f}')
st.metric("Potential gross value (BRL)",f'{s["potential_value"]:,.2f}')
st.caption("Not guaranteed revenue or savings. Investigate high-rate segments before intervention.")
st.download_button("Export filtered data",df.to_csv(index=False),"appointments.csv")


st.divider()
st.caption("Rodrigo Alcantara | Analytics Intelligence Lab | Independent synthetic demonstration")
st.markdown("[Data Quality](https://dgalkan-data-quality.streamlit.app) · [Decision Intelligence](https://dgalkan-decision-intelligence.streamlit.app) · [Customer Journey](https://dgalkan-customer-journey.streamlit.app)")
