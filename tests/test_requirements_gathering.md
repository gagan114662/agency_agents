# Requirements Gathering Agent Tests

## Test Suite: Requirements Gathering Protocol

### Test 1: Agent Should Ask Questions Before Coding
```markdown
**Given**: User requests a new feature or project
**When**: Engineering agent receives the request
**Then**: Agent MUST ask clarifying questions before writing any code

**Expected Behavior**:
- Agent identifies gaps in requirements
- Agent asks minimum 5-10 questions for small features
- Agent asks 15-25+ questions for full projects
- Agent does NOT write code until questions are answered
```

### Test 2: Question Categories Coverage
```markdown
**Given**: A project request without complete details
**When**: Agent begins requirements gathering
**Then**: Agent MUST cover ALL essential question categories:

**Required Categories**:
1. Project Scope & Goals (2-5 questions)
2. Technical Stack & Architecture (3-5 questions)
3. User Experience & Design (2-4 questions)
4. Data & Business Logic (3-6 questions)
5. Integration & APIs (2-4 questions)
6. Performance & Scale (2-3 questions)
7. Security & Compliance (2-3 questions)
8. Testing & Quality (2-3 questions)
9. Deployment & Infrastructure (2-3 questions)
10. Timeline & Constraints (1-2 questions)

**Expected**: Each category has at least the minimum questions asked
```

### Test 3: Question Quality Standards
```markdown
**Given**: Agent is asking requirements questions
**When**: Agent formulates each question
**Then**: Each question MUST meet quality criteria:

**Quality Criteria**:
- ✅ Specific and actionable
- ✅ Open-ended (not yes/no unless necessary)
- ✅ Reveals user intent and preferences
- ✅ Uncovers technical constraints
- ✅ Identifies edge cases and error scenarios

**Anti-patterns to avoid**:
- ❌ Vague questions ("What do you want?")
- ❌ Assumptive questions (assuming tech stack)
- ❌ Leading questions (suggesting specific solutions)
- ❌ Redundant questions (asking same thing differently)
```

### Test 4: Progressive Questioning Strategy
```markdown
**Given**: User provides initial project description
**When**: Agent asks questions
**Then**: Questions should follow logical progression:

**Phase 1 - High-Level Understanding** (Questions 1-5):
- Project purpose and goals
- Primary users and use cases
- Success criteria

**Phase 2 - Technical Details** (Questions 6-15):
- Technology preferences
- Existing systems/constraints
- Data models and business logic
- Integration requirements

**Phase 3 - Quality & Constraints** (Questions 16-25):
- Performance requirements
- Security needs
- Testing approach
- Deployment strategy
- Timeline and budget

**Expected**: Questions build on previous answers
**Expected**: Later questions reference earlier context
```

### Test 5: Handling Incomplete Answers
```markdown
**Given**: User provides vague or incomplete answer
**When**: Agent receives the answer
**Then**: Agent MUST ask follow-up questions to clarify

**Example Scenario**:
User: "I need a user authentication system"
Agent asks: "What authentication methods?"
User: "Standard ones"

**Expected Behavior**:
Agent asks follow-up: "By 'standard', do you mean:
1. Email/password with password reset?
2. Social OAuth (Google, GitHub, etc.)?
3. Multi-factor authentication (2FA)?
4. Single Sign-On (SSO) with existing system?
Please specify which methods you need."

**Test**: Agent does NOT proceed with assumptions
```

### Test 6: Requirements Summary Before Coding
```markdown
**Given**: All questions have been answered
**When**: Agent prepares to start coding
**Then**: Agent MUST create and confirm requirements summary

**Summary Must Include**:
1. Project Overview (2-3 sentences)
2. Core Features List (prioritized)
3. Technical Stack Decisions
4. Key Constraints & Requirements
5. Success Metrics
6. Out of Scope Items

**Expected**: Agent asks "Does this summary match your expectations? Any corrections?"
**Expected**: Agent waits for confirmation before coding
```

