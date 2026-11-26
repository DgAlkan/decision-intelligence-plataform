import pandas as pd
import numpy as np

def generate(n=12000, seed=42):
    rng=np.random.default_rng(seed)
    unit=rng.choice(["North","South","Central"],n)
    p=np.where(unit=="North",.25,.12)
    u=rng.random(n)
    return pd.DataFrame({"id":range(n),"date":pd.Timestamp("2025-01-01")+pd.to_timedelta(rng.integers(0,365,n),unit="D"),"unit":unit,"service":rng.choice(["Consultation","Review"],n),"status":np.where(u<.15,"Cancelled",np.where(u<.15+p,"No show","Attended"))})

def metrics(df):
    if df.id.duplicated().any() or df.id.isna().any(): raise ValueError("Invalid appointment key")
    if not df.status.isin(["Cancelled","No show","Attended"]).all(): raise ValueError("Invalid status")
    eligible=df.status.isin(["No show","Attended"]).sum()
    missed=df.status.eq("No show").sum()
    return {"appointments":len(df),"eligible":int(eligible),"attended":int(df.status.eq("Attended").sum()),"cancelled":int(df.status.eq("Cancelled").sum()),"no_show":int(missed),"rate":missed/eligible if eligible else None}

def scenario(eligible, rate, target, value, conversion=1):
    if not (eligible>=0 and 0<=target<=rate<=1 and value>=0 and 0<=conversion<=1): raise ValueError("Invalid scenario")
    recovered=eligible*(rate-target)*conversion
    return {"recovered":recovered,"potential_value":recovered*value}
