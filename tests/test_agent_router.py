"""
Test suite for Agent Router system
Tests the core routing logic that determines which agent to invoke for a given task

Following Test-First Development Protocol:
- These tests are written BEFORE implementation
- Tests import from actual modules (not yet implemented)
- Tests will initially fail, then implementation will make them pass
"""

import pytest
from agent_router.router import AgentRouter
from agent_router.config import AgentConfig


class TestAgentRouterInitialization:
    """Test router initialization and configuration loading"""

    def test_router_initializes_successfully(self):
        """Router should initialize with default config"""
        router = AgentRouter()
        assert router is not None
        assert router.config is not None

    def test_router_loads_all_agents_from_config(self):
        """Router should load all 37 agents from YAML config"""
        router = AgentRouter()
        agents = router.get_available_agents()

        # Should have all agent categories
        assert 'engineering' in agents
        assert 'design' in agents
        assert 'testing' in agents
        assert 'marketing' in agents
        assert 'product' in agents
        assert 'support' in agents

        # Should have at least 37 total agents
        total_agents = sum(len(category_agents) for category_agents in agents.values())
        assert total_agents >= 37

    def test_router_validates_agent_config_on_load(self):
        """Router should validate agent config structure on load"""
        router = AgentRouter()

        # All agents should have required fields
        for agent in router.get_all_agents():
            assert 'name' in agent
            assert 'description' in agent
            assert 'keywords' in agent
            assert 'file_path' in agent
            assert isinstance(agent['keywords'], list)


class TestAgentSelectionLogic:
    """Test the core agent selection algorithm"""

    def test_frontend_task_routes_to_frontend_developer(self):
        """Frontend tasks should route to Frontend Developer agent"""
        router = AgentRouter()

        test_cases = [
            "Build a React dashboard with user authentication",
            "Create a Vue.js component library",
            "Implement responsive navigation menu",
            "Fix CSS styling issues on mobile",
            "Add dark mode toggle to the UI"
        ]

        for task in test_cases:
            agent = router.select_agent(task)
            assert agent['name'] == 'Frontend Developer'
            assert agent['category'] == 'engineering'

    def test_backend_task_routes_to_backend_architect(self):
        """Backend tasks should route to Backend Architect agent"""
        router = AgentRouter()

        test_cases = [
            "Design a REST API for user management",
            "Optimize database queries for performance",
            "Implement JWT authentication system",
            "Create microservices architecture",
            "Set up PostgreSQL database schema"
        ]

        for task in test_cases:
            agent = router.select_agent(task)
            assert agent['name'] == 'Backend Architect'
            assert agent['category'] == 'engineering'

    def test_ai_task_routes_to_ai_engineer(self):
        """AI/ML tasks should route to AI Engineer agent"""
        router = AgentRouter()

        test_cases = [
            "Build a sentiment analysis model",
            "Implement RAG system with vector database",
            "Create recommendation engine using collaborative filtering",
            "Fine-tune LLM for customer support",
            "Deploy machine learning model to production"
        ]

        for task in test_cases:
            agent = router.select_agent(task)
            assert agent['name'] == 'AI Engineer'
            assert agent['category'] == 'engineering'

    def test_design_task_routes_to_ui_designer(self):
        """UI design tasks should route to UI Designer agent"""
        router = AgentRouter()

        test_cases = [
            "Create a design system for the application",
            "Design component library with Figma",
            "Establish typography and color tokens",
            "Create responsive grid system",
            "Design dark mode theme"
        ]

        for task in test_cases:
            agent = router.select_agent(task)
            assert agent['name'] == 'UI Designer'
            assert agent['category'] == 'design'

    def test_testing_task_routes_to_reality_checker(self):
        """Testing/QA tasks should route to Reality Checker agent"""
        router = AgentRouter()

        test_cases = [
            "Validate the application is production ready",
            "Run integration tests and QA validation",
            "Check if all specifications are implemented",
            "Verify cross-browser compatibility",
            "Test complete user journeys"
        ]

        for task in test_cases:
            agent = router.select_agent(task)
            assert agent['name'] == 'Reality Checker'
            assert agent['category'] == 'testing'

    def test_ambiguous_task_defaults_to_senior_developer(self):
        """Ambiguous tasks should default to Senior Developer"""
        router = AgentRouter()

        test_cases = [
            "Help me with my project",
            "Fix this bug",
            "Improve the code",
            "Make it better",
            "General refactoring needed"
        ]

        for task in test_cases:
            agent = router.select_agent(task)
            assert agent['name'] == 'Senior Developer'
            assert agent['category'] == 'engineering'


