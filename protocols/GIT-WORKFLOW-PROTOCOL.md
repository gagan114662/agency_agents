# Git Workflow Protocol

## 🚨 MANDATORY: Pre-Commit and Pre-Push Checklist

Before EVERY git commit and push, you MUST complete ALL 4 checks in this protocol.

---

## Feature 1: Verify Remote Branch Push (Not Local)

### The Problem
Agents sometimes say "pushed to GitHub" but only committed locally. This is UNACCEPTABLE.

### The Solution
ALWAYS verify push went to REMOTE repository, not just local.

### MANDATORY Verification Commands

After EVERY `git push`, run these commands:

```bash
#!/bin/bash

echo "=== Verifying Remote Push ==="

# 1. Check remote tracking
echo "
[1/4] Checking remote tracking..."
BRANCH=$(git branch --show-current)
TRACKING=$(git branch -vv | grep "^\* $BRANCH" | grep -o '\[origin/[^]]*\]')

if [ -n "$TRACKING" ]; then
  echo "✅ PASS: Branch tracks $TRACKING"
else
  echo "❌ FAIL: Branch does NOT track remote"
  exit 1
fi

# 2. Verify remote branch exists
echo "
[2/4] Verifying remote branch exists..."
if git branch -r | grep -q "origin/$BRANCH"; then
  echo "✅ PASS: Remote branch origin/$BRANCH exists"
else
  echo "❌ FAIL: Remote branch origin/$BRANCH does NOT exist"
  exit 1
fi

# 3. Check sync status (local vs remote)
echo "
[3/4] Checking sync status..."
git fetch origin --quiet

AHEAD=$(git rev-list origin/$BRANCH..$BRANCH --count 2>/dev/null || echo "0")
BEHIND=$(git rev-list $BRANCH..origin/$BRANCH --count 2>/dev/null || echo "0")

echo "Local ahead by: $AHEAD commits"
echo "Local behind by: $BEHIND commits"

if [ "$AHEAD" -eq 0 ] && [ "$BEHIND" -eq 0 ]; then
  echo "✅ PASS: Local and remote are in perfect sync"
elif [ "$AHEAD" -gt 0 ]; then
  echo "❌ FAIL: Local is ahead by $AHEAD commits - PUSH DID NOT COMPLETE"
  exit 1
elif [ "$BEHIND" -gt 0 ]; then
  echo "⚠️  WARN: Local is behind by $BEHIND commits - need to pull"
  exit 1
fi

# 4. Verify latest commit is on remote
echo "
[4/4] Verifying latest commit is on remote..."
LOCAL_SHA=$(git rev-parse HEAD)
REMOTE_SHA=$(git rev-parse origin/$BRANCH)

if [ "$LOCAL_SHA" = "$REMOTE_SHA" ]; then
  echo "✅ PASS: Latest commit $LOCAL_SHA is on remote"
else
  echo "❌ FAIL: Local SHA ($LOCAL_SHA) != Remote SHA ($REMOTE_SHA)"
  exit 1
fi

echo "
========================================
✅ ALL CHECKS PASSED
✅ Code is successfully pushed to remote
✅ GitHub repository is up-to-date
========================================"
```

### Usage in Agent Workflow

**After `git push origin main`**:
```bash
# DON'T just say "pushed to GitHub"
# VERIFY IT ACTUALLY HAPPENED

# Run verification script
bash verify_remote_push.sh

# If script exits 0 (success):
echo "✅ Confirmed: Changes pushed to GitHub repository"

# If script exits 1 (failure):
echo "❌ ERROR: Push to remote failed, retrying..."
git push origin main --verbose
```

### What to Report to User

**GOOD** ✅:
```
✅ Changes committed and pushed to GitHub
✅ Verification: Remote branch origin/main is up-to-date
✅ Latest commit abc123 confirmed on remote
```

**BAD** ❌:
```
"Pushed to GitHub"  ← NO VERIFICATION!
```

