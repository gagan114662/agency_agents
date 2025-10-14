# Requirements Gathering Protocol

## 🎯 Core Principle

**NEVER START CODING WITHOUT COMPLETE REQUIREMENTS**

Before writing a single line of code, you MUST gather comprehensive requirements through systematic questioning. This ensures you build exactly what the user needs, the first time.

## 🚨 MANDATORY: Pre-Coding Checklist

Before ANY code is written, you MUST:
- [ ] Ask minimum 5-10 questions for small features
- [ ] Ask minimum 15-25 questions for full projects
- [ ] Cover ALL 10 question categories (see below)
- [ ] Get clear answers to all critical questions
- [ ] Create comprehensive project brief
- [ ] Get user confirmation on requirements
- [ ] Save requirements to `ai/memory-bank/project-brief.md`

**VIOLATION**: Writing code before completing this checklist is a CRITICAL ERROR.

## 📋 The 10 Essential Question Categories

### Category 1: Project Scope & Goals (2-5 questions)
**Purpose**: Understand the "why" and "what" of the project

**Essential Questions**:
1. "What is the primary goal of this project? What problem does it solve?"
2. "Who are the target users? What are their main characteristics and needs?"
3. "How will success be measured? What metrics matter?"
4. "What are the must-have features for initial launch (P0)?"
5. "What features are nice-to-have but can wait (P1, P2)?"

**Why this matters**: Without clear goals, you'll build the wrong solution.

### Category 2: Technical Stack & Architecture (3-5 questions)
**Purpose**: Determine the technology foundation

**Essential Questions**:
1. "Do you have preferred technologies? (e.g., React vs Vue, Python vs Node.js)"
2. "Is this a web app, mobile app, desktop app, API, or multiple?"
3. "What's your database preference? (PostgreSQL, MySQL, MongoDB, etc.)"
4. "What's the expected system architecture? (Monolith, microservices, serverless)"
5. "Are there any specific libraries or frameworks you want to use?"

**Why this matters**: Wrong tech stack = costly rewrites later.

### Category 3: User Experience & Design (2-4 questions)
**Purpose**: Understand the visual and interaction requirements

**Essential Questions**:
1. "Do you have existing designs, wireframes, or mockups?"
2. "What's your preferred design style? (Minimal, modern, corporate, playful, luxury)"
3. "What devices must be supported? (Desktop, tablet, mobile, all)"
4. "Are there any accessibility requirements? (WCAG level, screen reader support)"

**Why this matters**: Design decisions impact architecture and implementation.

### Category 4: Data & Business Logic (3-6 questions)
**Purpose**: Understand the data model and business rules

**Essential Questions**:
1. "What are the main data entities in your system?" (e.g., Users, Products, Orders)
2. "What are the key relationships between these entities?"
3. "What business rules or validations are required?"
4. "What are the expected data volumes?" (Users, records, storage)
5. "Are there any complex calculations or algorithms needed?"
6. "What are the critical edge cases or error scenarios?"

**Why this matters**: Data model is the foundation of your application.

### Category 5: Integration & APIs (2-4 questions)
**Purpose**: Identify external system dependencies

**Essential Questions**:
1. "Do you need to integrate with any existing systems or APIs?"
2. "What authentication/authorization is required?" (JWT, OAuth, session, etc.)
3. "Will this system expose APIs for other applications?"
4. "Are there any third-party services to integrate?" (Payment, email, SMS, analytics)

**Why this matters**: Integration complexity significantly impacts timeline.

### Category 6: Performance & Scale (2-3 questions)
**Purpose**: Set performance expectations

**Essential Questions**:
1. "How many concurrent users do you expect?" (Now and future)
2. "What's the acceptable response time?" (<2s, <5s, <10s)
3. "What's the expected data growth rate?" (Records per day/month)

**Why this matters**: Performance requirements drive architectural decisions.

### Category 7: Security & Compliance (2-3 questions)
**Purpose**: Identify security and regulatory requirements

**Essential Questions**:
1. "What security level is required?" (Public app, sensitive data, financial, healthcare)
2. "Are there any compliance requirements?" (GDPR, HIPAA, SOC 2, PCI-DSS)
3. "What data needs special protection?" (PII, financial, health, etc.)

**Why this matters**: Security cannot be bolted on later.

### Category 8: Testing & Quality (2-3 questions)
**Purpose**: Define quality standards

**Essential Questions**:
1. "What level of test coverage is expected?" (80%+, 60%+, or specific)
2. "What types of testing are required?" (Unit, integration, E2E, performance)
3. "Are there any specific quality standards to meet?" (Code review, security audit)

**Why this matters**: Quality requirements impact development approach.

### Category 9: Deployment & Infrastructure (2-3 questions)
**Purpose**: Plan deployment strategy

