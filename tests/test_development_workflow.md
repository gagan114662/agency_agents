# Development Workflow Tests

## Test Suite: Development Best Practices Validation

### Test 1: Pre-Work Test Approval (MANDATORY)
```markdown
**Given**: Agent receives a new task or feature request
**When**: Agent begins work
**Then**: Agent MUST get user approval on tests BEFORE writing any implementation code

**Test Cases**:

#### Test 1.1: Test Creation Before Implementation
**Scenario**: User requests "Build a data validation function"

**Expected Agent Behavior**:
1. Agent analyzes requirements
2. Agent writes comprehensive tests
3. Agent presents tests to user
4. Agent asks: "Do these tests cover all requirements? Should I add integration tests?"
5. Agent WAITS for user approval
6. Only after "yes" → Agent implements code

**Validation**:
```bash
# Check that test file exists and has timestamp before implementation file
TEST_TIME=$(stat -f %m tests/test_feature.py)
IMPL_TIME=$(stat -f %m src/feature.py)

if [ "$TEST_TIME" -lt "$IMPL_TIME" ]; then
  echo "✅ PASS: Tests written before implementation"
else
  echo "❌ FAIL: Implementation written before tests"
  exit 1
fi
```

**Pass Criteria**:
- ✅ Tests written and presented to user
- ✅ User explicitly approves tests
- ✅ Integration tests included if needed
- ✅ No implementation code until approval

**Fail Criteria**:
- ❌ Agent writes implementation before tests
- ❌ Agent proceeds without user approval
- ❌ Agent skips integration tests when needed

---

#### Test 1.2: Test Content Validation
**Given**: Agent writes tests
**When**: Validating test quality
**Then**: Tests MUST import from actual codebase, NO hardcoded values

**Bad Test Example** ❌:
```python
def test_calculate_total():
    # Hardcoded - BAD!
    result = 150
    assert result == 150  # Not testing anything!
```

**Good Test Example** ✅:
```python
from src.calculator import calculate_total

def test_calculate_total():
    items = [50, 50, 50]
    result = calculate_total(items)  # Testing actual function
    assert result == 150
    assert isinstance(result, (int, float))
```

**Validation Script**:
```bash
# Check test files for hardcoded values
echo "=== Checking for hardcoded test values ==="

HARDCODED=$(grep -r "assert.*==" tests/ | grep -E "assert [0-9]+ == [0-9]+|assert \".*\" == \".*\"" | wc -l)

if [ "$HARDCODED" -gt 0 ]; then
  echo "❌ FAIL: Found $HARDCODED hardcoded assertions in tests"
  grep -r "assert.*==" tests/ | grep -E "assert [0-9]+ == [0-9]+|assert \".*\" == \".*\""
  exit 1
else
  echo "✅ PASS: No hardcoded test values found"
fi
```

**Pass Criteria**:
- ✅ All tests import from actual modules
- ✅ Tests verify real behavior, not hardcoded values
- ✅ Tests can catch real bugs

**Fail Criteria**:
- ❌ Tests have hardcoded expected values
- ❌ Tests don't import actual implementation
- ❌ Tests are just placeholders
```

### Test 2: Git Commit Checkpoints
```markdown
**Given**: Agent completes a task or subtask
**When**: About to move to next task
**Then**: Agent MUST ask user: "Do you want to commit and push these changes?"

**Test Cases**:

#### Test 2.1: Checkpoint After Task Completion
**Scenario**: Agent completes implementing feature X

**Expected Agent Behavior**:
```
Agent: "✅ Feature X is complete and all tests pass.

Before moving to the next task, would you like to:
1. Commit and push changes now
2. Continue to next task and commit later

What would you prefer?"
```

**User Response Handling**:
- If "1" or "yes" → Run git workflow, commit, push, verify
- If "2" or "later" → Proceed to next task

**Validation**:
```bash
# Check git history has reasonable commit frequency
# (not all changes in one massive commit at the end)

COMMITS=$(git log --oneline --since="1 day ago" | wc -l)
FILES_CHANGED=$(git diff HEAD~1 --stat | wc -l)

if [ "$FILES_CHANGED" -gt 50 ] && [ "$COMMITS" -lt 3 ]; then
  echo "⚠️  WARN: Large commit detected - should have been broken into smaller commits"
