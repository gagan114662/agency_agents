# Question-Asking Protocol Tests

## Test Suite: Question Protocol Validation

### Test 1: Question Template Validation
```markdown
**Given**: Agent needs to ask a requirements question
**When**: Agent formulates the question
**Then**: Question MUST follow structured template

**Template Structure**:
```
## [Category]: [Specific Question]

**Why this matters**: [Brief explanation of why answer is important]

**Options** (if applicable):
1. [Option A with brief description]
2. [Option B with brief description]
3. [Other - please specify]

**Your Answer**: [Awaiting response]
```

**Test Cases**:
- ✅ Question has clear category label
- ✅ Question includes "why this matters" context
- ✅ Question provides options when appropriate
- ✅ Question is specific and actionable
```

### Test 2: Question Categories Are Comprehensive
```markdown
**Given**: A new project request
**When**: Agent generates question list
**Then**: ALL categories below MUST be covered

**Category 1: Project Scope & Goals**
Example Questions:
- "What is the primary goal of this project?"
- "Who are the target users/audience?"
- "What problem does this solve?"
- "How will success be measured?"
- "What are the must-have vs. nice-to-have features?"

**Category 2: Technical Stack & Architecture**
Example Questions:
- "Do you have a preferred technology stack? (e.g., React, Vue, Node.js, Python)"
- "Is this a web app, mobile app, desktop app, or API?"
- "What's your database preference? (SQL, NoSQL, both)"
- "Are there any specific libraries or frameworks you want to use?"
- "What's the expected system architecture? (Monolith, microservices, serverless)"

**Category 3: User Experience & Design**
Example Questions:
- "Do you have existing designs or wireframes?"
- "What's your preferred design style? (Minimal, modern, corporate, playful)"
- "What devices should be supported? (Desktop, tablet, mobile)"
- "Are there any accessibility requirements? (WCAG compliance level)"
- "What's the target user's technical proficiency?"

**Category 4: Data & Business Logic**
Example Questions:
- "What are the main data entities in the system?"
- "What are the key relationships between data?"
- "What business rules or validations are required?"
- "How should data be organized and structured?"
- "What are the expected data volumes?"

**Category 5: Integration & APIs**
Example Questions:
- "Do you need to integrate with any existing systems or APIs?"
- "Will this system expose APIs for other applications?"
- "What authentication/authorization is needed?"
- "Are there any third-party services to integrate? (Payment, email, etc.)"

**Category 6: Performance & Scale**
Example Questions:
- "How many concurrent users do you expect?"
- "What's the acceptable page load time?"
- "What's the expected data growth rate?"
- "Are there any specific performance requirements?"

**Category 7: Security & Compliance**
Example Questions:
- "What security level is required for this project?"
- "Are there any compliance requirements? (GDPR, HIPAA, PCI-DSS)"
- "What data needs to be encrypted?"
- "What are the authentication requirements?"

**Category 8: Testing & Quality**
Example Questions:
- "What level of test coverage is expected?"
- "What types of testing are required? (Unit, integration, E2E)"
- "Are there any specific quality standards to meet?"

**Category 9: Deployment & Infrastructure**
Example Questions:
- "Where will this be deployed? (Cloud provider, on-premise)"
- "What's your CI/CD preference?"
- "What's the expected uptime requirement?"
- "What's your infrastructure budget?"

**Category 10: Timeline & Constraints**
Example Questions:
- "What's your target timeline or deadline?"
- "Are there any budget constraints?"
- "Are there any technical constraints or limitations?"

**Test**: Agent asks at least 1 question from each relevant category
**Test**: Categories are asked in logical order
```

### Test 3: Dynamic Question Generation
```markdown
**Given**: User's initial project description
**When**: Agent analyzes the description
**Then**: Agent generates contextually relevant questions

**Example Input**: "I need a blog with user authentication"

**Expected Questions** (contextually relevant):
1. ✅ "What authentication methods do you want?" (relevant - auth mentioned)
2. ✅ "Should users be able to comment on posts?" (relevant - blog feature)
3. ✅ "Do you need an admin panel?" (relevant - content management)
4. ❌ "Do you need real-time chat?" (NOT relevant - not mentioned)

**Test**: Questions are relevant to user's stated needs
**Test**: Questions don't ask about obviously out-of-scope features
**Test**: Questions expand on mentioned features appropriately
```

