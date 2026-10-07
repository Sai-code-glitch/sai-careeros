from pathlib import Path
from fastapi import FastAPI,HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app import db
from app.agent import ingest_job,score_new,prepare_top,daily_run
from app.analytics import funnel,variants
from app.network import add_contact,graph
from app.intelligence import refresh_skills,make_portfolio,interview_prep,compare_offers
from app.config import APP_HOST,APP_PORT
app=FastAPI(title='Sai CareerOS',version='2.0.0');app.mount('/static',StaticFiles(directory=Path(__file__).parent/'static'),name='static')
class JobIn(BaseModel):title:str;company:str;description:str;location:str|None=None;url:str|None=None;salary:str|None=None;source:str|None='manual'
class ContactIn(BaseModel):company:str;name:str='';title:str='';email:str='';linkedin:str='';relationship:str='cold';notes:str=''
class OutcomeIn(BaseModel):recruiter_reply:int=0;screen:int=0;interview:int=0;offer:int=0;rejected:int=0;apply_status:str|None=None
class PortfolioIn(BaseModel):skill:str
@app.on_event('startup')
async def startup():
    db.init_db();s=AsyncIOScheduler(timezone='America/Detroit');s.add_job(daily_run,'cron',hour=6,minute=0,id='daily',replace_existing=True);s.add_job(refresh_skills,'cron',day_of_week='sun',hour=18,minute=0,id='skills',replace_existing=True);s.start();app.state.scheduler=s
@app.get('/')
def home():return FileResponse(Path(__file__).parent/'static'/'index.html')
@app.get('/api/dashboard')
def dashboard():return {'jobs':db.query('SELECT j.*,a.id application_id,a.variant,a.approval_status,a.apply_status,a.tailored_resume_path,a.cover_letter_path,a.outreach_draft,a.followup_due FROM jobs j LEFT JOIN applications a ON a.job_id=j.id ORDER BY j.created_at DESC LIMIT 150'),'funnel':funnel(),'variants':variants(),'skills':db.query('SELECT * FROM skill_signals ORDER BY roi_score DESC LIMIT 20'),'contacts':db.query('SELECT * FROM contacts ORDER BY warmth_score DESC LIMIT 20')}
@app.post('/api/jobs')
async def add_job(j:JobIn):return {'job_id':await ingest_job(j.model_dump())}
@app.post('/api/run')
async def run():return await daily_run()
@app.post('/api/score')
async def score():await score_new();return {'status':'ok'}
@app.post('/api/prepare')
async def prep():return {'prepared':await prepare_top()}
@app.post('/api/applications/{aid}/approve')
def approve(aid:int):
    a=db.one('SELECT * FROM applications WHERE id=?',(aid,));
    if not a:raise HTTPException(404,'Application not found')
    db.execute("UPDATE applications SET approval_status='APPROVED' WHERE id=?",(aid,));db.execute("UPDATE jobs SET status='APPROVED' WHERE id=?",(a['job_id'],));return {'status':'APPROVED'}
@app.post('/api/applications/{aid}/reject')
def reject(aid:int):db.execute("UPDATE applications SET approval_status='REJECTED' WHERE id=?",(aid,));return {'status':'REJECTED'}
@app.post('/api/applications/{aid}/outcome')
def outcome(aid:int,o:OutcomeIn):db.execute('UPDATE applications SET recruiter_reply=?,screen=?,interview=?,offer=?,rejected=?,apply_status=COALESCE(?,apply_status) WHERE id=?',(o.recruiter_reply,o.screen,o.interview,o.offer,o.rejected,o.apply_status,aid));return {'status':'updated'}
@app.post('/api/contacts')
def contact(c:ContactIn):return {'contact_id':add_contact(**c.model_dump())}
@app.get('/api/graph')
def relationship_graph():return graph()
@app.post('/api/skills/refresh')
def skills():return refresh_skills()
@app.post('/api/portfolio')
def portfolio(p:PortfolioIn):return make_portfolio(p.skill)
@app.post('/api/interviews/{aid}/prepare')
def interview(aid:int):return interview_prep(aid)
@app.get('/api/offers/compare')
def offers():return compare_offers()
@app.get('/api/file/{aid}/{kind}')
def file(aid:int,kind:str):
    a=db.one('SELECT * FROM applications WHERE id=?',(aid,));
    if not a:raise HTTPException(404,'Not found')
    p=a['tailored_resume_path'] if kind=='resume' else a['cover_letter_path']
    if not p or not Path(p).exists():raise HTTPException(404,'File not found')
    return FileResponse(p,filename=Path(p).name)
if __name__=='__main__':
    import uvicorn;uvicorn.run('app.main:app',host=APP_HOST,port=APP_PORT,reload=False)