fi
```

**Pass Criteria**:
- ✅ Agent asks about commit after each major task
- ✅ Agent respects user's choice
- ✅ Commits are logical units of work
- ✅ Git workflow protocol followed when committing

**Fail Criteria**:
- ❌ Agent never asks about commits
- ❌ Agent commits without asking
- ❌ One giant commit at the end
```

### Test 3: Logging Standards
```markdown
**Given**: Agent writes code that needs logging
**When**: Implementing logging
**Then**: Follow these standards:
- Development: DEBUG level for detailed info
- Production: INFO level for important events only
- Log files in designated logs/ directory
- Human-readable log messages

**Test Cases**:

#### Test 3.1: Log Level Configuration
**Expected**: Code has configurable log levels

**Good Example** ✅:
```python
import logging
import os

# Configurable via environment
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(level=LOG_LEVEL)

logger = logging.getLogger(__name__)

# INFO: Important for humans
logger.info("Portfolio optimization completed successfully")

# DEBUG: Detailed for debugging (only shown in DEBUG mode)
logger.debug(f"Weights calculated: {weights}")
```

**Bad Example** ❌:
```python
import logging
logging.basicConfig(level=logging.DEBUG)  # Always DEBUG - BAD!

# Too much noise for production
logging.debug("Entering function")
logging.debug("Variable x = 5")
logging.debug("Exiting function")
```

**Validation Script**:
```bash
#!/bin/bash

echo "=== Checking Logging Standards ==="

# 1. Check for hardcoded DEBUG level
HARDCODED_DEBUG=$(grep -r "level=logging.DEBUG\|level='DEBUG'\|level=\"DEBUG\"" --include="*.py" src/ | wc -l)

if [ "$HARDCODED_DEBUG" -gt 0 ]; then
  echo "❌ FAIL: Found hardcoded DEBUG logging level"
  grep -r "level=logging.DEBUG\|level='DEBUG'\|level=\"DEBUG\"" --include="*.py" src/
  exit 1
fi

# 2. Check logs directory exists
if [ ! -d "logs" ]; then
  echo "❌ FAIL: logs/ directory does not exist"
  exit 1
fi

# 3. Check for excessive debug statements
DEBUG_COUNT=$(grep -r "logger.debug\|logging.debug" --include="*.py" src/ | wc -l)
INFO_COUNT=$(grep -r "logger.info\|logging.info" --include="*.py" src/ | wc -l)

if [ "$DEBUG_COUNT" -gt $((INFO_COUNT * 3)) ]; then
  echo "⚠️  WARN: Too many debug statements ($DEBUG_COUNT debug vs $INFO_COUNT info)"
fi

echo "✅ PASS: Logging standards check complete"
```

**Pass Criteria**:
- ✅ Log level is configurable (env var or config)
- ✅ Production uses INFO level
- ✅ Logs directory exists
- ✅ Log messages are human-readable
- ✅ DEBUG used for details, INFO for important events

**Fail Criteria**:
- ❌ Hardcoded DEBUG level in production code
- ❌ No logs directory
- ❌ Cryptic log messages
- ❌ Too much noise in INFO level
```

### Test 4: Bash Test Validation
```markdown
**Given**: Agent implements logic/math functions
**When**: Before finalizing implementation
**Then**: Agent MUST write small bash tests to verify accuracy

**Test Cases**:

#### Test 4.1: Math Accuracy Validation
**Scenario**: Agent implements compound interest calculator

**Expected Agent Behavior**:
1. Write the Python implementation
2. Write Python unit tests
3. Write bash validation test
4. Run bash test to verify math
5. Show results to user

**Example Bash Test**:
```bash
#!/bin/bash

echo "=== Testing Compound Interest Calculator ==="

# Test 1: Known values
RESULT=$(python -c "from src.calculator import compound_interest; print(compound_interest(1000, 0.05, 10))")
EXPECTED="1628.89"  # 1000 * (1.05)^10

if [ "$(echo "$RESULT - $EXPECTED" | bc)" -lt 0.01 ]; then
  echo "✅ Test 1 PASS: Compound interest accurate"
else
  echo "❌ Test 1 FAIL: Got $RESULT, expected $EXPECTED"
  exit 1
