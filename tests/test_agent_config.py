"""
Test suite for Agent Configuration system
Tests YAML config loading, validation, and agent metadata

Following Test-First Development Protocol:
- These tests are written BEFORE implementation
- Tests import from actual modules (not yet implemented)
"""

import pytest
import os
from agent_router.config import AgentConfig, AgentConfigError


class TestConfigLoading:
    """Test YAML configuration file loading"""

    def test_config_loads_from_yaml_file(self):
        """Should load agent configuration from YAML file"""
        config = AgentConfig()
        assert config.agents is not None
        assert isinstance(config.agents, dict)

    def test_config_file_exists_at_expected_path(self):
        """Config file should exist at agent_router/agents.yaml"""
        expected_path = '/Users/gaganarora/Desktop/gagan_projects/Agency/agency_agents/agent_router/agents.yaml'
        config = AgentConfig()

        assert os.path.exists(expected_path)
        assert config.config_path == expected_path

    def test_config_has_all_categories(self):
        """Config should have all agent categories"""
        config = AgentConfig()

        required_categories = [
            'engineering',
            'design',
            'testing',
            'marketing',
            'product',
            'support'
        ]

        for category in required_categories:
            assert category in config.agents, f"Missing category: {category}"

    def test_invalid_yaml_raises_error(self):
        """Invalid YAML should raise AgentConfigError"""
        with pytest.raises(AgentConfigError):
            config = AgentConfig(config_path='/invalid/path/agents.yaml')


class TestAgentDefinitionValidation:
    """Test individual agent definition validation"""

    def test_all_agents_have_required_fields(self):
        """Every agent must have name, description, keywords, file_path"""
        config = AgentConfig()

        required_fields = ['name', 'description', 'keywords', 'file_path']

        for category, agents in config.agents.items():
            for agent in agents:
                for field in required_fields:
                    assert field in agent, f"Agent in {category} missing {field}"

    def test_agent_keywords_are_lists(self):
        """Agent keywords should be lists of strings"""
        config = AgentConfig()

        for category, agents in config.agents.items():
            for agent in agents:
                assert isinstance(agent['keywords'], list)
                assert all(isinstance(kw, str) for kw in agent['keywords'])
                assert len(agent['keywords']) > 0

    def test_agent_file_paths_are_valid(self):
        """Agent file paths should point to existing .md files"""
        config = AgentConfig()

        for category, agents in config.agents.items():
            for agent in agents:
                file_path = agent['file_path']
                assert file_path.endswith('.md')
                assert os.path.exists(file_path), f"Agent file not found: {file_path}"

    def test_agent_names_are_unique(self):
        """Agent names should be unique across all categories"""
        config = AgentConfig()

        all_names = []
        for category, agents in config.agents.items():
            for agent in agents:
                all_names.append(agent['name'])

        assert len(all_names) == len(set(all_names)), "Duplicate agent names found"

    def test_agent_descriptions_are_non_empty(self):
        """Agent descriptions should be non-empty strings"""
        config = AgentConfig()

        for category, agents in config.agents.items():
            for agent in agents:
                assert isinstance(agent['description'], str)
                assert len(agent['description']) > 10


class TestEngineeringAgents:
    """Test engineering category agent definitions"""

    def test_frontend_developer_defined(self):
        """Frontend Developer agent should be properly defined"""
        config = AgentConfig()

        frontend_dev = config.get_agent_by_name('Frontend Developer')
        assert frontend_dev is not None
        assert frontend_dev['category'] == 'engineering'
        assert 'react' in [kw.lower() for kw in frontend_dev['keywords']]
        assert 'frontend' in [kw.lower() for kw in frontend_dev['keywords']]

    def test_backend_architect_defined(self):
        """Backend Architect agent should be properly defined"""
        config = AgentConfig()

        backend_arch = config.get_agent_by_name('Backend Architect')
        assert backend_arch is not None
        assert backend_arch['category'] == 'engineering'
        assert 'api' in [kw.lower() for kw in backend_arch['keywords']]
        assert 'backend' in [kw.lower() for kw in backend_arch['keywords']]

    def test_ai_engineer_defined(self):
        """AI Engineer agent should be properly defined"""
        config = AgentConfig()

        ai_engineer = config.get_agent_by_name('AI Engineer')
        assert ai_engineer is not None
        assert ai_engineer['category'] == 'engineering'
        assert any('ml' in kw.lower() or 'ai' in kw.lower() for kw in ai_engineer['keywords'])

    def test_senior_developer_defined(self):
        """Senior Developer agent should be properly defined"""
        config = AgentConfig()

        senior_dev = config.get_agent_by_name('Senior Developer')
        assert senior_dev is not None
        assert senior_dev['category'] == 'engineering'
        assert senior_dev['is_default'] is True  # Should be marked as default


class TestDesignAgents:
    """Test design category agent definitions"""

    def test_ui_designer_defined(self):
        """UI Designer agent should be properly defined"""
        config = AgentConfig()

        ui_designer = config.get_agent_by_name('UI Designer')
        assert ui_designer is not None
        assert ui_designer['category'] == 'design'
        assert 'ui' in [kw.lower() for kw in ui_designer['keywords']]

    def test_ux_architect_defined(self):
        """UX Architect agent should be properly defined"""
        config = AgentConfig()

        ux_architect = config.get_agent_by_name('UX Architect')
        assert ux_architect is not None
        assert ux_architect['category'] == 'design'


