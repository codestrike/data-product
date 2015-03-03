import pandas as pd


def rank(frame,cols,pct=True):
	Rank_frame = pd.DataFrame()
	print cols
	for col in cols:

		Rank_frame[col]=frame[col].rank(pct=pct)
		
	return Rank_frame