fi

# Test 2: Edge case - zero interest
RESULT=$(python -c "from src.calculator import compound_interest; print(compound_interest(1000, 0, 10))")
EXPECTED="1000.00"

if [ "$RESULT" == "$EXPECTED" ]; then
  echo "✅ Test 2 PASS: Zero interest handled correctly"
else
  echo "❌ Test 2 FAIL: Got $RESULT, expected $EXPECTED"
  exit 1
fi

echo "✅ All bash validation tests passed"
```

**Validation**:
```bash
# Check that bash test scripts exist for math/logic functions
if [ -d "scripts/validation_tests" ]; then
  TEST_COUNT=$(find scripts/validation_tests -name "*.sh" | wc -l)
  if [ "$TEST_COUNT" -gt 0 ]; then
    echo "✅ PASS: Found $TEST_COUNT bash validation tests"
  else
    echo "⚠️  WARN: No bash validation tests found"
  fi
fi
```

**Pass Criteria**:
- ✅ Bash tests written for math/logic functions
- ✅ Tests verify accuracy with known values
- ✅ Edge cases tested
- ✅ Tests are temporary (not saved to repo if just for verification)

**Fail Criteria**:
- ❌ No validation tests for complex logic
- ❌ Math functions not verified
- ❌ Dummy bash tests saved to repo
```

### Test 5: Code Organization
```markdown
**Given**: Agent modifies codebase
**When**: Rewriting functions or adding files
**Then**: Maintain clean, organized codebase

**Test Cases**:

#### Test 5.1: No Duplicate Functions
**Rule**: If rewriting a function, DELETE the old one

**Validation Script**:
```bash
#!/bin/bash

echo "=== Checking for Duplicate Functions ==="

# Find function definitions and check for duplicates
DUPLICATES=$(grep -rh "^def \|^function " --include="*.py" --include="*.js" src/ | \
             sort | uniq -d)

if [ -n "$DUPLICATES" ]; then
  echo "❌ FAIL: Found duplicate function definitions:"
  echo "$DUPLICATES"
  exit 1
else
  echo "✅ PASS: No duplicate functions found"
fi
```

#### Test 5.2: Proper File Placement
**Rule**: New files go in appropriate directories

**Directory Structure**:
```
src/
├── core/           # Core business logic
├── utils/          # Utility functions
├── models/         # Data models
├── services/       # External service integrations
├── api/            # API endpoints
└── cli/            # CLI commands

tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
└── validation/     # Validation scripts
```

**Validation**:
```bash
#!/bin/bash

echo "=== Checking File Organization ==="

# Check for misplaced files
MISPLACED=0

# Utils in wrong place
if grep -rq "def.*util\|class.*Util" src/core/ src/models/; then
  echo "⚠️  WARN: Utility functions found outside utils/ directory"
  MISPLACED=$((MISPLACED + 1))
fi

# Tests in src
if find src/ -name "test_*.py" -o -name "*_test.py" | grep -q .; then
  echo "❌ FAIL: Test files found in src/ directory"
  find src/ -name "test_*.py" -o -name "*_test.py"
  exit 1
fi

if [ "$MISPLACED" -eq 0 ]; then
  echo "✅ PASS: Files properly organized"
fi
```

#### Test 5.3: Clean Commented Code
**Rule**: Remove old commented code, don't leave it for "reference"

**Validation**:
```bash
#!/bin/bash

echo "=== Checking for Excessive Commented Code ==="

# Count lines of commented code
COMMENTED=$(grep -r "^\s*#.*" --include="*.py" src/ | wc -l)
TOTAL=$(find src/ -name "*.py" -exec cat {} \; | wc -l)
RATIO=$(echo "scale=2; $COMMENTED / $TOTAL" | bc)

if (( $(echo "$RATIO > 0.15" | bc -l) )); then
  echo "⚠️  WARN: High ratio of comments ($RATIO) - review for old commented code"
else
  echo "✅ PASS: Reasonable comment ratio"
fi
```

**Pass Criteria**:
- ✅ No duplicate functions
- ✅ Files in appropriate directories
- ✅ Old functions removed
- ✅ No excessive commented-out code
- ✅ Clean, organized structure

**Fail Criteria**:
- ❌ Multiple versions of same function
- ❌ Files in wrong directories
- ❌ Old commented code left behind
- ❌ Messy repo structure
```

