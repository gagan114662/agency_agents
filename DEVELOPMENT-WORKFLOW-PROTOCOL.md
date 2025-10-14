# Development Workflow Protocol

**Version**: 1.0
**Status**: MANDATORY
**Applies To**: All Engineering Agents

---

## 🎯 Purpose

This protocol defines the **mandatory development workflow** that all engineering agents MUST follow when working on projects. These rules ensure code quality, proper testing, maintainable organization, and professional development practices.

---

## 🚨 CRITICAL: Protocol Enforcement Rules

### When This Protocol Applies

This protocol is **MANDATORY** for:
- ✅ All new feature development
- ✅ All bug fixes and improvements
- ✅ All code refactoring
- ✅ All project setup and configuration
- ✅ All code modifications of any size

**NO EXCEPTIONS**: Every agent must follow these rules for every task.

---

## 📋 The 11 Mandatory Workflow Rules

### Rule 1: Pre-Work Test Approval (MANDATORY)

**Rule**: ALWAYS get user approval on tests BEFORE writing any implementation code.

**Workflow**:
1. User requests a feature or task
2. Agent gathers requirements (see REQUIREMENTS-GATHERING-PROTOCOL.md)
3. Agent writes comprehensive tests FIRST
4. Agent asks user: "I've written tests for [feature]. May I proceed with implementation?"
5. User reviews and approves tests
6. ONLY THEN can agent begin implementation

**Why**: Ensures mutual understanding of expected behavior before time is invested in implementation.

**Validation**:
```bash
# Check test file was created before implementation
TEST_FILE="tests/test_feature.py"
IMPL_FILE="src/feature.py"

if [ -f "$TEST_FILE" ] && [ -f "$IMPL_FILE" ]; then
    TEST_TIME=$(stat -f %m "$TEST_FILE")
    IMPL_TIME=$(stat -f %m "$IMPL_FILE")

    if [ $TEST_TIME -lt $IMPL_TIME ]; then
        echo "✅ PASS: Tests created before implementation"
    else
        echo "❌ FAIL: Implementation created before tests"
    fi
else
    echo "❌ FAIL: Missing test or implementation file"
fi
```

**Reference**: See `TEST-FIRST-DEVELOPMENT.md` for complete test-first guidelines.

---

### Rule 2: Git Commit Checkpoint Protocol (MANDATORY)

**Rule**: Create git commits at logical milestones and ask user before committing.

**Workflow**:
1. Complete a logical unit of work (feature, fix, refactor)
2. Run all tests locally to ensure they pass
3. Ask user: "I've completed [description]. Would you like me to create a git commit?"
4. If user approves, follow Git Workflow Protocol (see GIT-WORKFLOW-PROTOCOL.md)
5. Create descriptive commit message following repository conventions

**Why**: Ensures user awareness of git history and prevents unwanted commits.

**Validation**:
```bash
# Check recent commit message quality
LAST_COMMIT=$(git log -1 --pretty=%B)

# Check commit message is descriptive (>20 characters)
if [ ${#LAST_COMMIT} -gt 20 ]; then
    echo "✅ PASS: Descriptive commit message"
else
    echo "❌ FAIL: Commit message too short"
fi

# Check commit follows conventional commits format (optional but recommended)
if echo "$LAST_COMMIT" | grep -qE "^(feat|fix|docs|style|refactor|test|chore):"; then
    echo "✅ PASS: Follows conventional commits"
fi
```

**Git Workflow Checks** (MANDATORY before every commit):
1. ✅ Clean unnecessary files (node_modules, __pycache__, .env, etc.)
2. ✅ Verify requirements file exists
3. ✅ Validate auth necessity
4. ✅ Verify remote push completed successfully

**Reference**: See `GIT-WORKFLOW-PROTOCOL.md` for complete git protocol.

---

### Rule 3: Logging Standards Enforcement (MANDATORY)

**Rule**: Use INFO level for production, DEBUG for development only.

**Production Code Requirements**:
- ✅ Use `logging.info()` for important events
- ✅ Use `logging.error()` for errors
- ✅ Use `logging.warning()` for warnings
- ❌ NO `logging.debug()` statements in production code
- ❌ NO `print()` statements in production code

**Development Code**:
- ✅ Use `logging.debug()` for development debugging
- ✅ Remove or disable DEBUG logs before committing

