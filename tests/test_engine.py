import pandas as pd
import pytest
from engine import generate,metrics,scenario
def test_metrics():
    x=pd.DataFrame({"id":[1,2,3],"status":["Attended","No show","Cancelled"]})
    assert metrics(x)["rate"]==.5
def test_empty():
    assert metrics(generate(0))["rate"] is None
def test_scenario():
    assert scenario(100,.2,.1,50,.5)["potential_value"]==250
def test_invalid():
    with pytest.raises(ValueError): scenario(100,.1,.2,50)
def test_seed():
    assert generate(20).equals(generate(20))
