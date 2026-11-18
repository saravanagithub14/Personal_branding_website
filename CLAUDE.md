# CLAUDE.md: AI Trainer landing page for Saravana Perumal R

Guidance for Claude Code when building the "AI trainer in Kerala" landing page on this Django portfolio. Read this whole file before changing anything.

## Goal

Rank and convert for "AI trainer" (primary) and "AI trainer in Kerala". The page positions Saravana as a researcher who taught himself AI, now teaching it in plain language to non-technical people and businesses. Long-term brand direction (do not put this in page copy yet): AI tools that help researchers do better research.

## Ground rules

- Do not invent facts, numbers, client names or testimonials. Anything not in this file is unknown. Leave a clearly marked `TODO` instead.
- No em dashes in page copy. Use commas or periods. Conversational tone, short and long sentences mixed, no corporate filler.
- One H1 on the page. Sections are H2, services and FAQ questions are H3.
- Use each target keyword naturally two or three times. No stuffing.
- This repo keeps site content in the database (Django admin), and views reshape DB rows into dicts for templates. Check `portfolio/models.py`, `portfolio/views.py`, `portfolio/context_processors.py` and `templates/base.html` before deciding whether this page is a new template with static copy, new models, or admin-edited content. Keep the view's dict shape in sync with the template if you touch a model.
- The V.E.R.A. chatbot answers from `knowledge_base/*.md`. After adding training services to the site, add a matching `knowledge_base/services.md` (same format as the existing files, with a front-matter block per section) and rebuild with `python manage.py build_rag_index --force`. Run `pytest` after.

## Facts you may use (from the CV and profile)

- Name: Saravana Perumal R. Based in Trivandrum (Thiruvananthapuram), Kerala, India.
- Current role: Gen AI Engineer at Blackbox Learning (since April 2026).
- Two book chapters and two research articles, including a 2019 book chapter in Advances in Experimental Medicine and Biology (from the IISER dissertation work). UGC-NET (Assistant Professor, Life Sciences) 2019.

### Experience (confirmed by Saravana, used on about.html)

AI & Data Science:

- **Gen AI Engineer, Blackbox Learning** (Apr 2026 to now). Building generative AI and agentic AI systems in Thiruvananthapuram: RAG pipelines, LangChain agents, vector databases, LLM fine-tuning (LoRA/QLoRA), generative AI deployment on AWS.
- **Data Scientist, Dexpro Innovations Pvt Ltd** (Apr 2025 to Mar 2026). Data analysis and statistical models for decisions; created and delivered data science workshops and learning resources; mentored students in data analysis, machine learning and statistical modelling toward jobs. Promoted from Jr. Data Scientist.
- **Jr. Data Scientist (Training & Development), Dexpro Innovations Pvt Ltd** (Feb 2024 to Feb 2025). First full-time data science role. Data analysis and statistical models, training material and workshops, one-on-one mentoring for data science careers.
- **Data Science Intern, Edure** (Sep 2023 to Feb 2024). Six-month internship alongside the Diploma in Data Science, Thiruvananthapuram. The move from life sciences research into data science.

Research & Life Sciences:

- **Senior Research Fellow, SCTIMST (Govt. of India)** (Jul 2019 to Nov 2023). Biomedical technology at Sree Chitra Tirunal Institute for Medical Sciences and Technology: 3D bioprinting of skin, an antimicrobial self-crosslinking hydrogel, biosynthesized nanosilver. Led and managed research projects with interdisciplinary teams under regulatory standards, statistical analysis of experimental data, reports, presentations and publications.
- **Young Professional II, CIBA, ICAR (Govt. of India)** (Mar 2019 to Jul 2019). Under Dr. M. Makesh on the ICAR-CRP project on Vaccines and Diagnostics, Chennai: vaccines against Nervous Necrosis Virus in sea bass, PCR-based disease diagnosis in aquaculture.
- **Masters Dissertation Scholar, Stem Cell Biology, IISER Thiruvananthapuram** (Nov 2017 to Nov 2018). Periostin-integrin signalling in the regulation of hematopoiesis in the bone marrow niche; cell culture, molecular biology, microscopy. Led to the 2019 book chapter above.
- Education: BSc Botany and Biotechnology (Kerala University, 2013 to 2016), MSc Biotechnology and Bioinformatics (KUFOS, 2016 to 2018), Diploma in Data Science (Edure, 2023 to 2024).
- 18 personal AI projects: RAG chatbots (ChromaDB, Pinecone, AstraDB, FAISS), LangChain agents, text to SQL, LoRA/QLoRA fine-tuning, AWS Bedrock and Lambda apps, YOLO and CNN computer vision (including brain tumour detection from MRI).
- Languages: English, Malayalam, Tamil, Hindi.
- Trained and mentored 100+ students and professionals (confirmed by Saravana; do not state a higher number).
- In-person cities: Trivandrum, Kochi and Ernakulam, Kollam, Alappuzha, Thrissur, Kozhikode. Other places in Kerala on request. Online across India.
- Pricing: do not publish prices. "Contact me for a quote".
- Profiles for schema `sameAs`: linkedin.com/in/saravana-perumal-r-04b368288, github.com/saravanagithub14, medium.com/@mynamesaravanaperumal, instagram.com/prof_ds_.

