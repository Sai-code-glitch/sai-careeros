import sqlite3
from contextlib import contextmanager
from app.config import DB_PATH
SCHEMA='''
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS jobs(id INTEGER PRIMARY KEY AUTOINCREMENT,external_id TEXT,title TEXT NOT NULL,company TEXT NOT NULL,location TEXT,url TEXT,description TEXT NOT NULL,salary TEXT,source TEXT,posted_at TEXT,match_score INTEGER DEFAULT 0,opportunity_score INTEGER DEFAULT 0,score_reason TEXT,sponsorship_risk TEXT,scam_risk INTEGER DEFAULT 0,ghost_risk INTEGER DEFAULT 0,salary_score INTEGER DEFAULT 50,network_score INTEGER DEFAULT 0,company_score INTEGER DEFAULT 50,status TEXT DEFAULT 'NEW',created_at DATETIME DEFAULT CURRENT_TIMESTAMP,updated_at DATETIME DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS applications(id INTEGER PRIMARY KEY AUTOINCREMENT,job_id INTEGER NOT NULL,variant TEXT DEFAULT 'A',tailored_resume_path TEXT,cover_letter_path TEXT,outreach_draft TEXT,approval_status TEXT DEFAULT 'PENDING',apply_status TEXT DEFAULT 'NOT_APPLIED',applied_at DATETIME,followup_due DATETIME,recruiter_reply INTEGER DEFAULT 0,screen INTEGER DEFAULT 0,interview INTEGER DEFAULT 0,offer INTEGER DEFAULT 0,rejected INTEGER DEFAULT 0,notes TEXT,FOREIGN KEY(job_id) REFERENCES jobs(id));
CREATE TABLE IF NOT EXISTS contacts(id INTEGER PRIMARY KEY AUTOINCREMENT,company TEXT NOT NULL,name TEXT,title TEXT,email TEXT,linkedin TEXT,relationship TEXT DEFAULT 'cold',warmth_score INTEGER DEFAULT 25,last_contact_at DATETIME,notes TEXT);
CREATE TABLE IF NOT EXISTS company_intel(id INTEGER PRIMARY KEY AUTOINCREMENT,company TEXT UNIQUE,summary TEXT,stability_score INTEGER DEFAULT 50,hiring_score INTEGER DEFAULT 50,visa_notes TEXT,interview_notes TEXT,tech_stack TEXT,sentiment_notes TEXT,source_notes TEXT,researched_at DATETIME DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS skill_signals(id INTEGER PRIMARY KEY AUTOINCREMENT,skill TEXT UNIQUE,mentions INTEGER DEFAULT 0,candidate_has INTEGER DEFAULT 0,roi_score REAL DEFAULT 0,updated_at DATETIME DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS portfolio_projects(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT,skill_gap TEXT,brief TEXT,status TEXT DEFAULT 'IDEA',repo_url TEXT,evidence_url TEXT,created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS interviews(id INTEGER PRIMARY KEY AUTOINCREMENT,application_id INTEGER,interview_at DATETIME,interview_type TEXT,interviewer TEXT,prep_packet TEXT,status TEXT DEFAULT 'UPCOMING');
CREATE TABLE IF NOT EXISTS offers(id INTEGER PRIMARY KEY AUTOINCREMENT,application_id INTEGER,base_salary REAL,bonus REAL,equity REAL,benefits_notes TEXT,location TEXT,remote_policy TEXT,visa_support TEXT,career_score INTEGER DEFAULT 0,total_score INTEGER DEFAULT 0,notes TEXT);
CREATE TABLE IF NOT EXISTS audits(id INTEGER PRIMARY KEY AUTOINCREMENT,job_id INTEGER,application_id INTEGER,passed INTEGER DEFAULT 0,risk_level TEXT,findings TEXT,created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS outreach(id INTEGER PRIMARY KEY AUTOINCREMENT,application_id INTEGER,contact_id INTEGER,channel TEXT DEFAULT 'email',subject TEXT,body TEXT,status TEXT DEFAULT 'DRAFT',sent_at DATETIME,replied_at DATETIME);
'''
def init_db():
    DB_PATH.parent.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(DB_PATH) as c:c.executescript(SCHEMA)
@contextmanager
def conn():
    c=sqlite3.connect(DB_PATH);c.row_factory=sqlite3.Row
    try:yield c;c.commit()
    finally:c.close()
def execute(sql,params=()):
    with conn() as c:return c.execute(sql,params).lastrowid
def query(sql,params=()):
    with conn() as c:return [dict(r) for r in c.execute(sql,params).fetchall()]
def one(sql,params=()):
    with conn() as c:
        r=c.execute(sql,params).fetchone();return dict(r) if r else None
