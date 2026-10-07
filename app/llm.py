import json
from openai import OpenAI
from app.config import OPENAI_API_KEY,OPENAI_MODEL,ENABLE_OPENAI_WEB_RESEARCH
from app.profile import PROFILE
client=OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
def call(instructions,payload,web=False):
    if not client:raise RuntimeError('OPENAI_API_KEY is not configured')
    kw={'model':OPENAI_MODEL,'instructions':instructions,'input':json.dumps(payload,ensure_ascii=False)}
    if web and ENABLE_OPENAI_WEB_RESEARCH:kw['tools']=[{'type':'web_search'}]
    return client.responses.create(**kw).output_text
def jcall(instructions,payload,web=False):
    raw=call(instructions+' Return strict JSON only.',payload,web);a,b=raw.find('{'),raw.rfind('}')
    if a<0 or b<0:raise ValueError('No JSON returned')
    return json.loads(raw[a:b+1])
def fit_agent(job,resume):return jcall('Conservative US recruiting analyst. Score only stated resume facts. Detect explicit no-sponsorship. Schema: {"score":0,"reason":"","matches":[],"gaps":[],"sponsorship_block":false,"recommended":false}.',{'profile':PROFILE,'resume':resume,'job':job})
def risk_agent(job):return jcall('Analyze scam, ghost/stale posting, clearance/citizenship, compensation and application risks without unsupported accusations. Schema: {"scam_risk":0,"ghost_risk":0,"sponsorship_risk":"unknown","hard_blocks":[],"warnings":[]}.',{'job':job})
def salary_agent(job):return jcall('Score salary fit only from stated compensation. Do not invent market pay. Schema: {"salary_score":50,"stated_compensation":"","notes":""}.',{'profile':PROFILE,'job':job})
def company_agent(job):return jcall('Research company stability, hiring momentum, visa evidence, interview hints and likely tech stack. Avoid speculation. Schema: {"summary":"","stability_score":50,"hiring_score":50,"visa_notes":"","interview_notes":"","tech_stack":"","sentiment_notes":"","source_notes":""}.',{'job':job},True)
def tailor_agent(job,resume,variant):return jcall(f'ATS resume editor. Variant {variant}. Rephrase/reorder only facts in master resume. Never invent employers, dates, tools, education, metrics, seniority or duties. Schema: {{"headline":"","summary":"","skills":[],"experience":[{{"employer":"","title":"","dates":"","bullets":[]}}],"ats_keywords_used":[],"unverified":[]}}.',{'job':job,'resume':resume,'profile':PROFILE})
def cover_agent(job,resume):return call('Write a concise 250-350 word US cover letter using only resume facts. No fake address or metrics.',{'job':job,'resume':resume})
def outreach_agent(job,resume,contact=None):return call('Write a personalized 90-140 word recruiter/hiring-team outreach email. Low pressure. Use only resume facts.',{'job':job,'resume':resume,'contact':contact or {}})
def supervisor_agent(job,resume,tailored,cover,outreach):return jcall('Final compliance audit. Flag invented facts, unsupported metrics, contradictory dates, misleading seniority, generic outreach and sensitive questions. Schema: {"passed":false,"risk_level":"low|medium|high","findings":[],"required_changes":[]}.',{'job':job,'master_resume':resume,'tailored':tailored,'cover':cover,'outreach':outreach})
def skills_agent(jobs,resume):return jcall('Analyze recurring JD skills, distinguish evidenced skills from gaps and rank career ROI. Schema: {"signals":[{"skill":"","mentions":0,"candidate_has":false,"roi_score":0}],"top_gaps":[],"learning_plan":[],"portfolio_ideas":[]}.',{'jobs':jobs,'resume':resume})
def portfolio_agent(skill):return jcall('Design a small ethical portfolio project proving this skill. Schema: {"title":"","brief":"","deliverables":[],"resume_bullet_after_completion":"","github_structure":[]}.',{'skill':skill})
def interview_agent(job,resume,intel=''):return jcall('Create interview prep grounded only in candidate facts. Schema: {"intro_60s":"","likely_questions":[],"star_stories":[],"technical_topics":[],"questions_to_ask":[],"red_flags_to_avoid":[]}.',{'job':job,'resume':resume,'company_intel':intel})
def offer_agent(offers):return jcall('Compare offers across compensation, visa/security, growth, skills, commute/remote, stability and benefits. Do not invent missing values. Schema: {"ranking":[],"tradeoffs":[],"negotiation_points":[]}.',{'offers':offers,'profile':PROFILE})
