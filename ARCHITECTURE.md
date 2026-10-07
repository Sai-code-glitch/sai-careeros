# Sai CareerOS V2 Architecture

## Daily pipeline

1. Scout discovers current jobs and deduplicates them.
2. Fit Agent scores resume alignment.
3. Risk Agent checks sponsorship blockers, citizenship/clearance barriers, scam signals and ghost/stale-posting signals.
4. Company Intelligence researches company/hiring context when web research is enabled.
5. Salary Agent scores stated compensation fit.
6. Network Agent checks warm contacts and calculates network strength.
7. Opportunity Scorer creates one priority score.
8. Top five jobs enter document production.
9. Resume Agent creates A/B truth-grounded variants.
10. Cover Letter and Outreach Agents generate role-specific copy.
11. Supervisor Agent audits everything against the master resume.
12. Mobile dashboard asks for human approval.
13. ATS layer handles routine autofill and stops at sensitive/uncertain fields.
14. Outcomes are recorded for closed-loop analytics.
15. Weekly Skills Agent recalculates skill demand and portfolio priorities.

## Data model

Jobs → Applications → Outreach → Contacts

Companies → Company Intelligence

Applications → Interviews → Offers

Jobs → Skill Signals → Portfolio Projects

Applications → Audits / Conversion Analytics

## Production principle

Automation is aggressive for reversible preparation/research and conservative for consequential declarations or external communication.
