"""
Test suite for Agent Personality Loading
Tests loading, parsing, and using agent personality from .md files

Following Test-First Development Protocol:
- Tests import from actual modules (not yet implemented)
- Tests verify personality adoption and communication style
"""

import pytest
import os
from agent_router.router import AgentRouter
from agent_router.personality import AgentPersonality


class TestPersonalityFileLoading:
    """Test loading agent personality from .md files"""

    def test_load_personality_from_md_file(self):
        """Should load agent personality from .md file"""
        personality = AgentPersonality()

        frontend_dev = personality.load_agent('Frontend Developer')

        assert frontend_dev is not None
        assert 'name' in frontend_dev
        assert 'description' in frontend_dev
        assert 'core_mission' in frontend_dev
        assert 'communication_style' in frontend_dev

    def test_load_all_37_agent_personalities(self):
        """Should successfully load all 37 agent personalities"""
        router = AgentRouter()
        personality = AgentPersonality()

        all_agents = router.get_all_agents()

        for agent in all_agents:
            loaded = personality.load_agent(agent['name'])
            assert loaded is not None, f"Failed to load {agent['name']}"
            assert loaded['file_path'] == agent['file_path']

    def test_personality_file_exists_for_all_agents(self):
        """All agent .md files should exist"""
        router = AgentRouter()

        for agent in router.get_all_agents():
            assert os.path.exists(agent['file_path']), f"Missing file: {agent['file_path']}"

    def test_invalid_agent_name_returns_none(self):
        """Loading non-existent agent should return None"""
        personality = AgentPersonality()

        result = personality.load_agent('Nonexistent Agent')
        assert result is None


class TestPersonalityParsing:
    """Test parsing of agent personality fields from .md"""

    def test_parse_agent_name(self):
        """Should parse agent name from frontmatter"""
        personality = AgentPersonality()

        frontend_dev = personality.load_agent('Frontend Developer')

        assert frontend_dev['name'] == 'Frontend Developer'

    def test_parse_agent_description(self):
        """Should parse agent description from frontmatter"""
        personality = AgentPersonality()

        frontend_dev = personality.load_agent('Frontend Developer')

        assert isinstance(frontend_dev['description'], str)
        assert len(frontend_dev['description']) > 20

    def test_parse_core_mission(self):
        """Should extract core mission section"""
        personality = AgentPersonality()

        frontend_dev = personality.load_agent('Frontend Developer')

        assert 'core_mission' in frontend_dev
        assert isinstance(frontend_dev['core_mission'], list)
        assert len(frontend_dev['core_mission']) > 0

    def test_parse_communication_style(self):
        """Should extract communication style section"""
        personality = AgentPersonality()

        frontend_dev = personality.load_agent('Frontend Developer')

        assert 'communication_style' in frontend_dev
        assert isinstance(frontend_dev['communication_style'], dict)

    def test_parse_deliverables(self):
        """Should extract technical deliverables section"""
        personality = AgentPersonality()

        frontend_dev = personality.load_agent('Frontend Developer')

        assert 'deliverables' in frontend_dev
        assert isinstance(frontend_dev['deliverables'], list)

    def test_parse_workflow_process(self):
        """Should extract workflow process steps"""
        personality = AgentPersonality()

        frontend_dev = personality.load_agent('Frontend Developer')

        assert 'workflow_process' in frontend_dev
        assert isinstance(frontend_dev['workflow_process'], list)

    def test_parse_critical_rules(self):
        """Should extract critical rules section"""
        personality = AgentPersonality()

        frontend_dev = personality.load_agent('Frontend Developer')

        assert 'critical_rules' in frontend_dev
        assert 'requirements_gathering_first' in frontend_dev['critical_rules']
        assert 'test_first_development' in frontend_dev['critical_rules']


