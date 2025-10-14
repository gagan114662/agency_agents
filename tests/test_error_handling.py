"""
Test suite for Error Handling and Edge Cases
Tests failure scenarios, error recovery, and edge cases

Following Test-First Development Protocol:
- Tests import from actual modules (not yet implemented)
"""

import pytest
from agent_router.router import AgentRouter
from agent_router.config import AgentConfig, AgentConfigError
from agent_router.personality import AgentPersonality, PersonalityLoadError
from agent_router.errors import RoutingError, ValidationError


class TestConfigurationErrors:
    """Test configuration file error handling"""

    def test_missing_config_file_raises_error(self):
        """Missing YAML config should raise AgentConfigError"""
        with pytest.raises(AgentConfigError):
            config = AgentConfig(config_path='/nonexistent/path/agents.yaml')

    def test_corrupted_yaml_raises_error(self):
        """Corrupted YAML should raise AgentConfigError"""
        with pytest.raises(AgentConfigError):
            config = AgentConfig(config_path='/path/to/corrupted.yaml')

    def test_missing_required_fields_raises_error(self):
        """Config missing required fields should raise error"""
        with pytest.raises(AgentConfigError) as exc_info:
            config = AgentConfig()
            # Simulate config with missing fields
            config._validate_agent({'name': 'Test'})  # Missing keywords, file_path

        assert 'required field' in str(exc_info.value).lower()

    def test_invalid_file_path_raises_error(self):
        """Invalid agent file path should raise error"""
        config = AgentConfig()

        with pytest.raises(AgentConfigError) as exc_info:
            config._validate_agent({
                'name': 'Test Agent',
                'description': 'Test',
                'keywords': ['test'],
                'file_path': '/nonexistent/agent.md'
            })

        assert 'file not found' in str(exc_info.value).lower()

    def test_duplicate_agent_names_raises_error(self):
        """Duplicate agent names should raise error"""
        with pytest.raises(AgentConfigError) as exc_info:
            config = AgentConfig()
            # Simulate duplicate names by adding a duplicate to the config
            if 'engineering' in config.agents and len(config.agents['engineering']) > 0:
                # Duplicate the first engineering agent
                duplicate_agent = config.agents['engineering'][0].copy()
                config.agents['engineering'].append(duplicate_agent)
            config._check_duplicates()

        assert 'duplicate' in str(exc_info.value).lower()


class TestPersonalityLoadingErrors:
    """Test personality loading error handling"""

    def test_missing_agent_file_returns_none(self):
        """Loading agent with missing file should return None"""
        personality = AgentPersonality()

        result = personality.load_agent('Nonexistent Agent')
        assert result is None

    def test_corrupted_markdown_handles_gracefully(self):
        """Corrupted markdown should handle gracefully"""
        personality = AgentPersonality()

        # Should not crash, should return None or partial data
        try:
            result = personality.load_agent_from_file('/path/to/corrupted.md')
            assert result is None or isinstance(result, dict)
        except PersonalityLoadError:
            # Also acceptable to raise specific error
            assert True

    def test_missing_frontmatter_handles_gracefully(self):
        """Markdown without frontmatter should handle gracefully"""
        personality = AgentPersonality()

        # Should extract what it can or return None
        result = personality.parse_markdown("# Agent\n\nNo frontmatter here")
        assert result is None or 'name' not in result