### Test 6: Local Testing First
```markdown
**Given**: Code is ready for deployment
**When**: Before pushing to GitHub or CI/CD
**Then**: EVERYTHING must be tested locally first

**Test Cases**:

#### Test 6.1: Local Test Suite Passes
**Pre-Deployment Checklist**:

```bash
#!/bin/bash

echo "=========================================="
echo "  PRE-DEPLOYMENT VALIDATION"
echo "  Testing EVERYTHING locally first..."
echo "=========================================="

FAILED=0

# 1. Run all unit tests
echo "
[1/6] Running unit tests..."
python -m pytest tests/unit/ -v
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Unit tests failed"
  FAILED=$((FAILED + 1))
else
  echo "✅ PASS: Unit tests passed"
fi

# 2. Run integration tests
echo "
[2/6] Running integration tests..."
python -m pytest tests/integration/ -v
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Integration tests failed"
  FAILED=$((FAILED + 1))
else
  echo "✅ PASS: Integration tests passed"
fi

# 3. Run linting
echo "
[3/6] Running linter..."
python -m pylint src/ --fail-under=8.0
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Linting failed"
  FAILED=$((FAILED + 1))
else
  echo "✅ PASS: Linting passed"
fi

# 4. Type checking
echo "
[4/6] Running type checker..."
python -m mypy src/
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Type checking failed"
  FAILED=$((FAILED + 1))
else
  echo "✅ PASS: Type checking passed"
fi

# 5. Security scan
echo "
[5/6] Running security scan..."
python -m bandit -r src/ -ll
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Security issues found"
  FAILED=$((FAILED + 1))
else
  echo "✅ PASS: Security scan passed"
fi

# 6. Build/Package test
echo "
[6/6] Testing build..."
python -m build
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Build failed"
  FAILED=$((FAILED + 1))
else
  echo "✅ PASS: Build succeeded"
fi

# Summary
echo "
=========================================="
if [ $FAILED -eq 0 ]; then
  echo "✅ ALL PRE-DEPLOYMENT CHECKS PASSED"
  echo "Safe to proceed with deployment"
  echo "=========================================="
  exit 0
else
  echo "❌ $FAILED CHECK(S) FAILED"
  echo "Fix issues before deploying"
  echo "=========================================="
  exit 1
fi
```

**Pass Criteria**:
- ✅ All tests pass locally
- ✅ Linting passes
- ✅ Type checking passes
- ✅ Security scan clean
- ✅ Build succeeds
- ✅ Manual testing completed

**Fail Criteria**:
- ❌ Pushing without running tests
- ❌ "It works on my machine" without verification
- ❌ Skipping integration tests
- ❌ Deploying with known issues
```

### Test 7: Production Code Standards
```markdown
**Given**: Agent writes code
**When**: Implementing any feature
**Then**: ONLY production-ready code, NO shortcuts or dummy code

**Test Cases**:

#### Test 7.1: No Placeholder Code
**Forbidden Patterns**:
```python
# ❌ BAD - Placeholder
def process_data(data):
    # TODO: Implement this
    pass

# ❌ BAD - Dummy return
def calculate_risk():
    return 0.5  # Dummy value for now

# ❌ BAD - Hardcoded test data
users = [
    {"name": "Test User", "email": "test@test.com"}  # Remove before production
]

# ✅ GOOD - Real implementation
def process_data(data):
    """Process incoming data and return validated results."""
    validated = validate_input(data)
    processed = transform_data(validated)
    return processed
```

**Validation Script**:
```bash
#!/bin/bash

echo "=== Checking for Non-Production Code ==="

ISSUES=0

# Check for TODO/FIXME in src (ok in tests)
TODOS=$(grep -r "TODO\|FIXME\|XXX\|HACK" --include="*.py" src/ | wc -l)
if [ "$TODOS" -gt 0 ]; then
  echo "❌ FAIL: Found $TODOS TODO/FIXME markers in production code"
  grep -r "TODO\|FIXME\|XXX\|HACK" --include="*.py" src/
  ISSUES=$((ISSUES + 1))
fi

