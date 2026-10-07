import json
from app import db
from app.llm import company_agent,skills_agent,portfolio_agent,interview_agent,offer_agent
from app.resume import read_master_resume
def company(job):
    c=db.one('SELECT * FROM company_intel WHERE company=?',(job['company'],))
    if c:return c
    x=company_agent(job);db.execute('INSERT OR REPLACE INTO company_intel(company,summary,stability_score,hiring_score,visa_notes,interview_notes,tech_stack,sentiment_notes,source_notes) VALUES(?,?,?,?,?,?,?,?,?)',(job['company'],x.get('summary',''),x.get('stability_score',50),x.get('hiring_score',50),x.get('visa_notes',''),x.get('interview_notes',''),x.get('tech_stack',''),x.get('sentiment_notes',''),x.get('source_notes','')));return db.one('SELECT * FROM company_intel WHERE company=?',(job['company'],))
def refresh_skills():
    jobs=db.query("SELECT title,company,description,match_score FROM jobs WHERE status NOT LIKE 'REJECTED%' ORDER BY created_at DESC LIMIT 100")
    if not jobs:return {'signals':[]}
    x=skills_agent(jobs,read_master_resume())
    for s in x.get('signals',[]):db.execute('INSERT INTO skill_signals(skill,mentions,candidate_has,roi_score,updated_at) VALUES(?,?,?,?,CURRENT_TIMESTAMP) ON CONFLICT(skill) DO UPDATE SET mentions=excluded.mentions,candidate_has=excluded.candidate_has,roi_score=excluded.roi_score,updated_at=CURRENT_TIMESTAMP',(s.get('skill',''),s.get('mentions',0),1 if s.get('candidate_has') else 0,s.get('roi_score',0)))
    return x
def make_portfolio(skill):
    x=portfolio_agent(skill);pid=db.execute('INSERT INTO portfolio_projects(title,skill_gap,brief) VALUES(?,?,?)',(x.get('title','Project'),skill,x.get('brief','')));return {'id':pid,**x}
def interview_prep(aid):
    r=db.one('SELECT a.*,j.*,ci.summary intel FROM applications a JOIN jobs j ON j.id=a.job_id LEFT JOIN company_intel ci ON ci.company=j.company WHERE a.id=?',(aid,));x=interview_agent(r,read_master_resume(),r.get('intel') or '');db.execute('INSERT INTO interviews(application_id,prep_packet) VALUES(?,?)',(aid,json.dumps(x)));return x
def compare_offers():
    offers=db.query('SELECT o.*,j.title,j.company FROM offers o JOIN applications a ON a.id=o.application_id JOIN jobs j ON j.id=a.job_id');return offer_agent(offers) if offers else {'ranking':[],'tradeoffs':[],'negotiation_points':[]}