**Why**: Prevents log spam in production and ensures proper log levels for monitoring.

**Validation**:
```bash
# Check for print statements in production code
PROD_FILES=$(find src -name "*.py" -o -name "*.js" -o -name "*.ts")

PRINT_COUNT=0
for file in $PROD_FILES; do
    if grep -qE "(print\(|console\.log|console\.debug)" "$file"; then
        echo "❌ FAIL: Found print/console.log in $file"
        PRINT_COUNT=$((PRINT_COUNT + 1))
    fi
done

if [ $PRINT_COUNT -eq 0 ]; then
    echo "✅ PASS: No print statements in production code"
fi

# Check for debug logging in production
DEBUG_COUNT=0
for file in $PROD_FILES; do
    if grep -qE "(logging\.debug|logger\.debug)" "$file"; then
        echo "⚠️  WARNING: Found debug logging in $file"
        DEBUG_COUNT=$((DEBUG_COUNT + 1))
    fi
done

if [ $DEBUG_COUNT -eq 0 ]; then
    echo "✅ PASS: No debug logging in production code"
fi
```

**Example Correct Logging**:
```python
import logging

logger = logging.getLogger(__name__)

def process_user_data(user_id):
    logger.info(f"Processing user data for user_id={user_id}")

    try:
        result = expensive_operation(user_id)
        logger.info(f"Successfully processed user {user_id}")
        return result
    except Exception as e:
        logger.error(f"Failed to process user {user_id}: {e}")
        raise
```

---

### Rule 4: Bash Test Validation for Math/Logic (MANDATORY)

**Rule**: For any mathematical calculations or critical logic, create bash test scripts to validate correctness.

**When This Applies**:
- ✅ Mathematical calculations (percentages, conversions, formulas)
- ✅ Financial calculations (pricing, taxes, fees)
- ✅ Date/time calculations
- ✅ Algorithm implementations
- ✅ Data transformations

**Workflow**:
1. Implement the calculation/logic
2. Create a bash script that tests the function with known inputs/outputs
3. Run the bash script to validate behavior
4. Include the bash script in `tests/validation/` directory

**Why**: Bash scripts provide an independent verification layer that catches logic errors.

**Validation**:
```bash
# Example validation script for a percentage calculation function
# tests/validation/test_percentage_calc.sh

#!/bin/bash

# Test percentage calculation
python3 -c "from src.calculations import calculate_percentage; print(calculate_percentage(50, 200))" > /tmp/result.txt
RESULT=$(cat /tmp/result.txt)

if [ "$RESULT" = "25.0" ]; then
    echo "✅ PASS: Percentage calculation correct (50/200 = 25%)"
else
    echo "❌ FAIL: Expected 25.0, got $RESULT"
    exit 1
fi

# Test edge case: zero
python3 -c "from src.calculations import calculate_percentage; print(calculate_percentage(0, 100))" > /tmp/result.txt
RESULT=$(cat /tmp/result.txt)

if [ "$RESULT" = "0.0" ]; then
    echo "✅ PASS: Zero percentage correct"
else
    echo "❌ FAIL: Expected 0.0 for zero input"
    exit 1
fi

# Test edge case: division by zero handling
python3 -c "from src.calculations import calculate_percentage; print(calculate_percentage(50, 0))" 2>&1 | grep -q "ZeroDivisionError\|ValueError\|Cannot divide by zero"

if [ $? -eq 0 ]; then
    echo "✅ PASS: Handles division by zero correctly"
else
    echo "❌ FAIL: Does not handle division by zero"
    exit 1
fi

echo "✅ All percentage calculation tests passed"
```

**Running Validation Scripts**:
```bash
# Make script executable
chmod +x tests/validation/test_percentage_calc.sh

# Run validation
./tests/validation/test_percentage_calc.sh
```

---

### Rule 5: Code Organization Standards (MANDATORY)

**Rule**: No duplicate functions, proper file structure, single responsibility principle.

**Requirements**:
1. ✅ **No duplicate functions**: Each function should exist in exactly ONE place
2. ✅ **Proper file organization**: Related functions in the same module
3. ✅ **Single responsibility**: Each module/file has ONE clear purpose
4. ✅ **Clear naming**: File names match their primary responsibility
5. ✅ **No "utils" dumping grounds**: Utility functions must be properly categorized

