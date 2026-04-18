---
title: OpenAI ai-in-the-enterprise
source_file: OpenAI ai-in-the-enterprise.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:22:22.135914
raw_file_updated: 2026-04-17T20:22:22.135914
version: 1
sources:
  - file: OpenAI ai-in-the-enterprise.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:22:22.135914
tags: []
related_topics: []
backlinked_by: []
---
# AI in the Enterprise

## Overview

**AI in the Enterprise** is a comprehensive guide published by [[OpenAI]] that synthesizes lessons from seven frontier companies implementing [[artificial intelligence]] solutions in business contexts. The guide emphasizes that successful AI adoption requires treating AI as a new paradigm rather than traditional software deployment, utilizing an [[iterative development]] approach that prioritizes experimentation, rigorous evaluation, and continuous learning from real-world use cases.

## Executive Summary

The document presents seven key lessons for enterprise AI adoption:

1. **Start with evals** - Use systematic evaluation processes to measure model performance
2. **Embed AI into your products** - Create new customer experiences through AI integration
3. **Start now and invest early** - Begin immediately to benefit from compounding improvements
4. **Customize and fine-tune your models** - Tailor AI to specific organizational needs
5. **Get AI in the hands of experts** - Empower domain specialists to drive implementation
6. **Unblock your developers** - Automate development workflows to accelerate innovation
7. **Set bold automation goals** - Aim high when automating routine processes

---

## Core Concepts

### The New Paradigm of AI Deployment

AI implementation differs fundamentally from traditional software or [[cloud computing]] deployment. Successful enterprises adopt an experimental mindset and iterative approach that accelerates value realization while building stakeholder buy-in.

#### Three Dimensions of AI Value

Organizations implementing AI effectively see measurable improvements across three fronts:

- **[[Workforce Performance]]** - Enabling employees to deliver higher-quality outputs in shorter timeframes
- **[[Automation]]** - Freeing people from repetitive tasks to focus on value-added work
- **[[Product Enhancement]]** - Delivering more relevant and responsive [[customer experience|customer experiences]]

### OpenAI's Organizational Approach

OpenAI structures its work around three specialized teams:

| Team | Function |
|------|----------|
| **Research Team** | Advances AI foundations through new models and capabilities |
| **Applied Team** | Transforms models into products like [[ChatGPT Enterprise]] and the [[OpenAI API]] |
| **Deployment Team** | Implements products within enterprises to address specific use cases |

This structure enables **iterative deployment** - a process of shipping regular updates, gathering feedback, and continuously improving performance and safety.

---

## Seven Lessons for Enterprise AI Adoption

### Lesson 1: Start with Evals

#### Definition and Purpose

An **[[evaluation|eval]]** is a rigorous, structured process for measuring how AI models perform against benchmarks in specific use cases. Evaluations serve dual purposes: validating model quality and providing a continuous feedback mechanism for improvement.

#### Case Study: Morgan Stanley

**Context:** As a global financial services leader, Morgan Stanley needed to ensure AI integration aligned with the personal, sensitive nature of client relationships.

**Implementation:**
- Conducted intensive evals for every proposed AI application
- Three initial model evaluations:
  - **Language Translation** - Measuring accuracy and translation quality
  - **Summarization** - Evaluating information condensing against agreed metrics
  - **Human Trainer Comparison** - Benchmarking AI results against expert advisor responses

**Results:**
- 98% of advisors now use OpenAI daily
- Document access increased from 20% to 80%
- Search time dramatically reduced
- Follow-ups that previously took days now occur within hours
- Overwhelmingly positive advisor feedback reporting increased client engagement

**Key Insight:** Rigorous evals build organizational confidence in AI systems, enabling production rollout with stakeholder support.

---

### Lesson 2: Embed AI into Your Products

#### Strategic Approach

When AI automates tedious work, employees focus on uniquely human capabilities. Because AI processes vast data amounts from multiple sources, it can create experiences that feel more human through greater relevance and personalization.

#### Case Study: Indeed

**Context:** The world's #1 job site sought to improve job matching and candidate experience.

**Implementation:**
- Used [[GPT-4o mini]] to match job seekers with opportunities in new ways
- Leveraged [[natural language processing|natural language]] and data analysis to explain *why* specific jobs were recommended
- Customized context for "Invite to Apply" feature explaining candidate fit

