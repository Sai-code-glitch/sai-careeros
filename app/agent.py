import json
from datetime import datetime,timedelta
from app import db
from app.config import DAILY_JOB_LIMIT,DISCOVERY_LIMIT,MIN_MATCH_SCORE
from app.job_source import discover_jobs
from app.resume import read_master_resume,save_resume,save_cover
from app.llm import fit_agent,risk_agent,salary_agent,tailor_agent,cover_agent,outreach_agent,supervisor_agent
from app.intelligence import company
from app.network import network_score
from app.scoring import opportunity_score
async def ingest_job(j):
    e=db.one("SELECT id FROM jobs WHERE company=? AND title=? AND COALESCE(url,'')=COALESCE(?,'')",(j['company'],j['title'],j.get('url')))
    if e:return e['id']
    return db.execute('INSERT INTO jobs(external_id,title,company,location,url,description,salary,source,posted_at) VALUES(?,?,?,?,?,?,?,?,?)',(j.get('external_id'),j['title'],j['company'],j.get('location'),j.get('url'),j['description'],j.get('salary'),j.get('source'),j.get('posted_at')))
async def score_new():
    resume=read_master_resume()
    for j in db.query("SELECT * FROM jobs WHERE status='NEW' LIMIT 100"):
        try:
            f=fit_agent(j,resume);r=risk_agent(j);s=salary_agent(j);ci=company(j);ns=network_score(j['company']);cs=round((ci['stability_score']+ci['hiring_score'])/2);op=opportunity_score(f.get('score',0),r.get('scam_risk',0),r.get('ghost_risk',0),s.get('salary_score',50),ns,cs)
            st='REJECTED_SPONSORSHIP' if f.get('sponsorship_block') else ('REJECTED_HARD_BLOCK' if r.get('hard_blocks') else ('REJECTED_LOW_MATCH' if f.get('score',0)<MIN_MATCH_SCORE else 'SHORTLISTED'))
            db.execute('UPDATE jobs SET match_score=?,opportunity_score=?,score_reason=?,sponsorship_risk=?,scam_risk=?,ghost_risk=?,salary_score=?,network_score=?,company_score=?,status=? WHERE id=?',(f.get('score',0),op,f.get('reason',''),r.get('sponsorship_risk','unknown'),r.get('scam_risk',0),r.get('ghost_risk',0),s.get('salary_score',50),ns,cs,st,j['id']))
        except Exception as e:db.execute('UPDATE jobs SET score_reason=? WHERE id=?',(f'Analysis error: {e}',j['id']))
async def prepare_top():
    resume=read_master_resume();jobs=db.query("SELECT * FROM jobs j WHERE status='SHORTLISTED' AND NOT EXISTS(SELECT 1 FROM applications a WHERE a.job_id=j.id) ORDER BY opportunity_score DESC LIMIT ?",(DAILY_JOB_LIMIT,));out=[]
    for i,j in enumerate(jobs):
        v='A' if i%2==0 else 'B';t=tailor_agent(j,resume,v);rp=save_resume(j['id'],t,v);c=cover_agent(j,resume);cp=save_cover(j['id'],j['company'],j['title'],c,v);contacts=db.query('SELECT * FROM contacts WHERE company=? ORDER BY warmth_score DESC LIMIT 1',(j['company'],));o=outreach_agent(j,resume,contacts[0] if contacts else None);aid=db.execute('INSERT INTO applications(job_id,variant,tailored_resume_path,cover_letter_path,outreach_draft,followup_due) VALUES(?,?,?,?,?,?)',(j['id'],v,rp,cp,o,(datetime.now()+timedelta(days=7)).isoformat(timespec='seconds')));audit=supervisor_agent(j,resume,t,c,o);db.execute('INSERT INTO audits(job_id,application_id,passed,risk_level,findings) VALUES(?,?,?,?,?)',(j['id'],aid,1 if audit.get('passed') else 0,audit.get('risk_level','medium'),json.dumps(audit)));db.execute('UPDATE jobs SET status=? WHERE id=?',('READY_FOR_REVIEW' if audit.get('passed') else 'NEEDS_FIX',j['id']));out.append({'job_id':j['id'],'application_id':aid,'variant':v,'audit':audit})
    return out
async def daily_run():
    live=await discover_jobs(DISCOVERY_LIMIT)
    for j in live:await ingest_job(j)
    await score_new();return {'discovered':len(live),'prepared':await prepare_top()}