**Why**: Prevents code duplication, reduces bugs, improves maintainability.

**Project Structure Example**:
```
src/
├── auth/                    # Authentication related code
│   ├── jwt_handler.py      # JWT token operations
│   ├── password.py         # Password hashing/verification
│   └── permissions.py      # Permission checking
├── database/               # Database operations
│   ├── connection.py       # DB connection management
│   ├── models.py          # Data models
│   └── queries.py         # Reusable queries
├── api/                    # API endpoints
│   ├── users.py           # User endpoints
│   ├── products.py        # Product endpoints
│   └── orders.py          # Order endpoints
└── services/               # Business logic
    ├── user_service.py    # User business logic
    ├── email_service.py   # Email operations
    └── payment_service.py # Payment processing
```

**Validation**:
```bash
# Check for duplicate function definitions
echo "Checking for duplicate functions..."

# Python
DUPLICATE_FUNCS=$(grep -rh "^def " src/ | sort | uniq -d)
if [ -z "$DUPLICATE_FUNCS" ]; then
    echo "✅ PASS: No duplicate function definitions found"
else
    echo "❌ FAIL: Found duplicate functions:"
    echo "$DUPLICATE_FUNCS"
fi

# JavaScript/TypeScript
DUPLICATE_FUNCS=$(grep -rh "function\s\+\w\+" src/ | sort | uniq -d)
if [ -z "$DUPLICATE_FUNCS" ]; then
    echo "✅ PASS: No duplicate JS functions found"
else
    echo "❌ FAIL: Found duplicate JS functions:"
    echo "$DUPLICATE_FUNCS"
fi

# Check for "utils" files (code smell)
UTILS_FILES=$(find src/ -name "*utils*" -o -name "*helpers*")
if [ -z "$UTILS_FILES" ]; then
    echo "✅ PASS: No generic utils files (good organization)"
else
    echo "⚠️  WARNING: Found generic utils files (consider better organization):"
    echo "$UTILS_FILES"
fi
```

---

### Rule 6: Local Testing Before Deployment (MANDATORY)

**Rule**: Run ALL tests locally and ensure 100% pass rate before deploying or pushing code.

**Workflow**:
1. Complete implementation
2. Run full test suite locally
3. Verify 100% of tests pass
4. Check code coverage meets minimum threshold (typically 80%+)
5. ONLY THEN proceed to commit/push/deploy

**Why**: Catches issues early, prevents broken code in production, maintains code quality.

**Validation**:
```bash
# Python projects
echo "Running Python tests..."
pytest tests/ -v --cov=src --cov-report=term-missing

if [ $? -eq 0 ]; then
    echo "✅ PASS: All Python tests passed"
else
    echo "❌ FAIL: Some tests failed - DO NOT DEPLOY"
    exit 1
fi

# JavaScript/TypeScript projects
echo "Running JS/TS tests..."
npm test -- --coverage

if [ $? -eq 0 ]; then
    echo "✅ PASS: All JS tests passed"
else
    echo "❌ FAIL: Some tests failed - DO NOT DEPLOY"
    exit 1
fi

# Check coverage threshold
COVERAGE=$(pytest tests/ --cov=src --cov-report=term | grep "TOTAL" | awk '{print $4}' | sed 's/%//')

if [ $COVERAGE -ge 80 ]; then
    echo "✅ PASS: Coverage is $COVERAGE% (meets 80% threshold)"
else
    echo "❌ FAIL: Coverage is $COVERAGE% (below 80% threshold)"
    exit 1
fi
```

---

### Rule 7: Production-Ready Code Standards (MANDATORY)

**Rule**: No commented-out code, no TODOs, no debug statements in production.

**Production Code Requirements**:
- ❌ NO commented-out code blocks
- ❌ NO TODO/FIXME comments
- ❌ NO debug statements or debug logging
- ❌ NO console.log or print statements
- ❌ NO temporary hacks or workarounds
- ✅ All code is clean, documented, and intentional

**Why**: Maintains professional code quality and prevents confusion.