**Results:**
- 20% increase in job applications started
- 13% uplift in downstream hiring success
- 20+ million messages monthly to job seekers
- 350 million monthly site visitors

**Optimization:**
- Partnered to fine-tune a smaller GPT model
- Achieved similar results with 60% fewer [[tokens|tokens]]

**Key Insight:** Embedding AI with contextual explanations creates more human-centered experiences at scale.

---

### Lesson 3: Start Now and Invest Early

#### The Compounding Effect

AI rarely provides plug-and-play solutions. Use cases grow in sophistication and impact through iteration. Earlier implementation enables organizations to benefit from compounding improvements across the business.

#### Case Study: Klarna

**Context:** A global payments network and shopping platform sought to streamline customer service.

**Implementation:**
- Introduced an AI assistant to handle customer service interactions
- Continuous testing and refinement over months
- Organization-wide adoption: 90% of employees use AI in daily work

**Results:**
- Assistant handles two-thirds of all service chats
- Equivalent to work of hundreds of agents
- Average resolution time: 11 minutes → 2 minutes
- Projected $40 million profit improvement
- Satisfaction scores maintained at parity with human support

**Key Insight:** Early investment combined with broad organizational adoption enables benefits to compound across the entire business.

---

### Lesson 4: Customize and Fine-tune Your Models

#### What is Fine-tuning?

If a base GPT model is a "store-bought suit," [[fine-tuning]] is the tailored option. It customizes models to an organization's specific data and needs, improving performance for particular use cases.

#### Why Fine-tuning Matters

| Benefit | Description |
|---------|-------------|
| **Improved Accuracy** | Training on unique data (product catalogs, FAQs) delivers more relevant, on-brand results |
| **Domain Expertise** | Models better understand industry terminology, style, and context |
| **Consistent Tone & Style** | Maintains brand voice in all outputs; ensures proper formatting |
| **Faster Outcomes** | Reduces manual editing and re-checking, freeing teams for high-value work |

#### Case Study: Lowe's

**Context:** The Fortune 50 home improvement company needed to improve ecommerce search accuracy despite thousands of suppliers with incomplete or inconsistent product data.

**Challenge:** Requires accurate product descriptions, intelligent tagging, and understanding of how shoppers search across different product categories.

**Implementation:**
- Fine-tuned OpenAI models on Lowe's product data
- Focused on improving product tagging and error detection

**Results:**
- 20% improvement in product tagging accuracy
- 60% improvement in error detection
- Significant team excitement upon seeing results

**Product Note:** [[Vision Fine-Tuning]] further improves ecommerce search and addresses challenges in medical imaging and autonomous driving.

---

### Lesson 5: Get AI in the Hands of Experts

#### Core Principle

Employees closest to processes and problems are best-positioned to identify AI-driven solutions. Empowering domain experts with AI tools is more powerful than building generic horizontal solutions.

#### Case Study: BBVA

**Context:** A global banking leader with 125,000 employees, each facing unique challenges and opportunities.

**Implementation:**
- Rolled out [[ChatGPT Enterprise]] globally
- Worked closely with Legal, Compliance, and IT Security teams
- Enabled employees to discover their own use cases
- Introduced [[custom GPTs]] for domain-specific applications

**Results:**
- 2,900+ custom GPTs created in five months
- Many reduce project and process timelines from weeks to hours

**Department-Specific Applications:**

| Department | Application |
|------------|-------------|
| **Credit Risk** | Faster, more accurate creditworthiness determination |
| **Legal** | Answers 40,000 annual questions on policies and compliance |
| **Customer Service** | Automates sentiment analysis of NPS surveys |
| **Marketing, Risk Management, Operations** | Continuous expansion of use cases |

**Product Feature: Deep Research**

ChatGPT can work independently through deep research, synthesizing hundreds of online sources to create comprehensive, PhD-level reports. Internal evaluation showed deep research saves an average of 4 hours per complex task.

**Key Insight:** Democratizing AI access to domain experts accelerates innovation across organizational silos.

---

### Lesson 6: Unblock Your Developers

#### The Developer Bottleneck

Developer resources represent the primary constraint and growth inhibitor in many organizations. Overwhelmed engineering teams slow innovation and create insurmountable application backlogs.

#### Case Study: Mercado