## Open items (ask Saravana, do not guess)

1. ~~One email and one base city.~~ Resolved: email is saravanaperumalr14@gmail.com, base city Trivandrum. Use this set everywhere, including schema and footer. Do not display any phone number on the site (Saravana's request): no phone line, no `telephone` in schema, and the WhatsApp number is never shown as text. WhatsApp is reached only through wa.me buttons labelled "Message on WhatsApp".
2. Named clients or institutions he may mention.
3. Two or three concrete outcomes from past training.
4. Testimonials (name, role, one or two lines).
5. Typical workshop length, group size, and what participants receive afterwards.
6. His signature session topic.
7. Real photos of him teaching (needed for hero image and alt text).
8. The live domain, for canonical URL and schema.
9. Research span. The dated research roles run Nov 2017 to Nov 2023 (about six years), but the page copy says "about seven years in research". Confirm which figure to use before changing the copy.
10. Titles and links for the second book chapter and the two research articles.

## SEO metadata

- URL: `/ai-trainer-in-kerala/`
- Title tag (57 chars): `AI Trainer in Kerala | Saravana Perumal R, Gen AI Trainer`
- Meta description (151 chars): `Saravana Perumal R is an AI trainer in Trivandrum, Kerala. Corporate AI training, generative AI and agentic AI workshops, and mentoring across India.`
- H1: `AI Trainer in Kerala: Learn and Build with AI, Even Without a Tech Background`
- Per-page title and description must come from template blocks or context, never one sitewide value. Add canonical link and Open Graph tags (`og:title`, `og:description`, `og:image`).

### Keyword map

| Keyword | Where it goes |
| --- | --- |
| AI trainer | Title, H1, hero, about, CTA |
| AI trainer in Kerala | Title, H1, hero, location section |
| AI trainer in Trivandrum (Thiruvananthapuram) | Location section, FAQ, footer address |
| AI trainer in India | Location section, FAQ |
| generative AI trainer | Services (generative AI block), about |
| Gen AI trainer India | Services, FAQ |
| agentic AI trainer | Services (agentic AI block) |
| AI corporate trainer | Services (corporate block), FAQ |
| AI workshop trainer | Services (workshop block), FAQ |
| AI mentor | Services (mentoring block), about |
| freelance AI trainer | Services (freelance block), FAQ |

Search volumes were not verified for India. Do not claim any volume in code or copy.

## Page copy (use as written)

### Hero

# AI Trainer in Kerala: Learn and Build with AI, Even Without a Tech Background

I'm Saravana Perumal R, an AI trainer and mentor based in Trivandrum. I teach generative AI and agentic AI to students, teams and companies across Kerala and India, in plain language, with real projects instead of theory dumps.

I didn't start in tech. I started in a biology lab, working on stem cells, vaccines and 3D bioprinted skin. I taught myself AI from scratch, built my own projects, and then started teaching it. So when you tell me AI feels too technical, I know exactly where you're stuck. I was there.

Buttons: `Book an AI workshop` | `Talk about corporate AI training` | `Find an AI mentor`

Trust line: Gen AI Engineer at Blackbox Learning · 100+ learners trained and mentored · Teaching since 2024 · Researcher turned AI builder · Teaches in English, Malayalam, Tamil and Hindi

### About: a researcher who taught himself AI

**Why a biologist makes a good AI trainer**

I spent about seven years in research, at IISER Thiruvananthapuram, ICAR's Central Institute of Brackishwater Aquaculture in Chennai, and Sree Chitra Tirunal Institute (SCTIMST), where I worked for over four years as a Senior Research Fellow. I've published two book chapters and two research articles. I qualified the UGC-NET for Assistant Professor in Life Sciences in 2019.

In 2023 I moved into data science, then into generative AI. I learned it the hard way: reading, building, breaking things, rebuilding. That's why I teach it the way I do. I explain one idea at a time, I show it working, and I make sure you build something yourself before the session ends.

**What I've built, which is what I teach from**

I'm a Gen AI Engineer at Blackbox Learning, and I've built 18 AI projects of my own. A few of them:

- Chatbots that answer questions from your own PDFs and documents (RAG)
- AI agents that use tools, search, and query databases in plain English
- Fine-tuned language models, and apps deployed on AWS
- Computer vision work, including brain tumour detection from MRI scans

I don't teach what I've only read about. Everything in my sessions is something I've built.

**Teaching experience**

I've been teaching and mentoring since February 2024. At Dexpro Innovations I created workshops and learning material, taught statistics, Python, machine learning and generative AI, and mentored students through placements. I now train students, working professionals and teams in generative AI and agentic AI.

I've trained and mentored more than 100 students and professionals, through workshops, courses and one-on-one mentoring.

### What I teach and how you can work with me

**Corporate AI training for your team.** I work as an AI corporate trainer for companies that want their people using AI properly, not just trying ChatGPT once. We start with the tasks your team actually does, then build AI into those: reports, emails, documents, customer replies, data. Your team leaves with working prompts, simple automations and clear rules for using AI safely at work. No technical background needed.

**AI workshops for colleges and communities.** As an AI workshop trainer, I run half-day and full-day sessions for students, faculty and mixed groups. Every workshop is hands-on: participants build something small and real before they leave. Online or in person, in English or Malayalam, Tamil and Hindi.

**Generative AI training.** I'm a generative AI trainer for beginners and working professionals across India. You'll learn how large language models work in plain terms, how to write prompts that give useful answers, and how to build your own chatbot that answers from your own documents.

**Agentic AI training.** As an agentic AI trainer, I teach how AI agents plan, use tools, search, and finish multi-step tasks. This is the newest and fastest-moving part of AI. I teach it with projects I've built myself, including agents that query databases and search the web.

**AI mentoring, one on one.** If you want a personal AI mentor, I work with you over several weeks. It suits career switchers, students and researchers. We set a learning roadmap, pick a project, and meet regularly so you keep moving. I made this switch myself, from lab research to AI, so I can tell you what to learn first and what to skip.

**Freelance AI trainer for hire.** As a freelance AI trainer, I take on single sessions, short courses and custom training programmes. Tell me your audience and goal, and I'll design the content around it.

### Who I train, and where

Who it's for:

- Students and fresh graduates who want an AI skill that helps them get hired
- Career switchers, especially people from biology, commerce, arts and other non-tech fields
- Working professionals and business owners who want to use AI in daily work
- College faculty and researchers who want to bring AI into teaching and research
- Companies and teams with no in-house AI expertise

**AI trainer in Kerala, Trivandrum and across India**

I'm an AI trainer in Trivandrum (Thiruvananthapuram), Kerala, and I take sessions in person across Kerala. If you're elsewhere, I teach online, so I work as an AI trainer in India for colleges, companies and learners in any city. Sessions run in English, Malayalam, Tamil or Hindi, whichever your group is most comfortable in.

Looking for an AI trainer near you? Send me your city, group size and goal, and I'll tell you what's possible.

**Cities I cover in person:** Trivandrum (Thiruvananthapuram), Kochi and Ernakulam, Kollam, Alappuzha, Thrissur and Kozhikode. Other places in Kerala on request.

### Frequently asked questions

Render as visible text and as `FAQPage` JSON-LD. The schema text must match the visible text exactly.

**Who is the best AI trainer in Kerala for beginners?** The best fit is someone who remembers being a beginner. I'm a Trivandrum-based AI trainer who started with no tech background and taught myself AI. I explain things in plain language, in English or Malayalam, and every session ends with something you've built.

**Do I need coding or a technical background to join your AI training?** No. Most of my learners are not technical. We start with how AI works in simple terms and with tools you can use right away. Coding is added only if your goal needs it.

**Can you train my company's team as a corporate AI trainer?** Yes. I design corporate AI training around your team's real tasks, such as documents, reports, customer messages and data. Tell me the team size and the work they do, and I'll propose a plan.

**Do you run AI workshops for colleges and schools?** Yes. As an AI workshop trainer, I run half-day and full-day workshops for students and faculty, in person in Kerala or online anywhere in India.

**What is the difference between generative AI and agentic AI training?** Generative AI training covers tools that create text, images and answers from a prompt, like ChatGPT. Agentic AI training goes a step further: AI that plans, uses tools and completes multi-step tasks on its own. I teach both, starting with generative AI.

**Are you available as a freelance AI trainer outside Kerala?** Yes. I take freelance training work across India, mostly online. For in-person sessions outside Kerala, we can discuss travel.

**Do you offer one-on-one AI mentoring?** Yes. As an AI mentor, I work with career switchers, students and researchers over several weeks: a roadmap, a real project, and regular check-ins.

**How do I book you?** Send a message on WhatsApp or email with your city, group size and goal. I reply with what I'd recommend and how we could work together.

**What are your fees for AI training?** Fees depend on the audience, group size, number of days, and whether the session is online or in person. Message me with those details and I'll send you a quote.

### Call to action and contact

**Let's plan your AI training.** Tell me who you want to train, how many people, and what you want them to be able to do. I'll reply with a clear plan, usually within a day.

Buttons: `Message me on WhatsApp` | `Email me` | `Connect on LinkedIn`

Footer line: Saravana Perumal R, AI trainer and mentor, Trivandrum (Thiruvananthapuram), Kerala, India. Available in person across Kerala and online across India.

## Technical SEO tasks

1. Add `ProfessionalService` JSON-LD in the page head (replace the domain and image):

```json
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Saravana Perumal R, AI Trainer",
  "description": "AI trainer and mentor in Trivandrum, Kerala. Corporate AI training, generative AI and agentic AI workshops across India.",
  "url": "https://YOUR-DOMAIN/ai-trainer-in-kerala/",
  "image": "https://YOUR-DOMAIN/static/img/saravana.jpg",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Thiruvananthapuram",
    "addressRegion": "Kerala",
    "addressCountry": "IN"
  },
  "areaServed": ["Kerala", "India"],
  "knowsAbout": ["Generative AI", "Agentic AI", "AI training", "AI mentoring"],
  "sameAs": [
    "https://www.linkedin.com/in/saravana-perumal-r-04b368288",
    "https://github.com/saravanagithub14",
    "https://medium.com/@mynamesaravanaperumal",
    "https://www.instagram.com/prof_ds_"
  ]
}
```

2. Add `FAQPage` JSON-LD generated from the same FAQ data the template renders, so text never drifts.
3. Images: real photos only. Alt text examples: `Saravana Perumal R, AI trainer in Kerala, teaching a generative AI workshop`, `AI corporate training session in Trivandrum`. File names like `ai-trainer-kerala.jpg`. Lazy-load below the fold, serve modern formats, set width and height to avoid layout shift.
4. Add the page to the sitemap and make sure `robots.txt` allows it. Check the site already has both.
5. Internal links: from the homepage and navigation to this page with anchor text "AI trainer in Kerala". Plan later pages `/corporate-ai-training/`, `/ai-workshops/`, `/ai-mentor/` and link the service blocks to them once they exist.
6. Mobile first. Check Core Web Vitals after build (the chat widget loads heavy models server side, so keep the front-end light).

## After launch (for Saravana, not code)

- Create a Google Business Profile with the same name, city and phone as the page.
- Submit the URL in Google Search Console, then check which queries show impressions after two weeks.
- Keep the LinkedIn headline close to the page title, for example "AI Trainer & Mentor | Generative AI and Agentic AI | Kerala".

## Definition of done

- Page renders at `/ai-trainer-in-kerala/` with the exact title, description and H1 above.
- Both JSON-LD blocks validate in Google's Rich Results Test.
- No placeholder text, `YOUR-DOMAIN` or `TODO` left in the shipped page.
- `pytest` passes, `knowledge_base/services.md` added and the index rebuilt.