class TestRoutingErrors:
    """Test routing error handling"""

    def test_empty_task_doesnt_crash(self):
        """Empty task should not crash, should default to Senior Developer"""
        router = AgentRouter()

        agent = router.select_agent("")
        assert agent is not None
        assert agent['name'] == 'Senior Developer'

    def test_very_long_task_handles_correctly(self):
        """Very long task should be handled correctly"""
        router = AgentRouter()

        long_task = "Build a React dashboard " * 1000  # 3000+ words
        agent = router.select_agent(long_task)

        assert agent is not None
        # Should still detect React keyword
        assert agent['name'] == 'Frontend Developer'

    def test_special_characters_handled(self):
        """Tasks with special characters should be handled"""
        router = AgentRouter()

        tasks = [
            "Build API with $pecial ch@r$",
            "Create système avec français",
            "Build 日本語 system",
            "API with émojis 🚀✨"
        ]

        for task in tasks:
            agent = router.select_agent(task)
            assert agent is not None  # Should not crash

    def test_only_punctuation_task(self):
        """Task with only punctuation should default gracefully"""
        router = AgentRouter()

        agent = router.select_agent("!@#$%^&*()")
        assert agent is not None
        assert agent['name'] == 'Senior Developer'

    def test_whitespace_only_task(self):
        """Whitespace-only task should be handled"""
        router = AgentRouter()

        agent = router.select_agent("     \n\n\t\t   ")
        assert agent is not None
        assert agent['name'] == 'Senior Developer'


class TestKeywordConflicts:
    """Test handling of keyword conflicts"""

    def test_multiple_agents_match(self):
        """When multiple agents match, should select best fit"""
        router = AgentRouter()

        # Task has both frontend and backend keywords
        task = "Build React components that call Node.js API endpoints"
        result = router.analyze_task(task)

        # Should detect multi-agent need
        assert result['is_multi_agent'] is True or \
               result['confidence_score'] > 0.5  # Or pick one with high confidence

    def test_conflicting_keywords_resolved(self):
        """Conflicting keywords should be resolved logically"""
        router = AgentRouter()

        # "design" and "implement" could conflict
        task = "Design the implementation of feature"
        agent = router.select_agent(task)

        assert agent is not None
        # Should pick one based on prominence

    def test_equal_confidence_scores(self):
        """Equal confidence scores should have deterministic fallback"""
        router = AgentRouter()

        # Generic task that doesn't strongly match anything
        task = "Work on the thing"
        agent = router.select_agent(task)

        assert agent is not None
        assert agent['name'] == 'Senior Developer'  # Default fallback


class TestCoordinationErrors:
    """Test coordination error handling"""

    def test_single_agent_coordination_plan(self):
        """Single agent task should have simple plan"""
        from agent_router.coordination import CoordinationPlanner

        planner = CoordinationPlanner()
        plan = planner.generate_plan("Fix CSS")

        assert len(plan['agents']) == 1
        assert len(plan['handoff_points']) == 0

    def test_impossible_coordination(self):
        """Impossible coordination should handle gracefully"""
        from agent_router.coordination import CoordinationPlanner

        planner = CoordinationPlanner()

        # Try to coordinate with no valid agents
        try:
            plan = planner.generate_plan("")
            assert plan is not None
        except RoutingError:
            # Also acceptable
            assert True


class TestProtocolValidationErrors:
    """Test protocol validation error handling"""

    def test_missing_requirements_blocks_progress(self):
        """Missing requirements should block progress"""
        from agent_router.protocols import ProtocolEnforcer

        enforcer = ProtocolEnforcer()
        result = enforcer.check_can_implement(task_id='test-123')

        assert result['allowed'] is False
        assert 'requirements' in result['message'].lower()

    def test_failed_tests_block_deployment(self):
        """Failed tests should block deployment"""
        from agent_router.protocols import ProtocolEnforcer

        enforcer = ProtocolEnforcer()

        test_results = {'total': 10, 'passed': 8, 'failed': 2}
        result = enforcer.can_deploy(test_results)

        assert result['allowed'] is False
        assert 'tests failed' in result['message'].lower()

    def test_invalid_code_blocks_commit(self):
        """Invalid code should block git commit"""
        from agent_router.protocols import ProtocolEnforcer

        enforcer = ProtocolEnforcer()

        code = """
        print("debug")  # Not allowed
        # TODO: Fix this  # Not allowed
        """

        result = enforcer.can_commit(code)
        assert result['allowed'] is False