---

## Feature 2: Remove Unnecessary Files Before Commit

### The Problem
Committing node_modules, __pycache__, .env files, and other junk pollutes the repository.

### The Solution
ALWAYS clean unnecessary files BEFORE `git add`.

### File Categories to Remove

#### 1. Dependencies (NEVER commit these)
```bash
node_modules/           # Node.js packages
vendor/                 # PHP packages
__pycache__/           # Python bytecode
*.pyc, *.pyo           # Python compiled
.pytest_cache/         # Test cache
.coverage              # Coverage data
*.egg-info/            # Python package info
```

#### 2. Virtual Environments
```bash
venv/
.venv/
env/
.env/
virtualenv/
```

#### 3. Build Artifacts
```bash
dist/
build/
out/
target/                # Java/Rust
*.o, *.so, *.dylib    # Compiled objects
*.exe, *.dll           # Windows binaries
```

#### 4. Environment & Secrets
```bash
.env
.env.local
.env.*.local
*.key
*.pem
credentials.json
secrets.yaml
config.local.*
```

#### 5. OS & Editor Files
```bash
.DS_Store              # macOS
Thumbs.db              # Windows
*.swp, *.swo          # Vim
*~                     # Editor backups
.idea/                 # JetBrains
.vscode/               # VS Code (unless project-specific)
```

#### 6. Logs & Temporary Files
```bash
*.log
*.tmp
*.temp
*.cache
.cache/
tmp/
temp/
*.bak
```

### MANDATORY Pre-Commit Cleanup Script

```bash
#!/bin/bash

echo "=== Cleaning Unnecessary Files Before Commit ==="

# Function to remove if exists
remove_if_exists() {
  if [ -e "$1" ]; then
    rm -rf "$1"
    echo "  Removed: $1"
  fi
}

# 1. Remove dependencies
echo "
[1/6] Removing dependencies..."
remove_if_exists "node_modules"
remove_if_exists "vendor"
remove_if_exists "__pycache__"
remove_if_exists ".pytest_cache"
remove_if_exists "*.egg-info"
find . -name "*.pyc" -delete 2>/dev/null
find . -name "*.pyo" -delete 2>/dev/null

# 2. Remove virtual environments
echo "
[2/6] Removing virtual environments..."
remove_if_exists "venv"
remove_if_exists ".venv"
remove_if_exists "env"
remove_if_exists "virtualenv"

# 3. Remove build artifacts
echo "
[3/6] Removing build artifacts..."
remove_if_exists "dist"
remove_if_exists "build"
remove_if_exists "out"
remove_if_exists "target"

# 4. Remove environment files (keep .env.example)
echo "
[4/6] Removing environment files..."
find . -name ".env" -not -name ".env.example" -delete 2>/dev/null
find . -name "*.key" -delete 2>/dev/null
find . -name "*.pem" -delete 2>/dev/null
remove_if_exists "credentials.json"
remove_if_exists "secrets.yaml"

# 5. Remove OS/editor files
echo "
[5/6] Removing OS/editor files..."
find . -name ".DS_Store" -delete 2>/dev/null
find . -name "Thumbs.db" -delete 2>/dev/null
find . -name "*.swp" -delete 2>/dev/null
find . -name "*.swo" -delete 2>/dev/null
find . -name "*~" -delete 2>/dev/null
remove_if_exists ".idea"
remove_if_exists ".vscode"

# 6. Remove logs/temp files
echo "
[6/6] Removing logs and temp files..."
find . -name "*.log" -delete 2>/dev/null
find . -name "*.tmp" -delete 2>/dev/null
find . -name "*.temp" -delete 2>/dev/null
find . -name "*.cache" -delete 2>/dev/null
find . -name "*.bak" -delete 2>/dev/null
remove_if_exists ".cache"
remove_if_exists "tmp"
remove_if_exists "temp"

echo "
✅ Cleanup complete - ready for git add"
```