class TestCommunicationStyleExtraction:
    """Test extraction of communication style patterns"""

    def test_extract_communication_examples(self):
        """Should extract communication style examples"""
        personality = AgentPersonality()

        frontend_dev = personality.load_agent('Frontend Developer')

        examples = frontend_dev['communication_style']['examples']
        assert len(examples) > 0
        assert all(isinstance(ex, str) for ex in examples)

    def test_extract_tone_characteristics(self):
        """Should extract tone characteristics"""
        personality = AgentPersonality()

        frontend_dev = personality.load_agent('Frontend Developer')

        tone = frontend_dev['communication_style']['tone']
        assert isinstance(tone, list)
        assert len(tone) > 0

    def test_different_agents_have_different_styles(self):
        """Different agents should have distinct communication styles"""
        personality = AgentPersonality()

        frontend = personality.load_agent('Frontend Developer')
        backend = personality.load_agent('Backend Architect')
        reality = personality.load_agent('Reality Checker')

        # Should have different tone characteristics
        assert frontend['communication_style']['tone'] != reality['communication_style']['tone']


class TestDeliverableTemplates:
    """Test extraction of deliverable templates"""

    def test_extract_deliverable_templates(self):
        """Should extract deliverable templates from agent"""
        personality = AgentPersonality()

        frontend_dev = personality.load_agent('Frontend Developer')

        assert 'deliverables' in frontend_dev
        assert len(frontend_dev['deliverables']) > 0

    def test_deliverable_templates_have_structure(self):
        """Deliverable templates should have title and content"""
        personality = AgentPersonality()

        frontend_dev = personality.load_agent('Frontend Developer')

        for deliverable in frontend_dev['deliverables']:
            assert 'title' in deliverable
            assert 'content' in deliverable or 'template' in deliverable

    def test_code_examples_preserved(self):
        """Code examples in deliverables should be preserved"""
        personality = AgentPersonality()

        frontend_dev = personality.load_agent('Frontend Developer')

        # Frontend Developer should have React component examples
        has_code_example = any(
            '```' in str(deliverable.get('content', '')) or '```' in str(deliverable.get('template', ''))
            for deliverable in frontend_dev['deliverables']
        )
        assert has_code_example


class TestPersonalityApplication:
    """Test applying agent personality to responses"""

    def test_generate_response_in_agent_style(self):
        """Should generate response matching agent communication style"""
        personality = AgentPersonality()

        frontend_dev = personality.load_agent('Frontend Developer')

        # Generate response using agent style
        response = personality.generate_response(
            agent='Frontend Developer',
            context='Build a React dashboard',
            response_content='I will create a responsive dashboard'
        )

        assert '🎯 Acting as: Frontend Developer' in response
        assert 'React' in response or 'dashboard' in response

    def test_format_with_agent_header(self):
        """Response should include agent header"""
        personality = AgentPersonality()

        response = personality.format_response(
            agent_name='Frontend Developer',
            content='Building React component'
        )

        assert '🎯 Acting as: Frontend Developer' in response
        assert 'Building React component' in response

    def test_apply_communication_tone(self):
        """Should apply agent-specific communication tone"""
        personality = AgentPersonality()

        frontend = personality.load_agent('Frontend Developer')
        reality_checker = personality.load_agent('Reality Checker')

        # Frontend Developer: precise, performance-focused
        assert 'precise' in str(frontend['communication_style']['tone']).lower() or \
               'performance' in str(frontend['communication_style']['tone']).lower()

        # Reality Checker: skeptical, evidence-obsessed
        assert 'skeptical' in str(reality_checker['communication_style']['tone']).lower() or \
               'evidence' in str(reality_checker['communication_style']['tone']).lower()