class TestMultiAgentDetection:
    """Test detection of tasks requiring multiple agents"""

    def test_detects_frontend_backend_combination(self):
        """Should detect tasks requiring both frontend and backend"""
        router = AgentRouter()

        task = "Build a full-stack dashboard with React frontend and Node.js API"
        result = router.analyze_task(task)

        assert result['is_multi_agent'] is True
        assert len(result['required_agents']) >= 2
        assert 'Frontend Developer' in [a['name'] for a in result['required_agents']]
        assert 'Backend Architect' in [a['name'] for a in result['required_agents']]

    def test_detects_design_engineering_combination(self):
        """Should detect tasks requiring design and engineering"""
        router = AgentRouter()

        task = "Design and implement a component library with React"
        result = router.analyze_task(task)

        assert result['is_multi_agent'] is True
        agent_names = [a['name'] for a in result['required_agents']]
        assert 'UI Designer' in agent_names or 'UX Architect' in agent_names
        assert 'Frontend Developer' in agent_names

    def test_single_agent_task_detected_correctly(self):
        """Should detect single-agent tasks correctly"""
        router = AgentRouter()

        task = "Fix the CSS styling on the homepage"
        result = router.analyze_task(task)

        assert result['is_multi_agent'] is False
        assert len(result['required_agents']) == 1
        assert result['required_agents'][0]['name'] == 'Frontend Developer'


class TestAgentPriorityOrdering:
    """Test priority ordering when multiple agents could handle a task"""

    def test_primary_agent_selected_first(self):
        """Primary agent should be selected first for multi-keyword tasks"""
        router = AgentRouter()

        # Task has both API and database keywords, but API is primary
        task = "Create REST API endpoints for database operations"
        agent = router.select_agent(task)

        assert agent['name'] == 'Backend Architect'

    def test_confidence_scores_calculated(self):
        """Router should calculate confidence scores for agent selection"""
        router = AgentRouter()

        task = "Build a React component"
        result = router.analyze_task(task)

        assert 'confidence_score' in result
        assert 0.0 <= result['confidence_score'] <= 1.0
        assert result['confidence_score'] > 0.7  # High confidence for clear task


class TestAgentMetadataRetrieval:
    """Test retrieval of agent metadata and information"""

    def test_get_agent_by_name(self):
        """Should retrieve agent details by name"""
        router = AgentRouter()

        agent = router.get_agent_by_name('Frontend Developer')

        assert agent is not None
        assert agent['name'] == 'Frontend Developer'
        assert agent['category'] == 'engineering'
        assert 'keywords' in agent
        assert 'file_path' in agent

    def test_get_agent_persona_file_path(self):
        """Should return correct path to agent .md file"""
        router = AgentRouter()

        agent = router.get_agent_by_name('Frontend Developer')
        expected_path = '/Users/gaganarora/Desktop/gagan_projects/Agency/agency_agents/engineering/engineering-frontend-developer.md'

        assert agent['file_path'] == expected_path

    def test_get_agents_by_category(self):
        """Should retrieve all agents in a category"""
        router = AgentRouter()

        engineering_agents = router.get_agents_by_category('engineering')

        assert len(engineering_agents) >= 7
        agent_names = [a['name'] for a in engineering_agents]
        assert 'Frontend Developer' in agent_names
        assert 'Backend Architect' in agent_names
        assert 'AI Engineer' in agent_names