### MANDATORY .gitignore Check

Before committing, ensure `.gitignore` exists and contains:

```gitignore
# Dependencies
node_modules/
vendor/
__pycache__/
*.pyc
*.pyo
.pytest_cache/
.coverage
*.egg-info/

# Virtual Environments
venv/
.venv/
env/
virtualenv/

# Build Artifacts
dist/
build/
out/
target/
*.o
*.so
*.dylib

# Environment & Secrets
.env
.env.local
.env.*.local
*.key
*.pem
credentials.json
secrets.yaml
config.local.*

# OS Files
.DS_Store
Thumbs.db
*.swp
*.swo
*~

# IDE
.idea/
.vscode/

# Logs & Temp
*.log
*.tmp
*.temp
*.cache
.cache/
tmp/
temp/
*.bak
```

### Agent Workflow Integration

**BEFORE `git add .`**:
```bash
# 1. Run cleanup script
bash cleanup_before_commit.sh

# 2. Verify .gitignore exists
if [ ! -f .gitignore ]; then
  echo "Creating .gitignore..."
  cat > .gitignore << 'EOF'
  [paste gitignore content above]
EOF
fi

# 3. Check for any remaining unnecessary files
UNNECESSARY=$(find . -name "node_modules" -o -name "__pycache__" -o -name ".env" -o -name ".DS_Store" | head -5)
if [ -n "$UNNECESSARY" ]; then
  echo "⚠️  WARNING: Still found unnecessary files:"
  echo "$UNNECESSARY"
  echo "Review before committing!"
fi

# 4. NOW safe to add
git add .
```

---

## Feature 3: Ensure Requirements File Exists

### The Problem
Projects pushed without requirements files cannot be installed/run by others.

### The Solution
ALWAYS check for and validate requirements file before pushing.

### Requirements Files by Language

| Language/Framework | Required File(s) | Contains |
|-------------------|-----------------|----------|
| Python | `requirements.txt` OR `pyproject.toml` OR `Pipfile` | Package dependencies with versions |
| Node.js | `package.json` | dependencies + devDependencies |
| PHP | `composer.json` | require + require-dev |
| Ruby | `Gemfile` | gem dependencies |
| Go | `go.mod` | module dependencies |
| Rust | `Cargo.toml` | dependencies |
| Java | `pom.xml` OR `build.gradle` | Maven/Gradle dependencies |

### MANDATORY Requirements Check Script

```bash
#!/bin/bash

echo "=== Checking Requirements Files ==="

PROJECT_TYPE=""
REQUIREMENTS_FILE=""
FOUND=false

# Detect Python
if ls *.py &>/dev/null 2>&1 || [ -d "src" ] && ls src/*.py &>/dev/null 2>&1; then
  PROJECT_TYPE="Python"
  echo "Detected: Python project"

  if [ -f "requirements.txt" ]; then
    REQUIREMENTS_FILE="requirements.txt"
    FOUND=true
  elif [ -f "pyproject.toml" ]; then
    REQUIREMENTS_FILE="pyproject.toml"
    FOUND=true
  elif [ -f "Pipfile" ]; then
    REQUIREMENTS_FILE="Pipfile"
    FOUND=true
  fi
fi

# Detect Node.js
if [ -f "package.json" ] || ls *.js *.ts &>/dev/null 2>&1; then
  PROJECT_TYPE="Node.js"
  echo "Detected: Node.js project"

  if [ -f "package.json" ]; then
    REQUIREMENTS_FILE="package.json"
    FOUND=true
  fi
fi

# Detect PHP
if ls *.php &>/dev/null 2>&1; then
  PROJECT_TYPE="PHP"
  echo "Detected: PHP project"

  if [ -f "composer.json" ]; then
    REQUIREMENTS_FILE="composer.json"
    FOUND=true
  fi
fi

# Detect Go
if ls *.go &>/dev/null 2>&1; then
  PROJECT_TYPE="Go"
  echo "Detected: Go project"

  if [ -f "go.mod" ]; then
    REQUIREMENTS_FILE="go.mod"
    FOUND=true
  fi
fi

# Detect Rust
if ls *.rs &>/dev/null 2>&1 || [ -f "Cargo.toml" ]; then
  PROJECT_TYPE="Rust"
  echo "Detected: Rust project"

  if [ -f "Cargo.toml" ]; then
    REQUIREMENTS_FILE="Cargo.toml"
    FOUND=true
  fi
fi

# Results
if [ "$FOUND" = true ]; then
  echo "✅ PASS: Found $REQUIREMENTS_FILE for $PROJECT_TYPE project"

  # Validate file is not empty
  if [ ! -s "$REQUIREMENTS_FILE" ]; then
    echo "❌ FAIL: $REQUIREMENTS_FILE is empty!"
    exit 1
  fi

  echo "✅ $REQUIREMENTS_FILE is not empty"
  exit 0
else
  if [ -n "$PROJECT_TYPE" ]; then
    echo "❌ FAIL: $PROJECT_TYPE project missing requirements file!"
    echo "Expected one of: $(get_expected_files)"
    exit 1
  else
    echo "⚠️  WARN: Could not detect project type or no code files"
    exit 0
  fi
fi
```

