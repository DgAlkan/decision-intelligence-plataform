from pathlib import Path
import pandas as pd
import duckdb
from streamlit.testing.v1 import AppTest
from engine import generate,metrics

def test_sql(tmp_path,monkeypatch):
    from pathlib import Path
    sql=Path("sql/analysis.sql").read_text()
    monkeypatch.chdir(tmp_path)
    Path("data").mkdir()
    x=generate(1000)
    x.to_csv("data/synthetic.csv",index=False)
    with duckdb.connect() as con:
        rows=con.execute(sql).fetchall()
    for month,unit,n,missed,rate in rows:
        g=x[(x.date.dt.to_period("M")==pd.Timestamp(month).to_period("M")) & (x.unit==unit)]
        m=metrics(g)
        assert n==m["appointments"] and missed==m["no_show"]
        assert rate==m["rate"]

def test_cancelled_only():
    assert metrics(pd.DataFrame({"id":[1],"status":["Cancelled"]}))["rate"] is None

def test_app():
    a=AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py"),default_timeout=60).run()
    assert not a.exception
    assert len(a.metric)>=5