class TestRoutingEdgeCases:
    """Test edge cases and error handling"""

    def test_empty_task_returns_senior_developer(self):
        """Empty task should default to Senior Developer"""
        router = AgentRouter()

        agent = router.select_agent("")
        assert agent['name'] == 'Senior Developer'

    def test_very_long_task_processes_correctly(self):
        """Very long task descriptions should be processed"""
        router = AgentRouter()

        task = "Build " + "a React component " * 100
        agent = router.select_agent(task)

        assert agent is not None
        assert agent['name'] == 'Frontend Developer'

    def test_special_characters_handled(self):
        """Tasks with special characters should be handled"""
        router = AgentRouter()

        task = "Create API with $pecial ch@racters & symbols!"
        agent = router.select_agent(task)

        assert agent is not None
        assert agent['category'] == 'engineering'

    def test_case_insensitive_matching(self):
        """Keyword matching should be case-insensitive"""
        router = AgentRouter()

        tasks = [
            "Build a REACT dashboard",
            "Build a react dashboard",
            "Build a React dashboard"
        ]

        for task in tasks:
            agent = router.select_agent(task)
            assert agent['name'] == 'Frontend Developer'


class TestCoordinationPlanGeneration:
    """Test multi-agent coordination plan generation"""

    def test_generates_coordination_plan_for_multi_agent_task(self):
        """Should generate coordination plan for multi-agent tasks"""
        router = AgentRouter()

        task = "Build full-stack e-commerce platform with React and Node.js"
        plan = router.generate_coordination_plan(task)

        assert plan is not None
        assert 'agents' in plan
        assert 'sequence' in plan
        assert 'handoff_points' in plan
        assert len(plan['agents']) >= 2

    def test_coordination_sequence_is_logical(self):
        """Coordination sequence should follow logical order"""
        router = AgentRouter()

        task = "Design and build authentication system"
        plan = router.generate_coordination_plan(task)

        # Design should come before implementation
        sequence = plan['sequence']
        design_index = next(i for i, step in enumerate(sequence) if 'design' in step.lower())
        impl_index = next(i for i, step in enumerate(sequence) if 'implement' in step.lower() or 'build' in step.lower())

        assert design_index < impl_index


class TestProtocolAdherence:
    """Test that routing system enforces protocol adherence"""

    def test_all_agents_require_requirements_gathering(self):
        """All agents should require requirements gathering first"""
        router = AgentRouter()

        for agent in router.get_all_agents():
            protocols = router.get_agent_protocols(agent['name'])
            assert 'requirements_gathering_first' in protocols
            assert protocols['requirements_gathering_first'] is True

    def test_all_agents_require_test_first_development(self):
        """All agents should require test-first development"""
        router = AgentRouter()

        for agent in router.get_all_agents():
            protocols = router.get_agent_protocols(agent['name'])
            assert 'test_first_development' in protocols
            assert protocols['test_first_development'] is True

    def test_all_agents_follow_11_rules(self):
        """All agents should follow all 11 workflow rules"""
        router = AgentRouter()

        for agent in router.get_all_agents():
            protocols = router.get_agent_protocols(agent['name'])
            assert 'workflow_rules' in protocols
            assert protocols['workflow_rules']['total_rules'] == 11


class TestPerformanceAndScaling:
    """Test performance and scalability"""

    def test_routing_completes_under_1_second(self):
        """Agent selection should complete under 1 second"""
        import time
        router = AgentRouter()

        task = "Build a complex full-stack application"
        start = time.time()
        agent = router.select_agent(task)
        duration = time.time() - start

        assert duration < 1.0
        assert agent is not None

    def test_handles_100_consecutive_requests(self):
        """Router should handle many consecutive requests"""
        router = AgentRouter()

        tasks = [f"Build feature {i}" for i in range(100)]

        for task in tasks:
            agent = router.select_agent(task)
            assert agent is not None


# Pytest fixtures
@pytest.fixture
def router():
    """Provide a fresh router instance for each test"""
    return AgentRouter()


@pytest.fixture
def sample_tasks():
    """Provide sample tasks for testing"""
    return {
        'frontend': "Build a React dashboard",
        'backend': "Create REST API",
        'ai': "Build sentiment analysis model",
        'design': "Create design system",
        'testing': "Run QA validation",
        'ambiguous': "Help with project"
    }
