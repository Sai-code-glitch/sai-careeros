from app import db
from app.scoring import warmth
def add_contact(company,name='',title='',email='',linkedin='',relationship='cold',notes=''):return db.execute('INSERT INTO contacts(company,name,title,email,linkedin,relationship,warmth_score,notes) VALUES(?,?,?,?,?,?,?,?)',(company,name,title,email,linkedin,relationship,warmth(relationship),notes))
def network_score(company):
    r=db.query('SELECT warmth_score FROM contacts WHERE company=? ORDER BY warmth_score DESC LIMIT 5',(company,));return min(100,(r[0]['warmth_score'] if r else 0)+max(0,len(r)-1)*5)
def graph():return {'jobs':db.query('SELECT id,title,company,status FROM jobs LIMIT 100'),'contacts':db.query('SELECT id,company,name,title,relationship,warmth_score FROM contacts'),'applications':db.query('SELECT id,job_id,approval_status,apply_status FROM applications')}