### Auto-Generate Requirements Files

If missing, agent should offer to create:

#### Python
```bash
# Generate requirements.txt from imports
pip freeze > requirements.txt
```

#### Node.js
```bash
# Initialize package.json
npm init -y

# Or yarn
yarn init -y
```

#### PHP
```bash
# Initialize composer.json
composer init --no-interaction
```

### Agent Workflow Integration

**BEFORE git push**:
```bash
# 1. Check requirements file exists
bash check_requirements.sh

# 2. If missing, ask user or auto-generate
if [ $? -ne 0 ]; then
  echo "⚠️  Requirements file missing!"
  echo "Do you want me to generate it? (y/n)"
  # If yes, run appropriate command above
fi

# 3. Validate content (not empty, valid format)

# 4. Add to commit if newly created
git add requirements.txt  # or package.json, etc.
```

---

## Feature 4: Validate Authentication Necessity

### The Problem
Agents implement authentication for EVERY project, even when not needed. This wastes time and adds unnecessary complexity.

### The Solution
ALWAYS ask if authentication is needed BEFORE implementing registration/login features.

### The Questionnaire (MANDATORY)

When user mentions "users", "accounts", "login", or "registration", agent MUST ask:

```
Before I implement authentication, I need to understand if it's actually necessary:

## Authentication Necessity Questions:

1. **Does this application handle user-specific data that belongs to individual users?**
   - Examples: Personal todos, user profiles, private messages
   - If NO → Auth likely not needed

2. **Do users need individual accounts with different permissions or personalized content?**
   - Examples: Admin vs user roles, personalized dashboards
   - If NO → Auth likely not needed

3. **Is there any sensitive or private information?**
   - Examples: Financial data, health records, PII
   - If YES → Auth REQUIRED

4. **Can the application function as a public/anonymous service?**
   - Examples: Calculator, public blog, weather app
   - If YES → Auth likely not needed

5. **Do users need to save their work/state between sessions?**
   - Could this be done with localStorage instead?
   - If localStorage works → Auth not needed

6. **Are there any compliance requirements?**
   - Examples: GDPR, HIPAA, PCI-DSS
   - If YES → Auth may be required

## Please answer these questions so I can determine the appropriate approach.
```

### Decision Tree

```
User-specific data?
├─ NO → SKIP AUTH ❌
└─ YES
    ↓
    Sensitive/Private data?
    ├─ YES → AUTH REQUIRED ✅
    └─ NO
        ↓
        Need persistence across sessions?
        ├─ NO → SKIP AUTH ❌
        └─ YES
            ↓
            Can use localStorage/sessionStorage?
            ├─ YES → SKIP AUTH ❌ (use browser storage)
            └─ NO → AUTH OPTIONAL ⚠️
                ↓
                Multiple users with different permissions?
                ├─ YES → AUTH REQUIRED ✅
                └─ NO → SKIP AUTH ❌
```

