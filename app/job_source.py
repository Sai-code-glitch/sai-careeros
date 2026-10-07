import httpx
from app.config import RAPIDAPI_KEY,RAPIDAPI_HOST
async def discover_jobs(limit=60):
    if not RAPIDAPI_KEY:return []
    qs=['data analyst Michigan','data quality analyst Michigan','master data analyst Michigan','technical data steward Michigan','business data analyst Michigan','remote data analyst USA','supply chain data analyst Michigan'];out=[];headers={'X-RapidAPI-Key':RAPIDAPI_KEY,'X-RapidAPI-Host':RAPIDAPI_HOST}
    async with httpx.AsyncClient(timeout=30) as c:
        for q in qs:
            r=await c.get(f'https://{RAPIDAPI_HOST}/search',headers=headers,params={'query':q,'page':'1','num_pages':'1','date_posted':'week'});r.raise_for_status()
            for x in r.json().get('data',[]):out.append({'external_id':x.get('job_id'),'title':x.get('job_title') or 'Unknown role','company':x.get('employer_name') or 'Unknown company','location':', '.join(filter(None,[x.get('job_city'),x.get('job_state')])),'url':x.get('job_apply_link') or x.get('job_google_link'),'description':x.get('job_description') or '','salary':'','source':x.get('job_publisher') or 'JSearch','posted_at':x.get('job_posted_at_datetime_utc')})
            if len(out)>=limit:break
    seen=set();res=[]
    for j in out:
        k=(j['company'].lower(),j['title'].lower(),j.get('url'))
        if k not in seen and j['description']:seen.add(k);res.append(j)
    return res[:limit]