**Validation**:
```bash
# Check for commented-out code
echo "Checking for commented-out code..."
COMMENTED_CODE=$(grep -rE "^\s*#.*=|^\s*//.*=" src/ | wc -l)

if [ $COMMENTED_CODE -eq 0 ]; then
    echo "✅ PASS: No commented-out code found"
else
    echo "❌ FAIL: Found $COMMENTED_CODE lines of commented-out code"
fi

# Check for TODO/FIXME comments
echo "Checking for TODO/FIXME comments..."
TODO_COUNT=$(grep -riE "TODO|FIXME|XXX|HACK" src/ | wc -l)

if [ $TODO_COUNT -eq 0 ]; then
    echo "✅ PASS: No TODO/FIXME comments in production code"
else
    echo "❌ FAIL: Found $TODO_COUNT TODO/FIXME comments"
    grep -riE "TODO|FIXME|XXX|HACK" src/
fi

# Check for debug statements
echo "Checking for debug statements..."
DEBUG_COUNT=$(grep -riE "console\.log|console\.debug|print\(|debugger|pdb\.set_trace" src/ | wc -l)

if [ $DEBUG_COUNT -eq 0 ]; then
    echo "✅ PASS: No debug statements found"
else
    echo "❌ FAIL: Found $DEBUG_COUNT debug statements"
    grep -riE "console\.log|console\.debug|print\(|debugger|pdb\.set_trace" src/
fi
```

---

### Rule 8: User Decision Points with Options (MANDATORY)

**Rule**: At key decision points, present options to user with pros/cons before proceeding.

**When This Applies**:
- ✅ Technology stack choices (framework, library, database)
- ✅ Architecture decisions (monolith vs microservices, REST vs GraphQL)
- ✅ Implementation approaches (algorithm choice, design pattern)
- ✅ Major refactoring decisions
- ✅ Deployment strategy choices

**Workflow**:
1. Identify decision point
2. Research 2-3 viable options
3. Present to user with:
   - Brief description of each option
   - Pros and cons
   - Recommendation with reasoning
4. Get user approval before proceeding

**Why**: Ensures user is informed and agrees with major technical decisions.

**Example Decision Presentation**:
```markdown
## Decision Point: State Management Library

I need to choose a state management solution for this React application. Here are the options:

### Option 1: Redux Toolkit (Recommended)
**Pros**:
- Industry standard with extensive ecosystem
- Excellent DevTools for debugging
- Built-in middleware for async operations
- Strong TypeScript support

**Cons**:
- More boilerplate than alternatives
- Steeper learning curve
- Can be overkill for simple apps

### Option 2: Zustand
**Pros**:
- Minimal boilerplate
- Easy to learn and use
- Small bundle size (1KB)
- Good TypeScript support

**Cons**:
- Less mature ecosystem
- Fewer middleware options
- Less structured (can lead to inconsistent patterns)

### Option 3: React Context + useReducer
**Pros**:
- No external dependencies
- Native React solution
- Very lightweight
- Simple for small apps

**Cons**:
- Performance issues with frequent updates
- No built-in DevTools
- More manual work for async operations
- Not ideal for large-scale apps

### My Recommendation: Redux Toolkit
Given the project requirements (medium-large scale, team collaboration, complex async logic), I recommend Redux Toolkit for its robust ecosystem, excellent debugging tools, and proven scalability.

**Which option would you like me to proceed with?**
```

**Validation**:
```bash
# Check git history for decision documentation
echo "Checking for documented decisions..."

# Look for decision documentation in commits or docs
DECISION_DOCS=$(find docs/ -name "*decision*" -o -name "*adr*" 2>/dev/null)

if [ -n "$DECISION_DOCS" ]; then
    echo "✅ PASS: Found decision documentation:"
    echo "$DECISION_DOCS"
else
    echo "⚠️  WARNING: No decision documentation found (consider creating docs/decisions/)"
fi
```

---

### Rule 9: Copy-Paste Ready Commands (MANDATORY)

**Rule**: All commands provided to user must be executable as-is with NO placeholders.

**Requirements**:
- ✅ Use ACTUAL paths (not `<your-project-path>`)
- ✅ Use ACTUAL values (not `<your-api-key>`)
- ✅ Use ACTUAL file names (not `<filename>`)
- ✅ Commands must work immediately when copy-pasted

**Why**: Saves user time and prevents errors from placeholder mistakes.

**BAD Examples** (DO NOT DO THIS):
```bash
# ❌ Has placeholders
cd <your-project-directory>
export API_KEY=<your-api-key>
docker run -v <path-to-config>:/config myapp
```