# Check for pass-only functions
PASS_FUNCTIONS=$(grep -A 1 "^def " src/**/*.py | grep -c "^\s*pass\s*$")
if [ "$PASS_FUNCTIONS" -gt 0 ]; then
  echo "❌ FAIL: Found $PASS_FUNCTIONS empty (pass-only) functions"
  ISSUES=$((ISSUES + 1))
fi

# Check for dummy/test data
DUMMY=$(grep -ri "dummy\|test.*data\|placeholder" --include="*.py" src/ | wc -l)
if [ "$DUMMY" -gt 0 ]; then
  echo "⚠️  WARN: Found $DUMMY potential dummy/test data references"
  grep -ri "dummy\|test.*data\|placeholder" --include="*.py" src/
fi

if [ "$ISSUES" -eq 0 ]; then
  echo "✅ PASS: No placeholder code found"
else
  exit 1
fi
```

**Pass Criteria**:
- ✅ All functions fully implemented
- ✅ No TODO/FIXME in production code
- ✅ No dummy data or placeholder values
- ✅ Real error handling
- ✅ Production-ready quality

**Fail Criteria**:
- ❌ Placeholder functions
- ❌ Hardcoded test data
- ❌ "Quick hack" solutions
- ❌ Incomplete implementations
```

### Test 8: User Decision Points
```markdown
**Given**: Agent encounters a decision point
**When**: Multiple valid approaches exist
**Then**: Present options, explain trade-offs, let user decide

**Test Cases**:

#### Test 8.1: Option Presentation Format
**Expected Format**:

```
I need your input on [specific decision].

Here are the options:

**Option 1: [Approach A]**
Pros:
- [Benefit 1]
- [Benefit 2]
Cons:
- [Drawback 1]
- [Drawback 2]
Best for: [Use case]

**Option 2: [Approach B]**
Pros:
- [Benefit 1]
- [Benefit 2]
Cons:
- [Drawback 1]
- [Drawback 2]
Best for: [Use case]

**My Recommendation**: [Option X] because [reasoning]

Which would you prefer? (1/2)
```

**Pass Criteria**:
- ✅ At least 2 clear options presented
- ✅ Pros/cons explained for each
- ✅ Use cases identified
- ✅ Recommendation provided with reasoning
- ✅ Agent waits for user response

**Fail Criteria**:
- ❌ Agent makes decision without asking
- ❌ Options not clearly explained
- ❌ No recommendation provided
- ❌ Vague or confusing presentation
```

### Test 9: Copy-Paste Ready Commands
```markdown
**Given**: Agent provides commands for user to run
**When**: Formatting command output
**Then**: Commands must be directly copy-pasteable (no extra spaces)

**Test Cases**:

#### Test 9.1: Command Formatting
**Bad Format** ❌:
```
   python -m pytest tests/     ← Extra leading spaces!
```

**Good Format** ✅:
```bash
python -m pytest tests/
```

**Multi-line Commands** ✅:
```bash
cd /Users/vandanchopra/Vandan_Personal_Folder/CODE_STUFF/Projects/MathematricksTrader && \
source venv/bin/activate && \
python -m pytest tests/unit/ -v
```

**With Explanation** ✅:
```
Run the following command to execute tests:

```bash
python -m pytest tests/unit/ -v
```

This will run all unit tests with verbose output.
```

**Pass Criteria**:
- ✅ No leading/trailing spaces in commands
- ✅ Code blocks properly formatted
- ✅ Multi-line commands use proper line continuation
- ✅ Commands are immediately runnable

**Fail Criteria**:
- ❌ Extra spaces that break copy-paste
- ❌ Commands mixed with prose
- ❌ Missing code block formatting
```

---

## Integration Test: Complete Development Workflow

### End-to-End Scenario
```markdown
**Given**: User requests "Add portfolio optimization feature"
**When**: Agent completes full workflow
**Then**: All 9 rules must be followed

**Expected Flow**:

1. ✅ Agent writes tests first, gets approval
2. ✅ Agent implements feature (production-ready, no shortcuts)
3. ✅ Agent writes bash validation for math accuracy
4. ✅ Agent organizes files properly (removes old code)
5. ✅ Agent configures logging (INFO for production)
6. ✅ Agent runs all tests locally
7. ✅ Agent asks: "Want to commit before next task?"
8. ✅ If unclear direction, agent presents options
9. ✅ All commands provided are copy-paste ready

**Validation**:
- Check git log for logical commits
- Check test files created before implementation
- Check no placeholder code in src/
- Check proper logging configuration
- Check files organized correctly
```