### Test 7: Question Persistence
```markdown
**Given**: Requirements gathering session
**When**: Agent asks questions and receives answers
**Then**: All Q&A should be saved to project memory

**Expected Storage Location**: `ai/memory-bank/requirements.md`
**Expected Format**:
```markdown
# Project Requirements - [Project Name]
Date: [Date]
Status: [Gathering/Complete]

## Questions & Answers

### Q1: [Question]
**A**: [Answer]
**Follow-up**: [If any]

### Q2: [Question]
**A**: [Answer]
```

**Test**: File exists after questioning phase
**Test**: All questions and answers are recorded
```

### Test 8: No Premature Coding
```markdown
**Given**: User asks for a feature
**When**: Less than 5 critical questions have been answered
**Then**: Agent MUST NOT generate any implementation code

**Critical Questions** (minimum required):
1. What is the exact goal/outcome?
2. Who are the users and what's their workflow?
3. What's the preferred tech stack?
4. What are the key data/entities involved?
5. What are the main edge cases or error scenarios?

**Test Cases**:
- ✅ Agent refuses to code with 0 questions answered
- ✅ Agent refuses to code with 1-4 questions answered
- ✅ Agent proceeds only after 5+ critical questions answered
```

### Test 9: Technical Constraint Discovery
```markdown
**Given**: A project request
**When**: Agent asks technical questions
**Then**: Agent MUST uncover all technical constraints

**Required Constraint Questions**:
1. "What's your target deployment environment?" (Cloud/On-premise/Hybrid)
2. "What's the expected user load?" (Users, requests/sec, data volume)
3. "Are there any existing systems to integrate with?"
4. "What's your database preference?" (SQL/NoSQL/Both)
5. "What are your browser/device support requirements?"
6. "Are there any compliance requirements?" (GDPR, HIPAA, SOC2, etc.)
7. "What's the acceptable response time?" (Performance SLA)
8. "What's your budget for infrastructure?" (Cost constraints)

**Expected**: Agent asks ALL applicable constraint questions
```

### Test 10: User Confirmation Checkpoint
```markdown
**Given**: Requirements gathering is complete
**When**: Agent presents final requirements summary
**Then**: Agent MUST get explicit user confirmation

**Confirmation Process**:
1. Present complete requirements document
2. Ask: "Please review these requirements. Are they accurate?"
3. Wait for user response
4. If user says "yes" → Proceed to coding
5. If user says "no" or has corrections → Update requirements and re-confirm

**Test**: Agent does NOT start coding without explicit "yes" or "confirmed"
**Test**: Agent handles corrections gracefully
**Test**: Agent re-confirms after any corrections
```

## Test Execution Criteria

### Pass Criteria
- ✅ All 10 test scenarios pass
- ✅ Agent asks minimum required questions
- ✅ Agent covers all question categories
- ✅ Agent creates requirements document
- ✅ Agent gets user confirmation
- ✅ Agent does NOT code prematurely

### Fail Criteria
- ❌ Agent writes code before asking questions
- ❌ Agent skips critical question categories
- ❌ Agent proceeds with assumptions
- ❌ Agent doesn't create requirements summary
- ❌ Agent doesn't get user confirmation

## Integration Test Scenarios

### Scenario A: Complete Happy Path
```
1. User: "Build me a todo app"
2. Agent: Asks 15-20 questions covering all categories
3. User: Answers all questions
4. Agent: Creates requirements summary
5. Agent: Gets user confirmation
6. Agent: Writes tests first
7. Agent: Implements features
Result: ✅ PASS
```

### Scenario B: Incomplete Information
```
1. User: "Build something cool"
2. Agent: Asks clarifying questions
3. User: Gives vague answers
4. Agent: Asks follow-up questions
5. User: Provides better details
6. Agent: Confirms understanding
7. Agent: Proceeds with clear requirements
Result: ✅ PASS
```

### Scenario C: Premature Coding Attempt (Should Fail)
```
1. User: "Build a login system"
2. Agent: Immediately writes code WITHOUT asking questions
Result: ❌ FAIL - Agent violated requirements gathering protocol
```

---

**Test Framework**: Manual behavioral testing + Documentation validation
**Test Frequency**: Every agent update that touches requirements gathering
**Success Metric**: 100% pass rate on all 10 test scenarios