**GOOD Examples** (DO THIS):
```bash
# ✅ Copy-paste ready with actual paths
cd /Users/gagan/Desktop/gagan_projects/agency_agents
export API_KEY=sk-test-1234567890abcdef
docker run -v /Users/gagan/Desktop/gagan_projects/config:/config myapp
```

**Validation**:
```bash
# Check README and docs for placeholder patterns
echo "Checking documentation for placeholders..."

PLACEHOLDER_PATTERNS="<.*>|\[your-.*\]|\{your-.*\}|<YOUR-.*>|<YourProject>|<project-name>"

PLACEHOLDER_COUNT=$(grep -rE "$PLACEHOLDER_PATTERNS" README.md docs/ 2>/dev/null | wc -l)

if [ $PLACEHOLDER_COUNT -eq 0 ]; then
    echo "✅ PASS: No placeholders found in documentation"
else
    echo "❌ FAIL: Found $PLACEHOLDER_COUNT placeholder instances"
    grep -rE "$PLACEHOLDER_PATTERNS" README.md docs/ 2>/dev/null
fi
```

---

### Rule 10: Virtual Environment Management (MANDATORY)

**Rule**: Use project-specific virtual environments and ensure proper setup.

**Virtual Environment Configuration**:
- **Shared Venv Path**: `/Users/gagan/Desktop/gagan_projects/venv`
- **Projects Using Shared Venv**:
  - aitutor: https://github.com/vandanchopra/aitutor
  - ipop: https://github.com/gagan114662/ipop

**Workflow**:
1. Check if venv exists at specified path
2. If not, create: `python3 -m venv /Users/gagan/Desktop/gagan_projects/venv`
3. Activate: `source /Users/gagan/Desktop/gagan_projects/venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Verify installation: `pip list`

**Why**: Ensures consistent Python environment across projects and prevents dependency conflicts.

**Validation**:
```bash
#!/bin/bash

VENV_PATH="/Users/gagan/Desktop/gagan_projects/venv"

echo "Validating virtual environment setup..."

# Check 1: Venv exists
if [ -d "$VENV_PATH" ]; then
    echo "✅ PASS: Virtual environment exists at $VENV_PATH"
else
    echo "❌ FAIL: Virtual environment not found at $VENV_PATH"
    echo "   Create with: python3 -m venv $VENV_PATH"
    exit 1
fi

# Check 2: Python interpreter exists
if [ -f "$VENV_PATH/bin/python" ]; then
    echo "✅ PASS: Python interpreter found"
    PYTHON_VERSION=$("$VENV_PATH/bin/python" --version)
    echo "   Python version: $PYTHON_VERSION"
else
    echo "❌ FAIL: Python interpreter not found in venv"
    exit 1
fi

# Check 3: pip is available
if [ -f "$VENV_PATH/bin/pip" ]; then
    echo "✅ PASS: pip is available"
    PIP_VERSION=$("$VENV_PATH/bin/pip" --version)
    echo "   pip version: $PIP_VERSION"
else
    echo "❌ FAIL: pip not found in venv"
    exit 1
fi

# Check 4: Verify project dependencies are installed
PROJECTS=("aitutor" "ipop")

for project in "${PROJECTS[@]}"; do
    PROJECT_PATH="/Users/gagan/Desktop/gagan_projects/$project"

    if [ -d "$PROJECT_PATH" ]; then
        echo "✅ PASS: Project $project found at $PROJECT_PATH"

        # Check for requirements file
        if [ -f "$PROJECT_PATH/requirements.txt" ]; then
            echo "✅ PASS: requirements.txt found for $project"

            # Try installing (dry-run to check validity)
            "$VENV_PATH/bin/pip" install --dry-run -r "$PROJECT_PATH/requirements.txt" > /dev/null 2>&1

            if [ $? -eq 0 ]; then
                echo "✅ PASS: requirements.txt is valid for $project"
            else
                echo "⚠️  WARNING: Some dependencies in requirements.txt may have issues"
            fi
        else
            echo "⚠️  WARNING: No requirements.txt found for $project"
        fi
    else
        echo "❌ FAIL: Project $project not found at $PROJECT_PATH"
    fi
done