class TestWorkflowProcessExtraction:
    """Test extraction of agent workflow process"""

    def test_extract_workflow_steps(self):
        """Should extract workflow steps from agent"""
        personality = AgentPersonality()

        frontend_dev = personality.load_agent('Frontend Developer')

        assert 'workflow_process' in frontend_dev
        assert len(frontend_dev['workflow_process']) >= 4  # Should have multiple steps

    def test_workflow_includes_requirements_gathering(self):
        """Workflow should include requirements gathering step"""
        personality = AgentPersonality()

        frontend_dev = personality.load_agent('Frontend Developer')

        workflow_text = ' '.join(str(step) for step in frontend_dev['workflow_process']).lower()
        assert 'requirements' in workflow_text or 'requirement' in workflow_text

    def test_workflow_includes_testing(self):
        """Workflow should include testing step"""
        personality = AgentPersonality()

        frontend_dev = personality.load_agent('Frontend Developer')

        workflow_text = ' '.join(str(step) for step in frontend_dev['workflow_process']).lower()
        assert 'test' in workflow_text

    def test_workflow_logical_order(self):
        """Workflow steps should be in logical order"""
        personality = AgentPersonality()

        frontend_dev = personality.load_agent('Frontend Developer')

        workflow_steps = frontend_dev['workflow_process']

        # First step should involve requirements/setup
        first_step = str(workflow_steps[0]).lower()
        assert any(word in first_step for word in ['requirements', 'setup', 'project', 'gather'])


class TestSuccessMetricsExtraction:
    """Test extraction of agent success metrics"""

    def test_extract_success_metrics(self):
        """Should extract success metrics from agent"""
        personality = AgentPersonality()

        frontend_dev = personality.load_agent('Frontend Developer')

        assert 'success_metrics' in frontend_dev
        assert len(frontend_dev['success_metrics']) > 0

    def test_metrics_are_measurable(self):
        """Success metrics should be measurable"""
        personality = AgentPersonality()

        frontend_dev = personality.load_agent('Frontend Developer')

        metrics = frontend_dev['success_metrics']

        # Should contain numbers or measurable criteria
        metrics_text = ' '.join(str(m) for m in metrics).lower()
        has_measurable = any(char.isdigit() for char in metrics_text) or \
                         any(word in metrics_text for word in ['%', 'percent', 'under', 'above', 'exceed'])
        assert has_measurable


class TestPersonalityCaching:
    """Test personality loading performance and caching"""

    def test_personality_cached_after_first_load(self):
        """Personality should be cached after first load"""
        personality = AgentPersonality()

        # Load once
        first = personality.load_agent('Frontend Developer')

        # Load again
        second = personality.load_agent('Frontend Developer')

        # Should return same cached object
        assert first is second

    def test_load_multiple_agents_efficiently(self):
        """Loading multiple agents should be efficient"""
        import time
        personality = AgentPersonality()

        agents_to_load = ['Frontend Developer', 'Backend Architect', 'AI Engineer', 'UI Designer']

        start = time.time()
        for agent_name in agents_to_load:
            personality.load_agent(agent_name)
        duration = time.time() - start

        # Should load 4 agents in under 2 seconds
        assert duration < 2.0

    def test_clear_cache_forces_reload(self):
        """clear_cache should force reload from file"""
        personality = AgentPersonality()

        first = personality.load_agent('Frontend Developer')
        personality.clear_cache()
        second = personality.load_agent('Frontend Developer')

        # Should be different objects after cache clear
        assert first is not second
        # But same content
        assert first['name'] == second['name']


class TestPersonalityValidation:
    """Test validation of loaded personality data"""

    def test_validate_personality_structure(self):
        """Loaded personality should have valid structure"""
        personality = AgentPersonality()

        frontend_dev = personality.load_agent('Frontend Developer')

        required_fields = [
            'name', 'description', 'core_mission', 'communication_style',
            'deliverables', 'workflow_process', 'critical_rules', 'success_metrics'
        ]

        for field in required_fields:
            assert field in frontend_dev, f"Missing required field: {field}"

    def test_all_agents_have_valid_structure(self):
        """All 37 agents should have valid personality structure"""
        router = AgentRouter()
        personality = AgentPersonality()

        required_fields = ['name', 'description', 'core_mission', 'communication_style']

        for agent in router.get_all_agents():
            loaded = personality.load_agent(agent['name'])
            for field in required_fields:
                assert field in loaded, f"{agent['name']} missing {field}"


# Pytest fixtures
@pytest.fixture
def personality():
    """Provide fresh AgentPersonality instance"""
    return AgentPersonality()


@pytest.fixture
def sample_agents():
    """Provide list of sample agent names for testing"""
    return [
        'Frontend Developer',
        'Backend Architect',
        'AI Engineer',
        'UI Designer',
        'Reality Checker'
    ]
