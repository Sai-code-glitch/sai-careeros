def clamp(x):return max(0,min(100,int(round(x))))
def opportunity_score(match,scam=0,ghost=0,salary=50,network=0,company=50):return clamp(match*.50+salary*.12+network*.10+company*.18+(100-scam)*.06+(100-ghost)*.04)
def warmth(rel):return {'first_degree':95,'former_colleague':85,'recruiter_prior':80,'alumni':75,'mutual':70,'cold':25}.get((rel or 'cold').lower(),25)