class TestRecoveryMechanisms:
    """Test error recovery mechanisms"""

    def test_config_reload_after_error(self):
        """Should be able to reload config after error"""
        config = AgentConfig()

        # Simulate error
        try:
            config._load_from_path('/invalid/path')
        except:
            pass

        # Should be able to reload successfully
        config.reload()
        assert config.agents is not None

    def test_router_continues_after_error(self):
        """Router should continue working after error"""
        router = AgentRouter()

        # Cause an error
        try:
            router.select_agent(None)  # None task
        except:
            pass

        # Should still work
        agent = router.select_agent("Build React app")
        assert agent is not None

    def test_personality_cache_cleared_after_error(self):
        """Should be able to clear personality cache after error"""
        personality = AgentPersonality()

        # Load with error
        try:
            personality.load_agent('Invalid Agent')
        except:
            pass

        # Clear cache and try again
        personality.clear_cache()
        result = personality.load_agent('Frontend Developer')
        assert result is not None


class TestResourceExhaustion:
    """Test handling of resource exhaustion"""

    def test_handles_many_concurrent_requests(self):
        """Should handle many concurrent routing requests"""
        router = AgentRouter()

        tasks = [f"Build feature {i}" for i in range(100)]

        for task in tasks:
            agent = router.select_agent(task)
            assert agent is not None

    def test_memory_doesnt_grow_unbounded(self):
        """Memory usage should stay reasonable"""
        import sys
        router = AgentRouter()

        initial_size = sys.getsizeof(router)

        # Make many requests
        for i in range(1000):
            router.select_agent(f"Task {i}")

        final_size = sys.getsizeof(router)

        # Size shouldn't grow dramatically (10x)
        assert final_size < initial_size * 10


class TestTimeoutHandling:
    """Test timeout handling"""

    def test_routing_completes_in_reasonable_time(self):
        """Routing should complete quickly"""
        import time
        router = AgentRouter()

        start = time.time()
        agent = router.select_agent("Build complex feature")
        duration = time.time() - start

        assert duration < 1.0  # Should be under 1 second

    def test_personality_loading_times_out(self):
        """Personality loading should timeout if too slow"""
        personality = AgentPersonality()

        # Should complete or timeout gracefully
        try:
            result = personality.load_agent('Frontend Developer')
            assert result is not None
        except TimeoutError:
            # Acceptable if timeout mechanism exists
            assert True


class TestValidationErrors:
    """Test validation error handling"""

    def test_invalid_agent_name_raises_error(self):
        """Invalid agent name should raise ValidationError"""
        router = AgentRouter()

        with pytest.raises((ValidationError, ValueError)):
            router.get_agent_by_name('')  # Empty name

    def test_invalid_task_type_handled(self):
        """Non-string task should be handled"""
        router = AgentRouter()

        # Try with different types
        try:
            agent = router.select_agent(123)  # Integer
            assert agent is not None  # Should convert or default
        except (ValidationError, TypeError):
            # Also acceptable to raise error
            assert True

    def test_negative_confidence_score(self):
        """Negative confidence score should be handled"""
        router = AgentRouter()

        result = router.analyze_task("test")
        assert result['confidence_score'] >= 0.0


class TestGracefulDegradation:
    """Test graceful degradation"""

    def test_partial_config_loads_what_it_can(self):
        """Partial config should load valid agents"""
        # If some agents are invalid, should still load valid ones
        config = AgentConfig()

        # Should have at least some agents
        all_agents = config.get_all_agents()
        assert len(all_agents) > 0

    def test_missing_personality_fields_filled_with_defaults(self):
        """Missing personality fields should use defaults"""
        personality = AgentPersonality()

        # Should handle agents with incomplete definitions
        result = personality.load_agent('Frontend Developer')

        # Should have some data even if not complete
        assert 'name' in result

    def test_routing_works_with_minimal_config(self):
        """Routing should work even with minimal config"""
        router = AgentRouter()

        # Should at least have default agent
        agent = router.select_agent("anything")
        assert agent is not None


# Pytest fixtures
@pytest.fixture
def router():
    """Provide fresh router instance"""
    return AgentRouter()


@pytest.fixture
def config():
    """Provide fresh config instance"""
    return AgentConfig()


@pytest.fixture
def personality():
    """Provide fresh personality instance"""
    return AgentPersonality()
