# Git Workflow Tests

## Test Suite: Git Operations Validation

### Test 1: Verify Remote Branch Push (Not Local)
```markdown
**Given**: Agent executes git push command
**When**: Push operation completes
**Then**: Agent MUST verify push went to REMOTE repository, not just local

**Test Cases**:

#### Test 1.1: Check Remote Tracking
```bash
# After push, verify branch tracks remote
git branch -vv

# Expected output should show:
# * main abc1234 [origin/main] commit message
#              ^^^^^^^^^^^^^ THIS MUST BE PRESENT
```

**Expected**: Branch shows `[origin/main]` or `[origin/<branch-name>]`
**Failure**: Branch shows no remote tracking or just local reference

#### Test 1.2: Verify Remote Branch Exists
```bash
# Check remote branches
git branch -r

# Expected output:
# origin/main
# or origin/<branch-name>
```

**Expected**: Remote branch listed in `git branch -r`
**Failure**: Only local branches visible

#### Test 1.3: Confirm Commits on Remote
```bash
# Check if local HEAD matches remote HEAD
git log HEAD..origin/main

# Expected: Empty output (no difference)
# If there's output, local is ahead of remote = PUSH FAILED
```

**Expected**: No output (local and remote in sync)
**Failure**: Shows commits (local ahead of remote)

#### Test 1.4: Verify via GitHub API
```bash
# Optional: Fetch from remote to confirm
git fetch origin

# Check what was fetched
git log --oneline --graph --all -n 5
```

**Expected**: Remote branches visible and up-to-date
**Failure**: Cannot fetch or remote is behind

---

### Automated Verification Commands

**After Every Push, Agent MUST Run**:
```bash
# 1. Verify remote tracking
echo "=== Checking Remote Tracking ==="
git branch -vv | grep -E '\[origin/'

# 2. Verify remote branch exists
echo "=== Checking Remote Branches ==="
git branch -r | grep "origin/$(git branch --show-current)"

# 3. Verify sync status
echo "=== Checking Sync Status ==="
BEHIND=$(git rev-list HEAD..origin/$(git branch --show-current) --count)
AHEAD=$(git rev-list origin/$(git branch --show-current)..HEAD --count)

if [ "$AHEAD" -eq 0 ] && [ "$BEHIND" -eq 0 ]; then
  echo "✅ PASS: Local and remote are in sync"
  exit 0
else
  echo "❌ FAIL: Local ahead by $AHEAD, behind by $BEHIND"
  exit 1
fi
```

**Pass Criteria**:
- ✅ Remote tracking confirmed
- ✅ Remote branch exists
- ✅ Local and remote in sync (ahead=0, behind=0)
- ✅ Can fetch from remote successfully

**Fail Criteria**:
- ❌ No remote tracking
- ❌ Remote branch doesn't exist
- ❌ Local ahead of remote (commits not pushed)
- ❌ Cannot fetch from remote
```

### Test 2: Remove Unnecessary Files Before Commit
```markdown
**Given**: Agent is preparing to commit code
**When**: Before running `git add` or `git commit`
**Then**: Agent MUST remove all unnecessary files first

**Unnecessary Files to Remove**:

#### Category 1: Development/Build Artifacts
```bash
# Files that should NEVER be committed:
node_modules/           # Node.js dependencies
__pycache__/           # Python bytecode
*.pyc                  # Python compiled files
.pytest_cache/         # Pytest cache
.coverage              # Coverage reports
dist/                  # Build distributions
build/                 # Build outputs
*.egg-info/            # Python package info
.venv/                 # Virtual environments
venv/                  # Virtual environments
env/                   # Virtual environments
.DS_Store              # macOS metadata
Thumbs.db              # Windows metadata
.idea/                 # JetBrains IDEs
.vscode/               # VS Code settings (unless project-specific)
*.swp                  # Vim swap files
*.swo                  # Vim swap files
```

#### Category 2: Temporary/Cache Files
```bash
*.tmp
*.temp
*.log                  # Log files (unless needed)
*.cache
.cache/
tmp/
temp/
*.bak                  # Backup files
*~                     # Editor backups
```

#### Category 3: Environment/Secret Files
```bash
.env                   # Environment variables
.env.local             # Local environment
.env.*.local           # Environment files
*.key                  # Private keys
*.pem                  # Certificates
credentials.json       # Credentials
secrets.yaml           # Secrets
config.local.*         # Local configs
```

#### Category 4: IDE/Editor Specific
```bash
.idea/                 # IntelliJ IDEA
.vscode/               # VS Code (unless project settings)
*.sublime-*            # Sublime Text
.project               # Eclipse
.classpath             # Eclipse
.settings/             # Eclipse
```

---

### Test Implementation

#### Test 2.1: Pre-Commit File Scan
```bash
# Before git add, scan for unnecessary files
echo "=== Scanning for Unnecessary Files ==="