### Test 10: Virtual Environment Management
```markdown
**Given**: Agent works on Python projects (aitutor, ipop)
**When**: Setting up or running Python code
**Then**: Use correct virtual environment in `/Users/gagan/Desktop/gagan_projects/venv`

**Test Cases**:

#### Test 10.1: Verify Correct venv Path
**Projects**:
- aitutor: https://github.com/vandanchopra/aitutor
- ipop: https://github.com/gagan114662/ipop

**Expected venv Location**: `/Users/gagan/Desktop/gagan_projects/venv`

**Validation Script**:
```bash
#!/bin/bash

echo "=== Checking Virtual Environment Setup ==="

VENV_PATH="/Users/gagan/Desktop/gagan_projects/venv"

# 1. Check venv exists
if [ ! -d "$VENV_PATH" ]; then
  echo "❌ FAIL: Virtual environment does not exist at $VENV_PATH"
  echo "Creating venv..."
  python3 -m venv "$VENV_PATH"

  if [ $? -eq 0 ]; then
    echo "✅ Created venv successfully"
  else
    echo "❌ Failed to create venv"
    exit 1
  fi
else
  echo "✅ PASS: Virtual environment exists"
fi

# 2. Check venv has Python
if [ -f "$VENV_PATH/bin/python" ]; then
  echo "✅ PASS: Python interpreter found"
  PYTHON_VERSION=$("$VENV_PATH/bin/python" --version)
  echo "   Python version: $PYTHON_VERSION"
else
  echo "❌ FAIL: Python interpreter not found in venv"
  exit 1
fi

# 3. Check pip is available
if [ -f "$VENV_PATH/bin/pip" ]; then
  echo "✅ PASS: pip found"
  PIP_VERSION=$("$VENV_PATH/bin/pip" --version)
  echo "   pip version: $PIP_VERSION"
else
  echo "❌ FAIL: pip not found in venv"
  exit 1
fi

echo "
✅ Virtual environment setup validated"
```

#### Test 10.2: Project-Specific Dependencies
**For each project (aitutor, ipop)**:

```bash
#!/bin/bash

echo "=== Checking Project Dependencies ==="

VENV_PATH="/Users/gagan/Desktop/gagan_projects/venv"
PROJECT_PATH="$1"  # Pass project path as argument

if [ -z "$PROJECT_PATH" ]; then
  echo "Usage: $0 <project_path>"
  exit 1
fi

cd "$PROJECT_PATH" || exit 1

# 1. Check requirements.txt exists
if [ ! -f "requirements.txt" ]; then
  echo "❌ FAIL: requirements.txt not found in $PROJECT_PATH"
  exit 1
fi

# 2. Install dependencies
echo "Installing dependencies from requirements.txt..."
"$VENV_PATH/bin/pip" install -r requirements.txt -q

if [ $? -eq 0 ]; then
  echo "✅ PASS: Dependencies installed successfully"
else
  echo "❌ FAIL: Failed to install dependencies"
  exit 1
fi

# 3. Verify key packages installed
echo "Verifying installed packages..."
"$VENV_PATH/bin/pip" list

echo "✅ Project dependencies validated"
```

#### Test 10.3: Ensure Correct Python is Used
**Rule**: Always use venv Python, not system Python

**Validation**:
```bash
#!/bin/bash

echo "=== Verifying Python Interpreter Usage ==="

VENV_PATH="/Users/gagan/Desktop/gagan_projects/venv"

# Check which python is being used
ACTIVE_PYTHON=$(which python)
EXPECTED_PYTHON="$VENV_PATH/bin/python"

if [ "$ACTIVE_PYTHON" = "$EXPECTED_PYTHON" ] || [ "$ACTIVE_PYTHON" = "$(realpath $EXPECTED_PYTHON)" ]; then
  echo "✅ PASS: Using venv Python: $ACTIVE_PYTHON"