echo ""
echo "✅ Virtual environment validation complete!"
echo ""
echo "To activate venv:"
echo "  source $VENV_PATH/bin/activate"
```

**Quick Commands**:
```bash
# Activate venv
source /Users/gagan/Desktop/gagan_projects/venv/bin/activate

# Check installed packages
pip list

# Install project dependencies
pip install -r /Users/gagan/Desktop/gagan_projects/aitutor/MediaMixer/requirements.txt
pip install -r /Users/gagan/Desktop/gagan_projects/ipop/requirements.txt

# Deactivate venv
deactivate
```

---

### Rule 11: To-Do List File Tracking (MANDATORY)

**Rule**: Maintain a to-do list file (`TODO.md`) in the project root with current status of all tasks.

**File Location**: `TODO.md` in project root

**Format**:
```markdown
# Project To-Do List

Last Updated: 2024-01-15

## In Progress
- [x] Implement user authentication system
  - Started: 2024-01-14
  - Status: 75% complete
  - Next: Add JWT refresh token logic

## Pending
- [ ] Add email verification
  - Priority: High
  - Blocked by: Email service provider setup

- [ ] Implement password reset flow
  - Priority: Medium
  - Estimated: 2-3 hours

- [ ] Add OAuth2 support (Google, GitHub)
  - Priority: Low
  - Estimated: 4-6 hours

## Completed
- [x] Set up project structure
  - Completed: 2024-01-10

- [x] Configure database connection
  - Completed: 2024-01-12

- [x] Create user model and migrations
  - Completed: 2024-01-13
```

**Workflow**:
1. Create `TODO.md` at project start
2. Update BEFORE starting each task (move to "In Progress")
3. Update AFTER completing each task (move to "Completed")
4. Add new tasks as discovered
5. Keep priorities and estimates updated

**Why**: Provides visibility into project progress and helps track what's left to do.

**Validation**:
```bash
#!/bin/bash

TODO_FILE="TODO.md"

echo "Validating TODO.md file..."

# Check 1: File exists
if [ -f "$TODO_FILE" ]; then
    echo "✅ PASS: TODO.md file exists"
else
    echo "❌ FAIL: TODO.md not found in project root"
    exit 1
fi

# Check 2: Has required sections
REQUIRED_SECTIONS=("In Progress" "Pending" "Completed")

for section in "${REQUIRED_SECTIONS[@]}"; do
    if grep -q "## $section" "$TODO_FILE"; then
        echo "✅ PASS: Section '$section' found"
    else
        echo "❌ FAIL: Section '$section' missing"
    fi
done

# Check 3: Has recent update (within last 7 days)
if [ $(uname) = "Darwin" ]; then
    # macOS
    LAST_MODIFIED=$(stat -f %m "$TODO_FILE")
else
    # Linux
    LAST_MODIFIED=$(stat -c %Y "$TODO_FILE")
fi

CURRENT_TIME=$(date +%s)
DAYS_OLD=$(( ($CURRENT_TIME - $LAST_MODIFIED) / 86400 ))

if [ $DAYS_OLD -le 7 ]; then
    echo "✅ PASS: TODO.md updated within last 7 days ($DAYS_OLD days ago)"
else
    echo "⚠️  WARNING: TODO.md not updated in $DAYS_OLD days (consider updating)"
fi

# Check 4: Has tasks in each section
IN_PROGRESS_COUNT=$(grep -c "- \[.\]" "$TODO_FILE" | awk '/## In Progress/,/## Pending/ {count++} END {print count}')
PENDING_COUNT=$(grep -c "- \[ \]" "$TODO_FILE")
COMPLETED_COUNT=$(grep -c "- \[x\]" "$TODO_FILE")

echo ""
echo "Task Summary:"
echo "  In Progress: $IN_PROGRESS_COUNT"
echo "  Pending: $PENDING_COUNT"
echo "  Completed: $COMPLETED_COUNT"

if [ $IN_PROGRESS_COUNT -eq 0 ] && [ $PENDING_COUNT -eq 0 ]; then
    echo "⚠️  WARNING: No tasks in progress or pending (project complete?)"
fi

echo ""
echo "✅ TODO.md validation complete!"
```

---

## 🔄 Complete Workflow Example

Here's how these rules work together in practice:

### Scenario: User asks to add a new feature

```markdown
USER: "Can you add a feature to calculate shipping costs based on weight and distance?"