UNNECESSARY_PATTERNS=(
  "node_modules"
  "__pycache__"
  "*.pyc"
  ".pytest_cache"
  "dist/"
  "build/"
  "*.egg-info"
  ".venv"
  "venv"
  ".DS_Store"
  ".env"
  "*.log"
  "*.tmp"
  ".idea"
  ".vscode"
)

FOUND_FILES=()

for pattern in "${UNNECESSARY_PATTERNS[@]}"; do
  files=$(find . -name "$pattern" -not -path "./.git/*" 2>/dev/null)
  if [ -n "$files" ]; then
    FOUND_FILES+=("$pattern: $files")
  fi
done

if [ ${#FOUND_FILES[@]} -gt 0 ]; then
  echo "❌ FAIL: Found unnecessary files:"
  printf '%s\n' "${FOUND_FILES[@]}"
  exit 1
else
  echo "✅ PASS: No unnecessary files found"
  exit 0
fi
```

#### Test 2.2: Verify .gitignore Exists
```bash
# Ensure .gitignore exists and is comprehensive
if [ ! -f .gitignore ]; then
  echo "❌ FAIL: .gitignore does not exist"
  exit 1
fi

# Check for essential ignore patterns
REQUIRED_PATTERNS=(
  "node_modules"
  "__pycache__"
  ".env"
  ".DS_Store"
  "dist"
  "build"
)

MISSING=()
for pattern in "${REQUIRED_PATTERNS[@]}"; do
  if ! grep -q "$pattern" .gitignore; then
    MISSING+=("$pattern")
  fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
  echo "❌ FAIL: .gitignore missing patterns:"
  printf '%s\n' "${MISSING[@]}"
  exit 1
else
  echo "✅ PASS: .gitignore is comprehensive"
  exit 0
fi
```

#### Test 2.3: Clean Before Commit
```bash
# Automated cleanup script
echo "=== Cleaning Unnecessary Files ==="

# Remove build artifacts
rm -rf node_modules __pycache__ .pytest_cache dist build *.egg-info

# Remove environment files (keep .env.example)
find . -name ".env" -not -name ".env.example" -delete

# Remove cache files
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete
find . -name "*.tmp" -delete
find . -name "*.log" -delete
find . -name ".DS_Store" -delete

# Remove IDE files
rm -rf .idea .vscode

echo "✅ Cleanup complete"
```

**Pass Criteria**:
- ✅ No node_modules/ or equivalent dependency directories
- ✅ No __pycache__/ or .pyc files
- ✅ No .env or credential files
- ✅ No build/dist artifacts
- ✅ .gitignore exists and is comprehensive
- ✅ Only source code and necessary config files remain

**Fail Criteria**:
- ❌ Any unnecessary files found in working directory
- ❌ .gitignore missing or incomplete
- ❌ Attempting to commit ignored files
```

### Test 3: Ensure Requirements File Exists
```markdown
**Given**: A project repository with dependencies
**When**: Before committing or deploying
**Then**: Agent MUST ensure appropriate requirements file exists

**Requirements Files by Language/Framework**:

#### For Python Projects
**Required**: `requirements.txt` or `pyproject.toml` or `Pipfile`

#### For Node.js Projects
**Required**: `package.json` with `dependencies` section

#### For PHP Projects
**Required**: `composer.json`

#### For Ruby Projects
**Required**: `Gemfile`

#### For Go Projects
**Required**: `go.mod`

#### For Rust Projects
**Required**: `Cargo.toml`

---

### Test Implementation

#### Test 3.1: Detect Project Type and Verify Requirements File
```bash
#!/bin/bash

echo "=== Checking Requirements Files ==="

# Detect project type and check for requirements file
PROJECT_TYPE=""
REQUIREMENTS_FILE=""
MISSING=false

# Python
if ls *.py &>/dev/null || [ -d "src" ] && ls src/*.py &>/dev/null; then
  PROJECT_TYPE="Python"
  if [ -f "requirements.txt" ]; then
    REQUIREMENTS_FILE="requirements.txt"
  elif [ -f "pyproject.toml" ]; then
    REQUIREMENTS_FILE="pyproject.toml"
  elif [ -f "Pipfile" ]; then
    REQUIREMENTS_FILE="Pipfile"
  else
    MISSING=true
  fi
fi

# Node.js
if [ -f "package.json" ] || ls *.js &>/dev/null || ls *.ts &>/dev/null; then
  PROJECT_TYPE="Node.js"
  if [ -f "package.json" ]; then
    REQUIREMENTS_FILE="package.json"
  else
    MISSING=true
  fi
fi

# PHP
if ls *.php &>/dev/null; then
  PROJECT_TYPE="PHP"
  if [ -f "composer.json" ]; then
    REQUIREMENTS_FILE="composer.json"
  else
    MISSING=true
  fi
fi

# Go
if ls *.go &>/dev/null; then
  PROJECT_TYPE="Go"
  if [ -f "go.mod" ]; then
    REQUIREMENTS_FILE="go.mod"
  else
    MISSING=true
  fi
fi

# Results
if [ "$MISSING" = true ]; then
  echo "❌ FAIL: $PROJECT_TYPE project missing requirements file"
  echo "Expected one of: $(get_expected_files $PROJECT_TYPE)"
  exit 1
elif [ -n "$REQUIREMENTS_FILE" ]; then
  echo "✅ PASS: Found $REQUIREMENTS_FILE for $PROJECT_TYPE project"
  exit 0
else
  echo "⚠️  WARN: Could not detect project type or no code files found"
  exit 0
fi
```

#### Test 3.2: Validate Requirements File Content
```bash
# For Python requirements.txt
if [ -f "requirements.txt" ]; then
  echo "=== Validating requirements.txt ==="

  # Check file is not empty
  if [ ! -s "requirements.txt" ]; then
    echo "❌ FAIL: requirements.txt is empty"
    exit 1
  fi

  # Check for valid format (package==version or package>=version)
  if ! grep -qE '^[a-zA-Z0-9_-]+(==|>=|<=|~=|>|<)[0-9]' requirements.txt; then
    echo "⚠️  WARN: requirements.txt may not have pinned versions"
  fi

  echo "✅ PASS: requirements.txt is valid"
fi

# For package.json
if [ -f "package.json" ]; then
  echo "=== Validating package.json ==="

  # Check valid JSON
  if ! python3 -m json.tool package.json > /dev/null 2>&1; then
    echo "❌ FAIL: package.json is not valid JSON"
    exit 1
  fi

  # Check has dependencies or devDependencies
  if ! grep -q '"dependencies"' package.json && ! grep -q '"devDependencies"' package.json; then
    echo "⚠️  WARN: package.json has no dependencies listed"
  fi

  echo "✅ PASS: package.json is valid"
fi
```

#### Test 3.3: Check All Import Statements Have Corresponding Dependencies
```bash
# For Python projects
if [ -f "requirements.txt" ]; then
  echo "=== Checking Python imports vs requirements ==="

  # Extract imports from Python files
  IMPORTS=$(find . -name "*.py" -exec grep -h "^import \|^from " {} \; | \
            sed 's/import //g' | sed 's/from //g' | awk '{print $1}' | \
            sort -u | grep -v "^\.")

  # Extract packages from requirements.txt
  PACKAGES=$(cat requirements.txt | sed 's/==.*//' | sed 's/>=.*//' | \
             sed 's/<=.*//' | sed 's/~=.*//' | sort -u)

  MISSING_DEPS=()
  for import in $IMPORTS; do
    # Check if import is in standard library or requirements
    if ! python3 -c "import $import" 2>/dev/null && \
       ! echo "$PACKAGES" | grep -qi "^$import\$"; then
      MISSING_DEPS+=("$import")
    fi
  done

  if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo "❌ FAIL: Imports found but not in requirements.txt:"
    printf '%s\n' "${MISSING_DEPS[@]}"
    exit 1
  else
    echo "✅ PASS: All imports have corresponding dependencies"
  fi
fi
```

**Pass Criteria**:
- ✅ Appropriate requirements file exists for project type
- ✅ Requirements file is not empty
- ✅ Requirements file is valid format
- ✅ All imported modules are in requirements file
- ✅ Version pins are specified (best practice)

**Fail Criteria**:
- ❌ No requirements file exists for detected project type
- ❌ Requirements file is empty
- ❌ Requirements file has invalid syntax
- ❌ Imports used but not listed in requirements
```

### Test 4: Validate Authentication Necessity
```markdown
**Given**: Agent is implementing a new project or feature
**When**: Before implementing registration/authentication
**Then**: Agent MUST validate if auth is actually needed

**Critical Questions to Ask**:

1. "Does this project handle user-specific data?"
   - If NO → Auth likely not needed
   - If YES → Continue questioning

2. "Do users need individual accounts with personalized content?"
   - If NO → Auth likely not needed
   - If YES → Continue questioning

3. "Is there any sensitive or private information?"
   - If NO → Auth likely not needed
   - If YES → Auth needed

4. "Can the app function as a public/anonymous service?"
   - If YES → Auth likely not needed
   - If NO → Auth needed

5. "Are there different permission levels or roles?"
   - If NO → Auth might not be needed
   - If YES → Auth needed

---

### Test Implementation

#### Test 4.1: Authentication Necessity Questionnaire
```markdown
# Authentication Necessity Checklist

## Project: [Project Name]

### Critical Questions:

**Q1: Does this application handle user-specific data?**
- [ ] Yes - Users have personal data that belongs to them
- [ ] No - All data is public or shared

**Q2: Do users need individual accounts?**
- [ ] Yes - Each user needs their own account
- [ ] No - Single shared experience for all users

**Q3: Is there any sensitive or private information?**
- [ ] Yes - Contains PII, financial, health, or confidential data
- [ ] No - All information is public

**Q4: Can the app work as a public/anonymous service?**
- [ ] Yes - Anyone can use it without logging in
- [ ] No - Must identify users to function

**Q5: Are there different permission levels?**
- [ ] Yes - Admin, moderator, user roles needed
- [ ] No - Everyone has same permissions

**Q6: Does the app need to track user actions over time?**
- [ ] Yes - History, preferences, progress tracking
- [ ] No - Each session is independent

**Q7: Do users need to save their work/state?**
- [ ] Yes - Must persist data between sessions
- [ ] No - Stateless, no data persistence needed

**Q8: Are there any compliance requirements (GDPR, HIPAA, etc.)?**
- [ ] Yes - Legal requirements for user identification
- [ ] No - No compliance requirements

---

## Scoring:

**YES answers: [Count]**

### 0-2 YES answers:
**Verdict**: ❌ Authentication NOT needed
**Reason**: App can function without user accounts
**Alternative**: Use session storage, localStorage, or cookies for temporary state

### 3-4 YES answers:
**Verdict**: ⚠️ Authentication OPTIONAL
**Reason**: Could work without auth, but auth would add value
**Recommendation**: Start without auth, add later if needed
**Alternative**: "Guest mode" with optional account creation

### 5+ YES answers:
**Verdict**: ✅ Authentication REQUIRED
**Reason**: Core functionality depends on user identification
**Recommendation**: Implement authentication from the start

---

## Example Use Cases

### ❌ Auth NOT Needed:
- **Static Blog**: Public content, no user interaction
- **Calculator App**: Stateless, no data persistence
- **Public API Documentation**: Read-only, no personalization
- **Weather App**: Public data, no user-specific features
- **Timer/Stopwatch**: No data persistence needed

### ⚠️ Auth OPTIONAL:
- **Todo List**: Could use localStorage, but sync is nice-to-have
- **Recipe App**: Can browse publicly, but saved recipes need auth
- **News Reader**: Public articles, but bookmarks/preferences benefit from auth

### ✅ Auth REQUIRED:
- **Banking App**: Financial data, high security
- **Social Network**: User profiles, connections, private messages
- **E-commerce**: Orders, payment methods, shipping addresses
- **Healthcare Portal**: Medical records, HIPAA compliance
- **Team Collaboration Tool**: Permissions, private workspaces

---

## Agent Decision Tree

```
START
  ↓
  Q: User-specific data?
  ├─ NO → SKIP AUTH ❌
  └─ YES
      ↓
      Q: Sensitive/Private info?
      ├─ YES → AUTH REQUIRED ✅
      └─ NO
          ↓
          Q: Need persistence?
          ├─ NO → SKIP AUTH ❌
          └─ YES
              ↓
              Q: Can use localStorage?
              ├─ YES → SKIP AUTH ❌ (use local storage)
              └─ NO → AUTH REQUIRED ✅
```
```

#### Test 4.2: Validate Agent Asks Before Implementing Auth
```markdown
**Test Scenario**: User requests "Build a todo app"

**Expected Agent Behavior**:
```
Agent: "Before I implement this todo app, I need to understand the authentication requirements:

1. Do users need individual accounts, or can todos be stored locally in the browser?
2. Should todos sync across devices?
3. Is there any sensitive information in the todos?
4. Do you need to share todos with other users?

Based on your answers, I'll determine if authentication is necessary or if we can use a simpler approach like localStorage."
```

**Test Assertion**:
- ✅ PASS: Agent asks about auth necessity BEFORE implementing
- ❌ FAIL: Agent implements auth without questioning

---

**Test Scenario**: User requests "Build a public blog"

**Expected Agent Behavior**:
```
Agent: "For a public blog, authentication is typically NOT needed for readers. However, I should ask:

1. Do you need an admin panel to create/edit posts?
2. Will there be multiple authors with different permissions?
3. Do readers need accounts to comment?

If answers are NO, we can skip authentication entirely.
If YES to any, we'll implement auth only for those specific features."
```

**Test Assertion**:
- ✅ PASS: Agent questions auth necessity
- ✅ PASS: Agent suggests alternatives (public + optional admin)
- ❌ FAIL: Agent assumes auth is needed

---

**Test Scenario**: User requests "Build a banking dashboard"

**Expected Agent Behavior**:
```
Agent: "A banking dashboard absolutely REQUIRES authentication because:

1. Financial data is highly sensitive
2. PCI-DSS compliance mandates user authentication
3. User-specific account information must be protected
4. Audit trails require user identification

I'll implement secure authentication with:
- Multi-factor authentication (2FA)
- Session management
- Audit logging
- Password policies

This is non-negotiable for financial applications."
```

**Test Assertion**:
- ✅ PASS: Agent correctly identifies auth as required
- ✅ PASS: Agent explains security reasoning
- ✅ PASS: Agent plans appropriate security measures
```

#### Test 4.3: Auth Implementation Checklist
```markdown
**If Agent Determines Auth IS Needed**:

Agent MUST create this section in project brief:

## Authentication Requirements

**Auth Verdict**: ✅ Required
**Reasoning**: [Specific reasons from questionnaire]

**Auth Features Needed**:
- [ ] User registration
- [ ] Email verification
- [ ] Login/logout
- [ ] Password reset
- [ ] Session management
- [ ] Multi-factor authentication (if high security)
- [ ] OAuth/Social login (if requested)
- [ ] Role-based access control (if multiple roles)

**Security Measures**:
- [ ] Password hashing (bcrypt/argon2)
- [ ] HTTPS/TLS required
- [ ] CSRF protection
- [ ] Rate limiting on auth endpoints
- [ ] Account lockout after failed attempts
- [ ] Secure session storage

**Compliance Requirements**:
- [ ] GDPR (if EU users)
- [ ] HIPAA (if healthcare)
- [ ] PCI-DSS (if payment data)
- [ ] Other: [specify]

---

**If Agent Determines Auth is NOT Needed**:

Agent MUST document this:

## Authentication Decision

**Auth Verdict**: ❌ Not Required
**Reasoning**: [Specific reasons - e.g., "App uses localStorage, no sensitive data, public access only"]

**Alternative Approach**:
- Using: [localStorage / sessionStorage / cookies / none]
- Data persistence: [Browser storage / None]
- User identification: [Not needed / Session ID only]

**Future Considerations**:
- If user growth requires sync: Add optional auth later
- If features become user-specific: Revisit auth necessity
- No premature optimization: Start simple, add auth when needed
```

**Pass Criteria**:
- ✅ Agent asks authentication necessity questions
- ✅ Agent provides reasoning for decision
- ✅ Agent suggests alternatives when auth not needed
- ✅ Agent documents decision in project brief
- ✅ Agent implements appropriate security if auth is needed

**Fail Criteria**:
- ❌ Agent implements auth without questioning necessity
- ❌ Agent adds auth to projects that don't need it
- ❌ Agent skips auth when it's actually required
- ❌ Agent doesn't document auth decision
```

---

## Integration Test: Complete Git Workflow

### End-to-End Test Scenario
```bash
#!/bin/bash

echo "=== Running Complete Git Workflow Tests ==="

# Test 1: Verify Remote Push
echo "
[TEST 1] Verifying Remote Push..."
git branch -vv | grep -q '\[origin/' && echo "✅ Remote tracking confirmed" || echo "❌ No remote tracking"

# Test 2: Clean Unnecessary Files
echo "
[TEST 2] Cleaning Unnecessary Files..."
rm -rf node_modules __pycache__ .DS_Store .env dist build
echo "✅ Cleanup complete"

# Test 3: Check Requirements File
echo "
[TEST 3] Checking Requirements File..."
if [ -f "requirements.txt" ] || [ -f "package.json" ] || [ -f "composer.json" ]; then
  echo "✅ Requirements file found"
else
  echo "❌ No requirements file found"
fi

# Test 4: Validate Auth Necessity
echo "
[TEST 4] Validating Auth Necessity..."
if grep -rq "register\|login\|authentication" .; then
  echo "⚠️  Auth code found - verify necessity was checked in project brief"
  if [ -f "ai/memory-bank/project-brief.md" ]; then
    if grep -q "Authentication" ai/memory-bank/project-brief.md; then
      echo "✅ Auth decision documented"
    else
      echo "❌ Auth not documented in project brief"
    fi
  fi
else
  echo "✅ No auth code found"
fi

echo "
=== All Tests Complete ==="
```

**All 4 Tests Must Pass Before Push**

---

## Test Execution Frequency

**When to Run These Tests**:
1. Before EVERY git commit
2. Before EVERY git push
3. As part of CI/CD pipeline
4. During project setup phase
5. After adding new dependencies

**Automated Integration**:
Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
# Run all git workflow tests
~/.claude/agents/tests/run_git_workflow_tests.sh
```
