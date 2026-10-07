# Sai CareerOS V2

A phone-first, cloud-ready AI career operating system built around the user's verified master resume.

## Included upgrades

- Multi-agent workflow: Scout, Fit, Risk, Company Intelligence, Salary, Network, Resume, Cover Letter, Outreach, Supervisor, Skills, Portfolio, Interview, Analytics and Offer agents.
- Opportunity score combining resume fit, company signals, salary fit, network strength and risk penalties.
- Company research with optional current-web research through the OpenAI Responses API.
- Sponsorship/clearance/hard-block filtering.
- Scam-risk and stale/ghost-posting risk scoring.
- Recruiter/contact CRM with warm-path scoring.
- Resume A/B testing and conversion analytics.
- Truth-grounded resume tailoring and final supervisor audit.
- Skill-demand analysis, career-ROI ranking and evidence-building portfolio projects.
- Interview packet generator: 60-second intro, likely questions, STAR map, technical topics and questions to ask.
- Offer-comparison engine.
- Phone-friendly PWA dashboard.
- Daily 6:00 AM America/Detroit scheduler plus weekly skill intelligence.
- Foundation registry for Greenhouse, Lever, Workday, iCIMS and SmartRecruiters.

## Safety / accuracy boundaries

CareerOS automates research, ranking, document preparation and routine autofill. It is designed to stop for legal declarations, immigration/work-authorization answers, citizenship/clearance, salary commitments, background disclosures, demographic/EEO questions, CAPTCHAs, anti-bot challenges, and anything uncertain. It does not invent qualifications or bypass site protections.

## Start

```bash
cp .env.example .env
# add OPENAI_API_KEY
# optional: add RAPIDAPI_KEY for live job discovery

docker compose up --build
```

Open `http://localhost:8000`. On iPhone Safari: **Share → Add to Home Screen**.

## 24/7 deployment

Deploy the Docker container to a persistent host and persist `/app/data` and `/app/generated`. Use HTTPS and protected authentication before making the dashboard publicly accessible. Store API/OAuth secrets in the host's secret manager, not in the repository.

## Optional current company research

Set:

```env
ENABLE_OPENAI_WEB_RESEARCH=true
```

The company-intelligence agent will use OpenAI web search through the Responses API. Leave it false to reduce API spend.

## Live integrations still require credentials

The product contains the integration points, but no application can manufacture your private credentials. To make every part live, configure:

- OpenAI API key
- licensed/current job-feed key (included adapter is JSearch-compatible)
- Gmail OAuth credentials for autonomous draft/send workflows
- optional licensed recruiter/contact data source
- deployment host/domain

## Outcome-learning loop

Record recruiter replies, screens, interviews, offers and rejections. CareerOS compares resume variants and uses recurring JD skills to guide what to learn or demonstrate next.