### Examples

#### ❌ Auth NOT Needed:
1. **Calculator App**: Stateless, no data persistence
2. **Public Blog** (read-only): Anyone can read, no accounts
3. **Weather App**: Public data, no personalization
4. **Timer/Stopwatch**: No data needs saving
5. **Static Documentation Site**: Public information only

**Alternative**: Use localStorage, sessionStorage, or cookies for temporary state

#### ⚠️ Auth OPTIONAL:
1. **Todo App**: Could use localStorage, but sync across devices is nice-to-have
2. **Note-taking App**: Local storage works, but cloud sync adds value
3. **Recipe Saver**: Can browse publicly, but saved recipes need auth

**Recommendation**: Start without auth, add later if users request sync/cloud features

#### ✅ Auth REQUIRED:
1. **Banking App**: Financial data, security critical
2. **Social Network**: User profiles, private content
3. **E-commerce**: Orders, payment info, shipping addresses
4. **Healthcare Portal**: Medical records, HIPAA compliance
5. **Team Collaboration**: Permissions, private workspaces
6. **Admin Dashboard**: Different user roles and permissions

**Requirement**: Implement secure authentication with proper security measures

### Documentation in Project Brief

Agent MUST add this section to project brief:

**If Auth NOT Needed**:
```markdown
## Authentication Decision

**Verdict**: ❌ Authentication NOT Required

**Reasoning**:
- Application uses localStorage for state persistence
- No sensitive or user-specific data
- Public access model (no private content)
- No compliance requirements

**Alternative Approach**:
- Data Storage: Browser localStorage
- Session Management: Session Storage for temporary state
- User Identification: Not needed

**Future Considerations**:
- If users request sync across devices → Add optional auth later
- If features become user-specific → Revisit auth necessity
- Start simple, add complexity only when needed
```

**If Auth IS Needed**:
```markdown
## Authentication Requirements

**Verdict**: ✅ Authentication REQUIRED

**Reasoning**:
- Handles sensitive user data (financial/health/PII)
- Different permission levels needed (admin, user, moderator)
- Compliance requirements (GDPR, HIPAA, etc.)
- User-specific content must be private

**Auth Features to Implement**:
- [x] User registration with email verification
- [x] Secure login (password hashing with bcrypt)
- [x] Password reset flow
- [x] Session management (JWT tokens)
- [x] Multi-factor authentication (for high security)
- [x] Role-based access control
- [ ] OAuth/Social login (optional)

**Security Measures**:
- [x] HTTPS/TLS required
- [x] Password complexity requirements
- [x] Rate limiting on auth endpoints
- [x] Account lockout after 5 failed attempts
- [x] CSRF protection
- [x] Audit logging for sensitive actions

**Compliance**:
- [x] GDPR compliance (EU users)
- [x] User data export functionality
- [x] Right to deletion (account deletion)
```

### Agent Workflow Integration

**BEFORE implementing any auth code**:
```bash
# 1. Check if user mentioned auth-related keywords
if grep -riq "register\|login\|auth\|user.*account" requirements.md; then

  # 2. Ask authentication necessity questions
  echo "I notice authentication might be needed. Let me ask some questions..."
  # Present questionnaire to user

  # 3. Wait for answers

  # 4. Make decision based on answers
  # Calculate score (YES answers)

  if [ $YES_COUNT -le 2 ]; then
    echo "❌ Auth NOT needed for this project"
    echo "Alternative: [suggest localStorage/sessionStorage]"
    SKIP_AUTH=true
  elif [ $YES_COUNT -le 4 ]; then
    echo "⚠️  Auth OPTIONAL - recommend starting without it"
    SKIP_AUTH=true
  else
    echo "✅ Auth REQUIRED - implementing secure authentication"
    SKIP_AUTH=false
  fi

  # 5. Document decision in project brief

fi
```