### Test 4: Follow-Up Question Logic
```markdown
**Given**: User provides an answer to a question
**When**: Answer is vague or incomplete
**Then**: Agent MUST ask clarifying follow-up

**Scenario 1: Vague Tech Stack Answer**
Q: "What's your preferred tech stack?"
A: "Modern web technologies"

Expected Follow-up:
"Could you be more specific about 'modern web technologies'? For example:
- Frontend: React, Vue, Angular, Svelte, or vanilla JS?
- Backend: Node.js, Python, Ruby, PHP, Go, or Java?
- Database: PostgreSQL, MySQL, MongoDB, or other?
Having specific technologies will help me set up the optimal architecture."

**Scenario 2: Unclear User Flow**
Q: "What should happen after a user logs in?"
A: "They see their dashboard"

Expected Follow-up:
"What information should the dashboard display? For example:
- User profile summary?
- Recent activity or notifications?
- Key metrics or statistics?
- Quick actions or shortcuts?
- Other content?"

**Test**: Agent identifies vague answers
**Test**: Agent asks specific clarifying questions
**Test**: Agent provides examples to guide user
```

### Test 5: Question Progression Tracking
```markdown
**Given**: Requirements gathering session in progress
**When**: Agent asks questions
**Then**: Agent tracks which questions have been answered

**Tracking Structure**:
```markdown
# Requirements Gathering Progress

## Status: 12/25 questions answered (48%)

### ✅ Answered Questions (12)
1. [Category] Question text - Answer: [answer]
2. [Category] Question text - Answer: [answer]
...

### ⏳ Pending Questions (13)
1. [Category] Question text
2. [Category] Question text
...

### 🔄 Questions Needing Clarification (0)
(None currently)
```

**Test**: Agent maintains accurate count
**Test**: Agent marks questions as answered
**Test**: Agent identifies questions needing more info
**Test**: Agent shows progress percentage
```

### Test 6: Minimum Question Threshold
```markdown
**Given**: A project request of varying complexity
**When**: Agent determines question count
**Then**: Agent MUST ask minimum questions based on project size

**Project Complexity Thresholds**:

**Small Feature** (e.g., "Add a search bar"):
- Minimum: 5 questions
- Typical: 5-10 questions
- Categories: 3-5

**Medium Feature** (e.g., "Build authentication system"):
- Minimum: 10 questions
- Typical: 10-15 questions
- Categories: 5-7

**Large Feature** (e.g., "Build e-commerce checkout"):
- Minimum: 15 questions
- Typical: 15-25 questions
- Categories: 7-9

**Full Project** (e.g., "Build a SaaS application"):
- Minimum: 25 questions
- Typical: 25-40 questions
- Categories: 10

**Test**: Agent asks sufficient questions for complexity level
**Test**: Agent doesn't under-question complex projects
**Test**: Agent doesn't over-question simple features
```

### Test 7: Question Quality Validation
```markdown
**Given**: Agent has generated a list of questions
**When**: Validating question quality
**Then**: Each question MUST pass quality checks

**Quality Checks**:

**Check 1: Specificity**
❌ Bad: "What do you want?"
✅ Good: "What specific features should the user dashboard include?"

**Check 2: Actionability**
❌ Bad: "Should it be good?"
✅ Good: "What's your target page load time? (e.g., <2s, <3s, <5s)"

**Check 3: Non-Leading**
❌ Bad: "You want to use React, right?"
✅ Good: "What's your preferred frontend framework, if any?"

**Check 4: Purposeful**
❌ Bad: "What's your favorite color?" (irrelevant)
✅ Good: "What's your brand color palette for the UI?"

**Check 5: Open-Ended (when appropriate)**
❌ Bad: "Do you want users?" (too closed)
✅ Good: "Who are your target users and what are their main goals?"

**Test**: Each question passes all applicable checks
**Test**: No vague or leading questions
**Test**: All questions have clear purpose
```

### Test 8: Handling "I Don't Know" Answers
```markdown
**Given**: User responds with "I don't know" or "Not sure"
**When**: Agent receives this response
**Then**: Agent MUST provide helpful guidance

**Response Template**:
```
I understand [question topic] might not be clear yet. Let me help:

**Common Approaches**:
1. [Option A]: [When to use this] [Pros/cons]
2. [Option B]: [When to use this] [Pros/cons]
3. [Option C]: [When to use this] [Pros/cons]