AGENT:
Step 1: Requirements Gathering (REQUIREMENTS-GATHERING-PROTOCOL.md)
- Ask questions about weight units, distance calculation, pricing tiers
- Document requirements in project brief

Step 2: Write Tests FIRST (Rule 1 - Pre-Work Test Approval)
- Create tests/test_shipping_calculator.py
- Write comprehensive test cases
- Ask user: "I've written tests for shipping calculator. May I proceed?"

Step 3: Get User Approval
- Wait for user confirmation
- Address any test modifications

Step 4: Implement Feature (Test-First Development)
- Create src/services/shipping_calculator.py
- Implement to make tests pass
- Follow logging standards (Rule 3 - INFO level only)

Step 5: Create Bash Validation (Rule 4)
- Create tests/validation/test_shipping_calc.sh
- Validate math calculations independently

Step 6: Verify Code Organization (Rule 5)
- Ensure no duplicate functions
- Place in correct service directory
- Single responsibility principle

Step 7: Local Testing (Rule 6)
- Run pytest tests/
- Verify 100% pass rate
- Check coverage threshold

Step 8: Clean Production Code (Rule 7)
- Remove any debug statements
- Remove commented-out code
- Remove TODOs

Step 9: Update TODO.md (Rule 11)
- Move "Add shipping calculator" to Completed
- Update timestamp

Step 10: Git Commit Checkpoint (Rule 2)
- Ask user: "Feature complete. Create git commit?"
- Run Git Workflow Protocol checks (Rule 2)
- Create descriptive commit message

Step 11: User provides copy-paste commands (Rule 9)
"You can test the feature with:
source /Users/gagan/Desktop/gagan_projects/venv/bin/activate
python -c 'from src.services.shipping_calculator import calculate_shipping; print(calculate_shipping(5.5, 100))'"
```

---

## 📊 Protocol Compliance Checklist

Before completing ANY task, verify:

- [ ] **Rule 1**: Tests written and approved BEFORE implementation
- [ ] **Rule 2**: Git commit checkpoint asked and completed properly
- [ ] **Rule 3**: Logging standards followed (INFO level, no prints)
- [ ] **Rule 4**: Bash validation scripts created for math/logic
- [ ] **Rule 5**: Code organization checked (no duplicates, proper structure)
- [ ] **Rule 6**: All tests run locally and pass (100%)
- [ ] **Rule 7**: Production code clean (no TODOs, comments, debug)
- [ ] **Rule 8**: User consulted on all major decisions
- [ ] **Rule 9**: All commands are copy-paste ready (no placeholders)
- [ ] **Rule 10**: Virtual environment properly configured
- [ ] **Rule 11**: TODO.md updated with current status

---

## 🚀 Quick Reference Commands

### Activate Virtual Environment
```bash
source /Users/gagan/Desktop/gagan_projects/venv/bin/activate
```

### Run All Tests
```bash
# Python
pytest tests/ -v --cov=src --cov-report=term-missing

# JavaScript
npm test -- --coverage
```

### Run Validation Scripts
```bash
chmod +x tests/validation/*.sh
./tests/validation/test_*.sh
```

### Check Code Quality
```bash
# Check for print statements
grep -r "print(" src/

# Check for TODOs
grep -r "TODO\|FIXME" src/

# Check for debug logging
grep -r "logging.debug" src/
```

### Update TODO.md
```bash
# Open and update
vim TODO.md

# Validate
./tests/validation/validate_todo.sh
```

---

## 📚 Related Protocols

- **REQUIREMENTS-GATHERING-PROTOCOL.md**: How to gather requirements before starting
- **GIT-WORKFLOW-PROTOCOL.md**: Git commit and push requirements (4 mandatory checks)
- **TEST-FIRST-DEVELOPMENT.md**: Comprehensive test-first development guide

---

## ✅ Success Criteria

You've successfully followed this protocol when:
- ✅ All 11 rules are followed for every task
- ✅ Tests are written and approved before implementation
- ✅ Code is clean, organized, and production-ready
- ✅ All validation scripts pass
- ✅ User is informed at key decision points
- ✅ Git history is clean and descriptive
- ✅ TODO.md accurately reflects project status

---

**Remember**: These rules are MANDATORY, not suggestions. Following this protocol ensures professional-quality code and smooth collaboration.