---

## Complete Pre-Commit/Pre-Push Workflow

### Master Script: Run Before EVERY Commit/Push

```bash
#!/bin/bash

echo "========================================="
echo "  GIT WORKFLOW VALIDATION"
echo "  Running all 4 mandatory checks..."
echo "========================================="

FAILED=0

# Feature 1: Clean unnecessary files
echo "
[CHECK 1/4] Cleaning unnecessary files..."
bash cleanup_before_commit.sh
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Cleanup failed"
  FAILED=$((FAILED + 1))
else
  echo "✅ PASS: Cleanup complete"
fi

# Feature 2: Check requirements file
echo "
[CHECK 2/4] Verifying requirements file..."
bash check_requirements.sh
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Requirements file missing or invalid"
  FAILED=$((FAILED + 1))
else
  echo "✅ PASS: Requirements file valid"
fi

# Feature 3: Validate auth necessity (if applicable)
echo "
[CHECK 3/4] Validating authentication necessity..."
if grep -riq "register\|login\|authentication" . 2>/dev/null; then
  if [ -f "ai/memory-bank/project-brief.md" ]; then
    if grep -q "Authentication Decision\|Authentication Requirements" ai/memory-bank/project-brief.md; then
      echo "✅ PASS: Auth decision documented"
    else
      echo "❌ FAIL: Auth code found but not documented in project brief"
      FAILED=$((FAILED + 1))
    fi
  else
    echo "⚠️  WARN: Auth code found but no project brief"
  fi
else
  echo "✅ PASS: No auth code found"
fi

# Feature 4: Verify remote push (run after push)
echo "
[CHECK 4/4] Will verify remote push after git push command..."
echo "✅ Ready to commit"

# Summary
echo "
========================================="
if [ $FAILED -eq 0 ]; then
  echo "✅ ALL PRE-COMMIT CHECKS PASSED"
  echo "Safe to proceed with git commit"
  echo "========================================="
  exit 0
else
  echo "❌ $FAILED CHECK(S) FAILED"
  echo "Fix issues before committing"
  echo "========================================="
  exit 1
fi
```

### Usage in Agent Workflow

```bash
# 1. Make code changes

# 2. Run pre-commit checks
bash git_workflow_checks.sh
if [ $? -ne 0 ]; then
  echo "Pre-commit checks failed - fixing issues..."
  exit 1
fi

# 3. Commit
git add .
git commit -m "Your commit message"

# 4. Push
git push origin main

# 5. VERIFY push went to remote (MANDATORY)
bash verify_remote_push.sh
if [ $? -eq 0 ]; then
  echo "✅ SUCCESS: Code committed and pushed to GitHub"
  echo "✅ Remote repository is up-to-date"
else
  echo "❌ ERROR: Push verification failed"
  echo "Retrying push..."
  git push origin main --verbose
fi
```

---

## Summary: The 4 Mandatory Features

1. ✅ **Verify Remote Push**: Always confirm code is on GitHub, not just local
2. ✅ **Clean Unnecessary Files**: Remove node_modules, .env, etc. before commit
3. ✅ **Check Requirements File**: Ensure dependencies are documented
4. ✅ **Validate Auth Necessity**: Don't implement auth unless actually needed

**ALL 4 MUST PASS before saying "pushed to GitHub"**

---

## Integration with Engineering Agents

Add to all engineering agents:

```markdown
### Git Workflow (MANDATORY)

Before EVERY commit and push:
1. Run cleanup script (remove unnecessary files)
2. Verify requirements file exists and is valid
3. If auth code present, verify necessity was validated
4. After push, verify it went to REMOTE repository

**Reference**: See `GIT-WORKFLOW-PROTOCOL.md` for complete protocol
**Scripts**: Available in `scripts/git_workflow/`
```