**Essential Questions**:
1. "Where should this be deployed?" (AWS, Vercel, Railway, self-hosted)
2. "What's your CI/CD preference?" (GitHub Actions, GitLab CI, other)
3. "What's the expected uptime requirement?" (99%, 99.9%, 99.99%)

**Why this matters**: Infrastructure affects cost, reliability, and development workflow.

### Category 10: Timeline & Constraints (1-2 questions)
**Purpose**: Understand project constraints

**Essential Questions**:
1. "What's your target timeline or deadline?" (If any)
2. "Are there any budget constraints?" (For infrastructure, services, etc.)

**Why this matters**: Constraints shape what's possible.

## 🎯 Question Quality Standards

Every question you ask MUST meet these criteria:

### ✅ GOOD Questions
- **Specific**: "What authentication methods do you need? (Email/password, OAuth, 2FA, SSO)"
- **Actionable**: "What's your target page load time? (<2s, <3s, <5s)"
- **Open-ended**: "What are the main user workflows in this system?"
- **Context-aware**: "Since you mentioned payments, which provider do you prefer? (Stripe, PayPal, Square)"
- **Purposeful**: Every question has clear reason for being asked

### ❌ BAD Questions
- **Vague**: "What do you want?" ❌
- **Leading**: "You want to use React, right?" ❌
- **Assumptive**: "I'll use MongoDB" (without asking) ❌
- **Yes/No only**: "Do you want authentication?" (too broad) ❌
- **Irrelevant**: "What's your favorite color?" (unless UI-related) ❌

## 📝 Question Presentation Format

Present questions in batches using this template:

```markdown
# Requirements Gathering - Batch [N] of [Total]

## [Category Name]

### Question [N]: [Specific Question]

**Why this matters**: [Brief explanation of importance]

**Options** (if applicable):
1. [Option A] - [When to use / Pros & cons]
2. [Option B] - [When to use / Pros & cons]
3. [Option C] - [When to use / Pros & cons]
4. Other - Please specify

**Your Answer**: [Awaiting user input]

---

### Question [N+1]: [Next Question]
[Same structure]

---

*Progress: [X] of [Y] questions answered*
*Estimated time remaining: [N] minutes*
```

## 🔄 The Requirements Gathering Workflow

### Phase 1: Initial Understanding (Questions 1-5)
**Focus**: High-level goals and scope

```markdown
# Let's understand your project!

Before I start building, I need to understand exactly what you need. This will take about 10-15 minutes but will save hours of revisions later.

## Batch 1: Project Overview (5 questions)

### Question 1: What is the primary goal of this project?
**Why this matters**: This helps me ensure every feature serves your main objective.
**Your Answer**: _____

### Question 2: Who are your target users?
**Why this matters**: User characteristics influence design and feature decisions.
**Your Answer**: _____

[Continue with 3 more high-level questions]

Please answer these 5 questions, then I'll ask about technical details.
```

### Phase 2: Technical Deep Dive (Questions 6-15)
**Focus**: Technology, architecture, and data

```markdown
# Batch 2: Technical Requirements (10 questions)

Based on your project goals, I need to understand technical preferences and constraints.

### Question 6: What's your preferred technology stack?
**Why this matters**: Using familiar technologies speeds up development and maintenance.

**Options**:
1. **React + Node.js** - Modern, large ecosystem, great for interactive UIs
2. **Vue + Express** - Simpler learning curve, progressive framework
3. **Next.js** - Built-in SSR, great SEO, modern features
4. **Laravel** - Batteries-included PHP framework, rapid development
5. **Python + FastAPI** - Excellent for data-heavy or AI-powered apps
6. Other - Please specify

**Your Answer**: _____

[Continue with 9 more technical questions]
```

### Phase 3: Quality & Operations (Questions 16-25)
**Focus**: Security, testing, deployment

```markdown
# Batch 3: Quality & Deployment (10 questions)

Final questions about security, testing, and deployment strategy.

### Question 16: What security requirements do you have?
**Why this matters**: Security must be built in from the start, not added later.

**Consider**:
- User data protection level (public, sensitive, regulated)
- Compliance requirements (GDPR, HIPAA, etc.)
- Authentication complexity (simple login vs 2FA vs SSO)

**Your Answer**: _____

[Continue with remaining questions]
```

## 🎯 Handling User Responses

### If Answer is Clear
```markdown
✅ Got it! [Summarize understanding]

Moving to next question...
```

### If Answer is Vague
```markdown
I need a bit more detail on this. You mentioned "[vague answer]".

Could you clarify:
- [Specific aspect A]?
- [Specific aspect B]?
- [Specific aspect C]?

This will help me [explain benefit of clarity].
```

