"""Safe ATS adapter registry.

Adapters automate navigation and routine fields only. They must stop for CAPTCHAs,
anti-bot challenges, legal/work-authorization declarations, demographic disclosures,
background questions, uncertain answers, and final submission unless explicitly configured
with a user approval step.
"""
ADAPTERS={
 'greenhouse':{'status':'foundation','routine_autofill':True},
 'lever':{'status':'foundation','routine_autofill':True},
 'workday':{'status':'foundation','routine_autofill':True},
 'icims':{'status':'foundation','routine_autofill':True},
 'smartrecruiters':{'status':'foundation','routine_autofill':True},
}
SENSITIVE=['work authorization','authorized to work','sponsorship','citizenship','clearance','veteran','disability','race','gender','criminal','background','salary expectation','non-compete']
def requires_human(question):return any(x in question.lower() for x in SENSITIVE)