else
  echo "⚠️  WARN: Not using venv Python"
  echo "   Active: $ACTIVE_PYTHON"
  echo "   Expected: $EXPECTED_PYTHON"
  echo "   Activate venv with: source $VENV_PATH/bin/activate"
fi

# Check Python path in scripts
if grep -rq "#!/usr/bin/env python\|#!/usr/bin/python" . --include="*.py" 2>/dev/null; then
  echo "⚠️  WARN: Found system Python shebangs - consider using venv Python"
fi
```

**Commands for User**:
```bash
# Activate venv
source /Users/gagan/Desktop/gagan_projects/venv/bin/activate

# Run Python code
python script.py

# Or use venv Python directly
/Users/gagan/Desktop/gagan_projects/venv/bin/python script.py

# Install packages
pip install package_name
```

**Pass Criteria**:
- ✅ venv exists at correct path
- ✅ Python and pip available in venv
- ✅ Project dependencies installed in venv
- ✅ venv Python used (not system Python)

**Fail Criteria**:
- ❌ venv doesn't exist
- ❌ Using system Python instead of venv
- ❌ Dependencies not installed
```

### Test 11: To-Do List File Tracking
```markdown
**Given**: Agent is working on tasks
**When**: Starting work, completing tasks, or changing focus
**Then**: Maintain to-do list in a dedicated file and keep it updated

**Test Cases**:

#### Test 11.1: To-Do List File Exists
**Expected Location**: `TODO.md` or `TASKS.md` in project root

**Validation Script**:
```bash
#!/bin/bash

echo "=== Checking To-Do List File ==="

# Check for todo file
if [ -f "TODO.md" ]; then
  TODO_FILE="TODO.md"
  echo "✅ PASS: Found TODO.md"
elif [ -f "TASKS.md" ]; then
  TODO_FILE="TASKS.md"
  echo "✅ PASS: Found TASKS.md"
else
  echo "❌ FAIL: No to-do list file found (TODO.md or TASKS.md)"
  echo "Creating TODO.md..."
  cat > TODO.md << 'EOF'
# Project To-Do List

## In Progress
- [ ] Task currently being worked on

## Pending
- [ ] Next task to do
- [ ] Another pending task

## Completed
- [x] Completed task with timestamp

---
Last Updated: $(date)
EOF
  echo "✅ Created TODO.md"
  TODO_FILE="TODO.md"
fi

# Check file is not empty
if [ ! -s "$TODO_FILE" ]; then
  echo "❌ FAIL: To-do list file is empty"
  exit 1
fi

echo "✅ To-do list file validated"
```

#### Test 11.2: To-Do List Format
**Expected Format**:

```markdown
# Project To-Do List

## In Progress
- [x] Task being worked on right now
  - Started: 2024-01-15
  - Status: 60% complete

## Pending
- [ ] Next high priority task
- [ ] Medium priority task
- [ ] Low priority task

## Completed
- [x] Completed task 1
  - Completed: 2024-01-14
  - Notes: All tests passed
- [x] Completed task 2
  - Completed: 2024-01-13

## Blocked
- [ ] Task blocked by external dependency
  - Reason: Waiting for API access

---
Last Updated: 2024-01-15 14:30
```

**Validation**:
```bash
#!/bin/bash

echo "=== Validating To-Do List Format ==="

TODO_FILE="TODO.md"

if [ ! -f "$TODO_FILE" ]; then
  echo "❌ FAIL: $TODO_FILE not found"
  exit 1
fi

ISSUES=0

# Check for required sections
SECTIONS=("In Progress" "Pending" "Completed")

for section in "${SECTIONS[@]}"; do
  if ! grep -qi "## $section" "$TODO_FILE"; then
    echo "⚠️  WARN: Missing '## $section' section"
    ISSUES=$((ISSUES + 1))
  fi
done

# Check for task items (checkbox format)
TASK_COUNT=$(grep -c "^- \[[ x]\]" "$TODO_FILE")

if [ "$TASK_COUNT" -eq 0 ]; then
  echo "⚠️  WARN: No tasks found in checkbox format"
  ISSUES=$((ISSUES + 1))
else
  echo "✅ Found $TASK_COUNT tasks"
fi

# Check for last updated timestamp
if ! grep -qi "Last Updated" "$TODO_FILE"; then
  echo "⚠️  WARN: No 'Last Updated' timestamp found"