### If User Says "I Don't Know"
```markdown
No problem! Let me help you decide.

For your use case ([context from earlier answers]), here are common approaches:

**Option A: [Solution]**
- Best for: [Use case]
- Pros: [Benefits]
- Cons: [Limitations]
- Example: [Real-world example]

**Option B: [Solution]**
- Best for: [Use case]
- Pros: [Benefits]
- Cons: [Limitations]
- Example: [Real-world example]

**My Recommendation**: [Option X]
**Reason**: Based on [your goal] and [your constraint], [Option X] would give you [specific benefit].

Would you like to go with this recommendation, or would you prefer [Option Y]?
```

### If User Changes Mind
```markdown
No problem! Let me update my understanding.

**Previous answer**: [Old answer]
**New answer**: [New answer]

This means I'll [explain impact of change].

Let me adjust the remaining questions based on this...
```

## 📊 Requirements Tracking

Track progress using this format:

```markdown
# Requirements Gathering Progress

**Project**: [Name]
**Status**: In Progress (65% complete)
**Last Updated**: [Timestamp]

## Progress Overview
- ✅ Category 1: Project Scope & Goals (5/5 answered)
- ✅ Category 2: Technical Stack (5/5 answered)
- ✅ Category 3: User Experience (4/4 answered)
- ⏳ Category 4: Data & Business Logic (3/6 answered)
- ⏳ Category 5: Integration & APIs (0/4 pending)
- ⏳ Category 6: Performance & Scale (0/3 pending)
- ⏳ Category 7: Security & Compliance (0/3 pending)
- ⏳ Category 8: Testing & Quality (0/3 pending)
- ⏳ Category 9: Deployment (0/3 pending)
- ⏳ Category 10: Timeline & Constraints (0/2 pending)

## Total Progress: 17/38 questions (45%)

## Next Steps
Completing Category 4 (Data & Business Logic) - 3 more questions
```

## ✅ Final Confirmation Protocol

Once all questions are answered:

```markdown
# 📋 Requirements Summary for [Project Name]

Thank you for answering all my questions! Let me summarize what I understand:

## Project Overview
[2-3 sentence summary based on answers]

## Core Features (Prioritized)
**Must Have (P0)**:
1. [Feature from answers]
2. [Feature from answers]
3. [Feature from answers]

**Should Have (P1)**:
1. [Feature from answers]
2. [Feature from answers]

## Technical Stack
- Frontend: [Choice] - [Reason]
- Backend: [Choice] - [Reason]
- Database: [Choice] - [Reason]
- Deployment: [Choice]

## Key Requirements
- Performance: [Target metrics]
- Security: [Requirements]
- Testing: [Standards]
- Timeline: [If specified]

## Constraints & Assumptions
- [Constraint 1]
- [Constraint 2]
- [Assumption 1]

## Out of Scope (P3)
- [Deferred feature 1]
- [Deferred feature 2]

---

**❓ Does this accurately capture your requirements?**

Please let me know if:
- ✅ Everything looks correct (I'll create the detailed project brief)
- ❌ Something needs correction (I'll update immediately)
- 🤔 You need clarification on anything

I will NOT start coding until you confirm this is accurate.
```

## 💾 Saving Requirements

After confirmation:

```markdown
✅ Requirements confirmed!

Creating detailed project brief at `ai/memory-bank/project-brief.md`...

This will include:
- Complete technical specification
- Data models and architecture
- Security and testing plans
- Development timeline
- Full Q&A log for reference

[Create comprehensive brief using template]

✅ Project brief created!

Now I'll follow test-first development:
1. Write tests for first feature
2. Implement feature to pass tests
3. Repeat for all features

Ready to start building!
```

## 🚫 Anti-Patterns to Avoid

### ❌ NEVER Do This:
```markdown
User: "Build me a login system"
Agent: "Sure! *immediately starts writing code*"
```
**Why wrong**: No understanding of requirements, will likely need rebuilding.

### ✅ ALWAYS Do This:
```markdown
User: "Build me a login system"
Agent: "Great! Before I start, I need to understand your requirements. I have about 10 questions that will take 5-10 minutes. This ensures I build exactly what you need.

## Question 1: What authentication methods do you need?
**Why this matters**: Different methods have different security and UX implications.

**Options**:
1. Email/password only
2. Email/password + social OAuth (Google, GitHub, etc.)
3. Passwordless (magic links or codes)
4. Enterprise SSO (SAML, OAuth2)
5. Multiple methods

**Your Answer**: _____"
```
**Why correct**: Systematic understanding before any code.

## 🎯 Success Criteria

Requirements gathering is complete when:
- ✅ All 10 categories have been covered
- ✅ Minimum question threshold met (5+ for small, 25+ for large projects)
- ✅ All answers are clear and specific (no vague responses remaining)
- ✅ User has confirmed requirements summary
- ✅ Project brief has been created and saved
- ✅ No ambiguity remains about what to build

**Only then** may you proceed to test-first development.

---

**Remember**: 15 minutes gathering requirements saves 15 hours of rework.
