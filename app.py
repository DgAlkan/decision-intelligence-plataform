import streamlit as st
import pandas as pd
from engine import generate, metrics, scenario
st.set_page_config(page_title="Decision Intelligence",layout="wide")
st.caption("ANALYTICS INTELLIGENCE LAB / PORTFOLIO / V2.0")
st.title("Decision Intelligence | Operations")
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
st.caption("Rodrigo Alcantara | Analytics Intelligence Lab | Synthetic demonstration")