fi

if [ "$ISSUES" -eq 0 ]; then
  echo "✅ PASS: To-do list format validated"
else
  echo "⚠️  $ISSUES format issues found"
fi
```

#### Test 11.3: To-Do List is Updated
**Rule**: Update to-do list when completing tasks or starting new ones

**Validation**:
```bash
#!/bin/bash

echo "=== Checking To-Do List Updates ==="

TODO_FILE="TODO.md"

# Get last modification time
LAST_MODIFIED=$(stat -f %m "$TODO_FILE" 2>/dev/null || stat -c %Y "$TODO_FILE" 2>/dev/null)
CURRENT_TIME=$(date +%s)
HOURS_SINCE_UPDATE=$(( (CURRENT_TIME - LAST_MODIFIED) / 3600 ))

if [ "$HOURS_SINCE_UPDATE" -gt 24 ]; then
  echo "⚠️  WARN: To-do list not updated in $HOURS_SINCE_UPDATE hours"
  echo "   Last modified: $(date -r $LAST_MODIFIED)"
else
  echo "✅ PASS: To-do list updated recently (${HOURS_SINCE_UPDATE}h ago)"
fi

# Check for "In Progress" tasks
IN_PROGRESS=$(grep -A 10 "## In Progress" "$TODO_FILE" | grep -c "^- \[[ x]\]")

if [ "$IN_PROGRESS" -eq 0 ]; then
  echo "⚠️  WARN: No tasks marked as 'In Progress'"
else
  echo "✅ $IN_PROGRESS task(s) in progress"
fi
```

#### Test 11.4: Agent Updates To-Do List
**Expected Behavior**:

When agent starts work:
```markdown
## In Progress
- [x] Write tests for development workflow features
  - Started: 2024-01-15 14:00
  - Status: Writing test cases
```

When agent completes task:
```markdown
## Completed
- [x] Write tests for development workflow features
  - Completed: 2024-01-15 15:30
  - Result: 11 test scenarios created in test_development_workflow.md
```

**Validation Command**:
```bash
# Show current to-do list status
cat TODO.md

# Or show summary
echo "=== To-Do List Summary ==="
echo "In Progress: $(grep -A 20 '## In Progress' TODO.md | grep -c '- \[ \]\|x\]')"
echo "Pending: $(grep -A 50 '## Pending' TODO.md | grep -c '- \[ \]')"
echo "Completed: $(grep -A 100 '## Completed' TODO.md | grep -c '- \[x\]')"
```

**Pass Criteria**:
- ✅ TODO.md or TASKS.md exists
- ✅ File has proper structure (In Progress, Pending, Completed)
- ✅ Tasks use checkbox format `- [ ]` or `- [x]`
- ✅ File is updated regularly (< 24 hours)
- ✅ Current work is marked "In Progress"
- ✅ Completed tasks moved to "Completed" section

**Fail Criteria**:
- ❌ No to-do list file
- ❌ File not updated in days
- ❌ No current task marked
- ❌ Tasks not moved to completed
```

---

## Test Execution

**Run All Tests**:
```bash
cd /Users/gagan/Desktop/gagan_projects/agency_agents
bash scripts/validation_tests/run_all_workflow_tests.sh
```

**Individual Test Runs**:
```bash
# Test 1: Pre-work test approval
bash tests/validation/test_1_pre_work_tests.sh

# Test 2: Git commit checkpoints
bash tests/validation/test_2_git_checkpoints.sh

# Test 3: Logging standards
bash tests/validation/test_3_logging.sh

# Test 4: Bash validation
bash tests/validation/test_4_bash_tests.sh

# Test 5: Code organization
bash tests/validation/test_5_organization.sh

# Test 6: Local testing first
bash tests/validation/test_6_local_testing.sh

# Test 7: Production code
bash tests/validation/test_7_production_code.sh

# Test 8: User decisions
bash tests/validation/test_8_user_decisions.sh

# Test 9: Command formatting
bash tests/validation/test_9_commands.sh

# Test 10: Virtual environment management
bash tests/validation/test_10_venv.sh

# Test 11: To-do list tracking
bash tests/validation/test_11_todo_list.sh
```

**Success Criteria**: All 11 tests pass before deployment