class TestTestingAgents:
    """Test testing category agent definitions"""

    def test_reality_checker_defined(self):
        """Reality Checker agent should be properly defined"""
        config = AgentConfig()

        reality_checker = config.get_agent_by_name('Reality Checker')
        assert reality_checker is not None
        assert reality_checker['category'] == 'testing'
        assert 'qa' in [kw.lower() for kw in reality_checker['keywords']]


class TestConfigHelperMethods:
    """Test helper methods on AgentConfig"""

    def test_get_agent_by_name_returns_correct_agent(self):
        """get_agent_by_name should return correct agent details"""
        config = AgentConfig()

        agent = config.get_agent_by_name('Frontend Developer')
        assert agent['name'] == 'Frontend Developer'
        assert 'keywords' in agent
        assert 'file_path' in agent

    def test_get_agent_by_name_returns_none_for_invalid_name(self):
        """get_agent_by_name should return None for non-existent agent"""
        config = AgentConfig()

        agent = config.get_agent_by_name('Nonexistent Agent')
        assert agent is None

    def test_get_agents_by_category_returns_list(self):
        """get_agents_by_category should return list of agents"""
        config = AgentConfig()

        agents = config.get_agents_by_category('engineering')
        assert isinstance(agents, list)
        assert len(agents) >= 7

    def test_get_all_agents_returns_flat_list(self):
        """get_all_agents should return flat list of all agents"""
        config = AgentConfig()

        all_agents = config.get_all_agents()
        assert isinstance(all_agents, list)
        assert len(all_agents) >= 37

    def test_get_default_agent_returns_senior_developer(self):
        """get_default_agent should return Senior Developer"""
        config = AgentConfig()

        default_agent = config.get_default_agent()
        assert default_agent['name'] == 'Senior Developer'
        assert default_agent['is_default'] is True

    def test_search_agents_by_keyword(self):
        """search_agents should find agents matching keyword"""
        config = AgentConfig()

        results = config.search_agents('react')
        assert len(results) > 0
        assert any(agent['name'] == 'Frontend Developer' for agent in results)

    def test_search_agents_case_insensitive(self):
        """search_agents should be case-insensitive"""
        config = AgentConfig()

        results_lower = config.search_agents('react')
        results_upper = config.search_agents('REACT')
        results_mixed = config.search_agents('React')

        assert len(results_lower) == len(results_upper) == len(results_mixed)


class TestConfigValidationRules:
    """Test configuration validation rules"""

    def test_validates_minimum_keywords_per_agent(self):
        """Each agent should have at least 3 keywords"""
        config = AgentConfig()

        for agent in config.get_all_agents():
            assert len(agent['keywords']) >= 3, f"{agent['name']} has too few keywords"

    def test_validates_file_path_format(self):
        """File paths should follow expected format"""
        config = AgentConfig()

        for agent in config.get_all_agents():
            file_path = agent['file_path']
            # Should be absolute path
            assert file_path.startswith('/')
            # Should contain agency_agents directory
            assert 'agency_agents' in file_path
            # Should end with .md
            assert file_path.endswith('.md')

    def test_validates_description_length(self):
        """Descriptions should be between 10 and 500 characters"""
        config = AgentConfig()

        for agent in config.get_all_agents():
            desc_len = len(agent['description'])
            assert 10 <= desc_len <= 500, f"{agent['name']} description length: {desc_len}"


class TestConfigCaching:
    """Test configuration caching and performance"""

    def test_config_loads_once_and_caches(self):
        """Config should load once and cache results"""
        config1 = AgentConfig()
        config2 = AgentConfig()

        # Both should reference same cached config
        assert config1.agents is config2.agents

    def test_reload_config_refreshes_data(self):
        """reload() should refresh configuration data"""
        config = AgentConfig()
        original_agents = config.agents

        config.reload()
        reloaded_agents = config.agents

        # Should be new object but same content
        assert original_agents == reloaded_agents


class TestProtocolDefinitions:
    """Test protocol definitions in agent config"""

    def test_all_agents_have_protocol_definitions(self):
        """All agents should have protocol requirements defined"""
        config = AgentConfig()

        for agent in config.get_all_agents():
            assert 'protocols' in agent
            assert isinstance(agent['protocols'], dict)

    def test_protocol_includes_11_rules(self):
        """Protocol should reference all 11 workflow rules"""
        config = AgentConfig()

        for agent in config.get_all_agents():
            protocols = agent['protocols']
            assert 'workflow_rules' in protocols
            assert protocols['workflow_rules']['total'] == 11
            assert protocols['workflow_rules']['mandatory'] is True


# Pytest fixtures
@pytest.fixture
def config():
    """Provide fresh AgentConfig instance"""
    return AgentConfig()


@pytest.fixture
def sample_agent():
    """Provide sample agent definition for testing"""
    return {
        'name': 'Test Agent',
        'description': 'Test agent for unit testing',
        'keywords': ['test', 'sample', 'example'],
        'file_path': '/path/to/test-agent.md',
        'category': 'testing',
        'protocols': {
            'requirements_gathering_first': True,
            'test_first_development': True,
            'workflow_rules': {'total': 11, 'mandatory': True}
        }
    }