**My Recommendation**:
For your use case ([brief context]), I'd suggest [Option X] because [reason].

Would you like to go with this recommendation, or would you prefer one of the other options?
```

**Test**: Agent doesn't leave user stuck
**Test**: Agent provides educated recommendations
**Test**: Agent explains trade-offs
**Test**: Agent still gets user to make a choice
```

### Test 9: Question Batch Sizing
```markdown
**Given**: Multiple questions to ask
**When**: Agent presents questions
**Then**: Agent MUST batch questions appropriately

**Batching Rules**:
- Present 5-7 questions at a time (not overwhelming)
- Group related questions together
- Allow user to answer batch before continuing
- Show progress after each batch

**Example Batch 1** (High-level):
```
# Questions 1-5: Project Overview

1. [Scope question]
2. [Goals question]
3. [Users question]
4. [Timeline question]
5. [Tech stack question]

Please answer these 5 questions, then I'll ask about specific technical details.
```

**Example Batch 2** (Technical):
```
# Questions 6-10: Technical Architecture

Based on your previous answers, I have some technical questions:

6. [Database question]
7. [API question]
8. [Authentication question]
9. [Performance question]
10. [Deployment question]

(5 more questions remaining after this batch)
```

**Test**: Questions presented in digestible batches
**Test**: Batches are thematically grouped
**Test**: Progress is communicated
**Test**: User isn't overwhelmed
```

### Test 10: Final Confirmation Protocol
```markdown
**Given**: All questions have been answered
**When**: Agent prepares final requirements
**Then**: Agent MUST follow confirmation protocol

**Confirmation Steps**:

1. **Compile Complete Requirements**
   - Create comprehensive requirements document
   - Include all Q&A pairs
   - Add derived requirements

2. **Present Summary**
   ```markdown
   # Requirements Summary

   Based on our discussion, here's what I understand:

   ## Project Overview
   [2-3 sentence summary]

   ## Core Features
   1. [Feature 1]
   2. [Feature 2]
   ...

   ## Technical Stack
   - Frontend: [stack]
   - Backend: [stack]
   - Database: [stack]

   ## Key Requirements
   - [Requirement 1]
   - [Requirement 2]
   ...

   ## Constraints
   - [Constraint 1]
   - [Constraint 2]
   ...
   ```

3. **Ask for Confirmation**
   "Does this accurately capture your requirements? Please let me know if anything needs correction or clarification."

4. **Handle Feedback**
   - If corrections → Update and re-present
   - If clarifications needed → Ask follow-ups
   - If confirmed → Proceed to implementation

5. **Save Requirements**
   - Save to `ai/memory-bank/requirements.md`
   - Include timestamp and status

**Test**: All steps are followed
**Test**: Summary is comprehensive
**Test**: User confirmation is obtained
**Test**: Requirements are persisted
```

## Integration Tests

### Integration Test 1: End-to-End Question Flow
```markdown
**Scenario**: User requests "Build a task management app"

**Expected Flow**:
1. Agent acknowledges request
2. Agent asks Batch 1 (5-7 questions) about project scope
3. User answers Batch 1
4. Agent asks Batch 2 (5-7 questions) about technical details
5. User answers Batch 2
6. Agent asks Batch 3 (remaining questions) about quality/deployment
7. User answers Batch 3
8. Agent presents requirements summary
9. Agent gets user confirmation
10. Agent proceeds to test-first development

**Test**: Complete flow executes correctly
**Test**: No premature coding
**Test**: All question categories covered
```

### Integration Test 2: Handling Course Corrections
```markdown
**Scenario**: User changes mind mid-questioning

**Flow**:
1. Agent asks tech stack question
2. User says "React"
3. Agent asks follow-up React questions
4. User says "Actually, I want to use Vue instead"
5. Agent acknowledges change
6. Agent asks appropriate Vue questions
7. Agent updates requirements document
8. Agent continues with correct context

**Test**: Agent handles changes gracefully
**Test**: Requirements stay consistent
**Test**: No contradictory assumptions
```

---

**Test Execution**: Manual validation + Agent behavior monitoring
**Pass Criteria**: All 10 tests + 2 integration tests pass
**Fail Fast**: Any critical violation (premature coding) = immediate fail
