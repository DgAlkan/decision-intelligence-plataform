from pathlib import Path
from engine import generate
Path('data').mkdir(exist_ok=True)
generate().to_csv('data/synthetic.csv',index=False)
