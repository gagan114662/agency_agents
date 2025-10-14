#!/bin/bash

#
# Bash Validation Script for Agent Routing System
# Tests routing accuracy with known inputs/outputs
#
# Following Rule 4: Bash Test Validation for Math/Logic
# This provides independent verification of routing logic
#

set -e  # Exit on error

echo "🧪 Starting Agent Router Validation Tests..."
echo "=============================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASS_COUNT=0
FAIL_COUNT=0

# Helper function to test routing
test_routing() {
    local test_name="$1"
    local task="$2"
    local expected_agent="$3"

    echo -n "Testing: $test_name... "

    # Call Python router (will be implemented)
    RESULT=$(python3 -c "
from agent_router.router import AgentRouter
router = AgentRouter()
agent = router.select_agent('$task')
print(agent['name'])
" 2>&1)

    if [ "$RESULT" = "$expected_agent" ]; then
        echo -e "${GREEN}✅ PASS${NC}"
        PASS_COUNT=$((PASS_COUNT + 1))
        return 0
    else
        echo -e "${RED}❌ FAIL${NC}"
        echo "   Expected: $expected_agent"
        echo "   Got: $RESULT"
        FAIL_COUNT=$((FAIL_COUNT + 1))
        return 1
    fi
}

# Test Category 1: Frontend Tasks
echo "📱 Testing Frontend Task Routing"
echo "--------------------------------"
test_routing "React Dashboard" "Build a React dashboard with authentication" "Frontend Developer"
test_routing "Vue Component" "Create Vue.js component library" "Frontend Developer"
test_routing "CSS Styling" "Fix responsive CSS on mobile devices" "Frontend Developer"
test_routing "UI Implementation" "Implement navigation menu with animations" "Frontend Developer"
echo ""

# Test Category 2: Backend Tasks
echo "🔧 Testing Backend Task Routing"
echo "--------------------------------"
test_routing "REST API" "Design REST API for user management" "Backend Architect"
test_routing "Database Schema" "Create PostgreSQL database schema" "Backend Architect"
test_routing "Authentication" "Implement JWT authentication system" "Backend Architect"
test_routing "Microservices" "Design microservices architecture" "Backend Architect"
echo ""

# Test Category 3: AI/ML Tasks
echo "🤖 Testing AI/ML Task Routing"
echo "--------------------------------"
test_routing "Sentiment Analysis" "Build sentiment analysis model" "AI Engineer"
test_routing "RAG System" "Implement RAG with vector database" "AI Engineer"
test_routing "Recommendation" "Create recommendation engine" "AI Engineer"
test_routing "LLM Fine-tuning" "Fine-tune LLM for customer support" "AI Engineer"
echo ""

# Test Category 4: Design Tasks
echo "🎨 Testing Design Task Routing"
echo "--------------------------------"
test_routing "Design System" "Create design system with components" "UI Designer"
test_routing "Component Library" "Design component library in Figma" "UI Designer"
test_routing "Typography" "Establish typography and color tokens" "UI Designer"
test_routing "User Flow" "Design user flow for checkout process" "UX Architect"
echo ""

# Test Category 5: Testing Tasks
echo "🧪 Testing QA Task Routing"
echo "--------------------------------"
test_routing "Production Ready" "Validate application is production ready" "Reality Checker"
test_routing "Integration Tests" "Run integration tests and QA validation" "Reality Checker"
test_routing "API Testing" "Test API endpoints for correctness" "API Tester"
test_routing "Performance" "Benchmark application performance" "Performance Benchmarker"
echo ""

# Test Category 6: Multi-Agent Detection
echo "🔀 Testing Multi-Agent Detection"
echo "--------------------------------"

echo -n "Testing: Full-stack app detection... "
RESULT=$(python3 -c "
from agent_router.router import AgentRouter
router = AgentRouter()
result = router.analyze_task('Build full-stack app with React and Node.js')
print('multi' if result['is_multi_agent'] else 'single')
" 2>&1)

if [ "$RESULT" = "multi" ]; then
    echo -e "${GREEN}✅ PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}❌ FAIL${NC}"
    echo "   Expected: multi-agent task"
    echo "   Got: $RESULT"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

echo ""

# Test Category 7: Default Agent (Ambiguous Tasks)
echo "🎯 Testing Default Agent Routing"
echo "--------------------------------"
test_routing "Ambiguous Task 1" "Help me with my project" "Senior Developer"
test_routing "Ambiguous Task 2" "Fix this issue" "Senior Developer"
test_routing "Ambiguous Task 3" "General refactoring needed" "Senior Developer"
echo ""

# Test Category 8: Edge Cases
echo "⚠️  Testing Edge Cases"
echo "--------------------------------"

# Test empty task
echo -n "Testing: Empty task... "
RESULT=$(python3 -c "
from agent_router.router import AgentRouter
router = AgentRouter()
agent = router.select_agent('')
print(agent['name'])
" 2>&1)

if [ "$RESULT" = "Senior Developer" ]; then
    echo -e "${GREEN}✅ PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}❌ FAIL${NC}"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test case sensitivity
echo -n "Testing: Case insensitive matching... "
RESULT=$(python3 -c "
from agent_router.router import AgentRouter
router = AgentRouter()
agent1 = router.select_agent('Build a REACT app')
agent2 = router.select_agent('Build a react app')
print('pass' if agent1['name'] == agent2['name'] == 'Frontend Developer' else 'fail')
" 2>&1)

if [ "$RESULT" = "pass" ]; then
    echo -e "${GREEN}✅ PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}❌ FAIL${NC}"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

echo ""

# Test Category 9: Performance
echo "⚡ Testing Performance"
echo "--------------------------------"

echo -n "Testing: Routing completes under 1 second... "
START_TIME=$(python3 -c "import time; print(time.time())")

python3 -c "
from agent_router.router import AgentRouter
router = AgentRouter()
agent = router.select_agent('Build a complex full-stack application with multiple features')
" 2>&1 > /dev/null

END_TIME=$(python3 -c "import time; print(time.time())")
DURATION=$(python3 -c "print($END_TIME - $START_TIME)")

if (( $(python3 -c "print(1 if $DURATION < 1.0 else 0)") )); then
    echo -e "${GREEN}✅ PASS${NC} (${DURATION}s)"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}❌ FAIL${NC} (${DURATION}s - too slow)"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

echo ""

# Test Category 10: Configuration Validation
echo "📋 Testing Configuration"
echo "--------------------------------"

echo -n "Testing: Config file exists... "
if [ -f "/Users/gaganarora/Desktop/gagan_projects/Agency/agency_agents/agent_router/agents.yaml" ]; then
    echo -e "${GREEN}✅ PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}❌ FAIL${NC}"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

echo -n "Testing: All agent files exist... "
MISSING_FILES=$(python3 -c "
from agent_router.config import AgentConfig
import os
config = AgentConfig()
missing = []
for agent in config.get_all_agents():
    if not os.path.exists(agent['file_path']):
        missing.append(agent['name'])
print(len(missing))
" 2>&1)

if [ "$MISSING_FILES" = "0" ]; then
    echo -e "${GREEN}✅ PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}❌ FAIL${NC} ($MISSING_FILES missing files)"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

echo ""

# Final Summary
echo "=============================================="
echo "📊 Test Results Summary"
echo "=============================================="
echo ""
echo -e "Total Tests: $((PASS_COUNT + FAIL_COUNT))"
echo -e "${GREEN}Passed: $PASS_COUNT${NC}"
echo -e "${RED}Failed: $FAIL_COUNT${NC}"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    echo ""
    exit 0
else
    echo -e "${RED}❌ Some tests failed. Please fix issues before proceeding.${NC}"
    echo ""
    exit 1
fi
