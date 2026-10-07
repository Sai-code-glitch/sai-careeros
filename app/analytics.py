from app import db
def funnel():
    r=db.query('SELECT * FROM applications');return {'prepared':len(r),'applications':sum(x['apply_status']=='APPLIED' for x in r),'replies':sum(x['recruiter_reply'] for x in r),'screens':sum(x['screen'] for x in r),'interviews':sum(x['interview'] for x in r),'offers':sum(x['offer'] for x in r),'rejections':sum(x['rejected'] for x in r)}
def variants():
    r=db.query('SELECT * FROM applications');o={}
    for v in sorted(set(x['variant'] for x in r)):
        s=[x for x in r if x['variant']==v];a=max(1,sum(x['apply_status']=='APPLIED' for x in s));o[v]={'prepared':len(s),'applied':a,'reply_rate':round(100*sum(x['recruiter_reply'] for x in s)/a,1),'interview_rate':round(100*sum(x['interview'] for x in s)/a,1)}
    return o
