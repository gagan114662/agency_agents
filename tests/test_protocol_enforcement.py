"""
Test suite for Protocol Enforcement
Tests that all agents enforce the 11 mandatory workflow rules

Following Test-First Development Protocol:
- Tests import from actual modules (not yet implemented)
"""

import pytest
from agent_router.router import AgentRouter
from agent_router.protocols import ProtocolEnforcer


class TestRequirementsGatheringFirst:
    """Test Rule 1: Requirements Gathering First (MANDATORY)"""

    def test_all_agents_require_requirements_first(self):
        """All 37 agents must require requirements gathering"""
        router = AgentRouter()
        enforcer = ProtocolEnforcer()

        for agent in router.get_all_agents():
            protocols = enforcer.get_agent_protocols(agent['name'])
            assert protocols['requirements_gathering_first'] is True, \
                f"{agent['name']} does not enforce requirements gathering first"

    def test_requirements_check_before_coding(self):
        """Should check that requirements exist before allowing implementation"""
        enforcer = ProtocolEnforcer()

        # Simulate no requirements gathered
        result = enforcer.check_requirements_gathered(task_id='test-123')
        assert result['allowed'] is False
        assert 'requirements' in result['message'].lower()

    def test_requirements_approved_allows_progress(self):
        """After requirements approved, should allow progress"""
        enforcer = ProtocolEnforcer()

        # Mark requirements as gathered
        enforcer.mark_requirements_gathered(task_id='test-123')

        result = enforcer.check_requirements_gathered(task_id='test-123')
        assert result['allowed'] is True


class TestTestFirstDevelopment:
    """Test Rule 2: Test-First Development (MANDATORY)"""

    def test_all_agents_require_test_first(self):
        """All 37 agents must require test-first development"""
        router = AgentRouter()
        enforcer = ProtocolEnforcer()

        for agent in router.get_all_agents():
            protocols = enforcer.get_agent_protocols(agent['name'])
            assert protocols['test_first_development'] is True, \
                f"{agent['name']} does not enforce test-first development"

    def test_tests_required_before_implementation(self):
        """Should require tests written before implementation"""
        enforcer = ProtocolEnforcer()

        # Try to implement without tests
        result = enforcer.check_tests_written(task_id='test-123')
        assert result['allowed'] is False
        assert 'tests' in result['message'].lower()

    def test_tests_approved_allows_implementation(self):
        """After tests written, reflected, and approved, allow implementation"""
        enforcer = ProtocolEnforcer()

        # Mark tests as written, reflection complete, and approved
        enforcer.mark_tests_written(task_id='test-123')
        enforcer.mark_reflection_complete(task_id='test-123')
        enforcer.mark_tests_approved(task_id='test-123')

        result = enforcer.check_can_implement(task_id='test-123')
        assert result['allowed'] is True


class TestSelfReflectionAfterTests:
    """Test Self-Reflection Cue After Test Writing (MANDATORY)"""

    def test_reflection_required_after_tests_written(self):
        """Should require self-reflection after tests are written"""
        enforcer = ProtocolEnforcer()

        # Mark tests as written
        enforcer.mark_tests_written(task_id='test-reflection-1')

        # Check if reflection is required
        result = enforcer.check_reflection_required(task_id='test-reflection-1')
        assert result['required'] is True
        assert 'reflect' in result['message'].lower()

    def test_reflection_cue_provides_prompts(self):
        """Should provide reflection prompts after tests written"""
        enforcer = ProtocolEnforcer()

        enforcer.mark_tests_written(task_id='test-reflection-2')

        reflection_cue = enforcer.generate_reflection_cue(task_id='test-reflection-2')

        assert isinstance(reflection_cue, dict)
        assert 'prompts' in reflection_cue
        assert len(reflection_cue['prompts']) >= 3
        assert 'test_coverage' in str(reflection_cue).lower()

    def test_reflection_marks_task_as_reflected(self):
        """Should mark task as reflected after reflection"""
        enforcer = ProtocolEnforcer()

        enforcer.mark_tests_written(task_id='test-reflection-3')
        enforcer.mark_reflection_complete(task_id='test-reflection-3')

        result = enforcer.check_reflection_required(task_id='test-reflection-3')
        assert result['required'] is False

    def test_implementation_blocked_without_reflection(self):
        """Implementation should be blocked if reflection not complete"""
        enforcer = ProtocolEnforcer()

        # Tests written but no reflection
        enforcer.mark_tests_written(task_id='test-reflection-4')
        enforcer.mark_tests_approved(task_id='test-reflection-4')

        result = enforcer.check_can_implement(task_id='test-reflection-4')
        assert result['allowed'] is False
        assert 'reflection' in result['message'].lower()

    def test_implementation_allowed_after_reflection(self):
        """Implementation allowed after reflection complete"""
        enforcer = ProtocolEnforcer()

        # Complete workflow with reflection
        enforcer.mark_tests_written(task_id='test-reflection-5')
        enforcer.mark_reflection_complete(task_id='test-reflection-5')
        enforcer.mark_tests_approved(task_id='test-reflection-5')

        result = enforcer.check_can_implement(task_id='test-reflection-5')
        assert result['allowed'] is True

    def test_reflection_prompts_include_key_questions(self):
        """Reflection prompts should include key self-assessment questions"""
        enforcer = ProtocolEnforcer()

        enforcer.mark_tests_written(task_id='test-reflection-6')
        reflection = enforcer.generate_reflection_cue(task_id='test-reflection-6')

        prompts = reflection['prompts']
        prompt_text = ' '.join([p['question'] for p in prompts])

        # Check for key reflection topics
        assert any(word in prompt_text.lower() for word in ['coverage', 'test', 'edge'])
        assert any(word in prompt_text.lower() for word in ['scenario', 'case'])
        assert any(word in prompt_text.lower() for word in ['quality', 'comprehensive'])


class TestGitCommitCheckpoint:
    """Test Rule 2 (from protocol): Git Commit Checkpoint (MANDATORY)"""

    def test_all_agents_require_git_workflow(self):
        """All agents must follow git workflow protocol"""
        router = AgentRouter()
        enforcer = ProtocolEnforcer()

        for agent in router.get_all_agents():
            protocols = enforcer.get_agent_protocols(agent['name'])
            assert protocols['git_commit_checkpoint'] is True

    def test_git_checks_required_before_commit(self):
        """Should require 4 git checks before commit"""
        enforcer = ProtocolEnforcer()

        result = enforcer.check_git_workflow_complete(task_id='test-123')

        assert 'checks' in result
        assert len(result['checks']) == 4
        assert 'clean_unnecessary_files' in [c['name'] for c in result['checks']]
        assert 'verify_requirements_file' in [c['name'] for c in result['checks']]
        assert 'validate_auth_necessity' in [c['name'] for c in result['checks']]
        assert 'verify_remote_push' in [c['name'] for c in result['checks']]


class TestLoggingStandards:
    """Test Rule 3: Logging Standards (MANDATORY)"""

    def test_all_agents_enforce_logging_standards(self):
        """All agents must enforce logging standards"""
        router = AgentRouter()
        enforcer = ProtocolEnforcer()

        for agent in router.get_all_agents():
            protocols = enforcer.get_agent_protocols(agent['name'])
            assert protocols['logging_standards'] is True

    def test_no_debug_logs_in_production(self):
        """Should check for debug logs in production code"""
        enforcer = ProtocolEnforcer()

        code = """
        import logging
        logger = logging.getLogger(__name__)
        logger.debug("This should not be here")
        """

        result = enforcer.validate_logging(code)
        assert result['has_debug_logs'] is True
        assert result['passed'] is False

    def test_no_print_statements(self):
        """Should check for print statements"""
        enforcer = ProtocolEnforcer()

        code = """
        print("This should not be here")
        """

        result = enforcer.validate_logging(code)
        assert result['has_print_statements'] is True
        assert result['passed'] is False


class TestBashValidation:
    """Test Rule 4: Bash Test Validation (MANDATORY)"""

    def test_all_agents_require_bash_validation(self):
        """All agents must require bash validation for logic"""
        router = AgentRouter()
        enforcer = ProtocolEnforcer()

        for agent in router.get_all_agents():
            protocols = enforcer.get_agent_protocols(agent['name'])
            assert protocols['bash_validation'] is True

    def test_math_logic_requires_bash_test(self):
        """Math/logic should require bash validation script"""
        enforcer = ProtocolEnforcer()

        task = "Implement percentage calculation"
        result = enforcer.requires_bash_validation(task)

        assert result['required'] is True
        assert 'math' in result['reason'].lower() or 'calculation' in result['reason'].lower()


class TestCodeOrganization:
    """Test Rule 5: Code Organization (MANDATORY)"""

    def test_all_agents_enforce_organization(self):
        """All agents must enforce code organization"""
        router = AgentRouter()
        enforcer = ProtocolEnforcer()

        for agent in router.get_all_agents():
            protocols = enforcer.get_agent_protocols(agent['name'])
            assert protocols['code_organization'] is True

    def test_detect_duplicate_functions(self):
        """Should detect duplicate function definitions"""
        enforcer = ProtocolEnforcer()

        code_files = {
            'file1.py': 'def calculate(): pass',
            'file2.py': 'def calculate(): pass'
        }

        result = enforcer.check_code_organization(code_files)
        assert result['has_duplicates'] is True
        assert len(result['duplicates']) > 0


class TestLocalTesting:
    """Test Rule 6: Local Testing (MANDATORY)"""

    def test_all_agents_require_local_testing(self):
        """All agents must require local testing"""
        router = AgentRouter()
        enforcer = ProtocolEnforcer()

        for agent in router.get_all_agents():
            protocols = enforcer.get_agent_protocols(agent['name'])
            assert protocols['local_testing'] is True

    def test_all_tests_must_pass(self):
        """Should require 100% test pass rate"""
        enforcer = ProtocolEnforcer()

        test_results = {'total': 10, 'passed': 9, 'failed': 1}

        result = enforcer.validate_test_results(test_results)
        assert result['allowed'] is False
        assert 'pass rate' in result['message'].lower()


class TestProductionReadyCode:
    """Test Rule 7: Production-Ready Code (MANDATORY)"""

    def test_all_agents_enforce_production_standards(self):
        """All agents must enforce production standards"""
        router = AgentRouter()
        enforcer = ProtocolEnforcer()

        for agent in router.get_all_agents():
            protocols = enforcer.get_agent_protocols(agent['name'])
            assert protocols['production_ready_code'] is True

    def test_no_commented_out_code(self):
        """Should detect commented-out code"""
        enforcer = ProtocolEnforcer()

        code = """
        def active_function():
            pass

        # def old_function():
        #     return 42
        """

        result = enforcer.validate_production_code(code)
        assert result['has_commented_code'] is True
        assert result['passed'] is False

    def test_no_todo_comments(self):
        """Should detect TODO/FIXME comments"""
        enforcer = ProtocolEnforcer()

        code = """
        def function():
            # TODO: Fix this later
            pass
        """

        result = enforcer.validate_production_code(code)
        assert result['has_todo_comments'] is True
        assert result['passed'] is False


class TestUserDecisionPoints:
    """Test Rule 8: User Decision Points (MANDATORY)"""

    def test_all_agents_require_user_decisions(self):
        """All agents must present options for key decisions"""
        router = AgentRouter()
        enforcer = ProtocolEnforcer()

        for agent in router.get_all_agents():
            protocols = enforcer.get_agent_protocols(agent['name'])
            assert protocols['user_decision_points'] is True

    def test_detect_decision_points(self):
        """Should detect when decision point is needed"""
        enforcer = ProtocolEnforcer()

        tasks = [
            "Choose database (PostgreSQL vs MongoDB)",
            "Select framework (React vs Vue)",
            "Decide architecture (monolith vs microservices)"
        ]

        for task in tasks:
            result = enforcer.is_decision_point(task)
            assert result['is_decision'] is True


class TestCopyPasteReadyCommands:
    """Test Rule 9: Copy-Paste Ready Commands (MANDATORY)"""

    def test_all_agents_provide_copy_paste_commands(self):
        """All agents must provide copy-paste ready commands"""
        router = AgentRouter()
        enforcer = ProtocolEnforcer()

        for agent in router.get_all_agents():
            protocols = enforcer.get_agent_protocols(agent['name'])
            assert protocols['copy_paste_ready_commands'] is True

    def test_detect_placeholders_in_commands(self):
        """Should detect placeholder patterns"""
        enforcer = ProtocolEnforcer()

        commands = [
            "cd <your-project-path>",
            "export API_KEY=<your-api-key>",
            "docker run -v <path>:/config app"
        ]

        for command in commands:
            result = enforcer.validate_command(command)
            assert result['has_placeholders'] is True
            assert result['passed'] is False

    def test_valid_commands_pass(self):
        """Valid copy-paste ready commands should pass"""
        enforcer = ProtocolEnforcer()

        command = "cd /Users/gaganarora/Desktop/gagan_projects/agency_agents"

        result = enforcer.validate_command(command)
        assert result['has_placeholders'] is False
        assert result['passed'] is True


class TestVirtualEnvironmentManagement:
    """Test Rule 10: Virtual Environment Management (MANDATORY)"""

    def test_all_agents_use_venv(self):
        """All agents must use shared venv"""
        router = AgentRouter()
        enforcer = ProtocolEnforcer()

        for agent in router.get_all_agents():
            protocols = enforcer.get_agent_protocols(agent['name'])
            assert protocols['virtual_environment'] is True
            assert protocols['venv_path'] == '/Users/gaganarora/Desktop/gagan_projects/venv'

    def test_venv_exists(self):
        """Should verify venv exists"""
        enforcer = ProtocolEnforcer()

        result = enforcer.check_venv_setup()
        assert 'venv_exists' in result
        assert 'venv_path' in result

    def test_venv_has_python(self):
        """Should verify venv has Python interpreter"""
        enforcer = ProtocolEnforcer()

        result = enforcer.check_venv_setup()
        assert 'python_exists' in result


class TestTODOTracking:
    """Test Rule 11: TODO.md Tracking (MANDATORY)"""

    def test_all_agents_maintain_todo(self):
        """All agents must maintain TODO.md"""
        router = AgentRouter()
        enforcer = ProtocolEnforcer()

        for agent in router.get_all_agents():
            protocols = enforcer.get_agent_protocols(agent['name'])
            assert protocols['todo_tracking'] is True

    def test_todo_file_exists(self):
        """Should verify TODO.md exists"""
        enforcer = ProtocolEnforcer()

        result = enforcer.check_todo_file()
        assert 'file_exists' in result

    def test_todo_has_required_sections(self):
        """Should verify TODO.md has required sections"""
        enforcer = ProtocolEnforcer()

        result = enforcer.validate_todo_structure()

        required_sections = ['In Progress', 'Pending', 'Completed']
        for section in required_sections:
            assert section in result['sections_found']

    def test_todo_updated_recently(self):
        """Should verify TODO.md updated recently"""
        enforcer = ProtocolEnforcer()

        result = enforcer.check_todo_freshness()
        assert 'days_since_update' in result


class TestProtocolCompliance:
    """Test overall protocol compliance"""

    def test_all_11_rules_enforced(self):
        """Should enforce all 11 mandatory rules"""
        enforcer = ProtocolEnforcer()

        protocols = enforcer.get_all_protocol_rules()

        assert len(protocols) == 11
        rule_names = [rule['name'] for rule in protocols]

        expected_rules = [
            'Requirements Gathering First',
            'Git Commit Checkpoint',
            'Logging Standards',
            'Bash Validation',
            'Code Organization',
            'Local Testing',
            'Production-Ready Code',
            'User Decision Points',
            'Copy-Paste Ready Commands',
            'Virtual Environment',
            'TODO Tracking'
        ]

        for rule in expected_rules:
            assert any(rule.lower() in name.lower() for name in rule_names)

    def test_check_compliance_for_task(self):
        """Should check compliance for a given task"""
        enforcer = ProtocolEnforcer()

        result = enforcer.check_compliance(task_id='test-123')

        assert 'rules_checked' in result
        assert 'rules_passed' in result
        assert 'rules_failed' in result
        assert 'compliance_percentage' in result

    def test_generate_compliance_report(self):
        """Should generate compliance report"""
        enforcer = ProtocolEnforcer()

        report = enforcer.generate_compliance_report(task_id='test-123')

        assert isinstance(report, str)
        assert 'compliance' in report.lower()
        assert '11' in report  # Should mention 11 rules


class TestProtocolByAgentCategory:
    """Test protocol requirements by agent category"""

    def test_engineering_agents_follow_all_protocols(self):
        """Engineering agents should follow all 11 protocols"""
        router = AgentRouter()
        enforcer = ProtocolEnforcer()

        engineering_agents = router.get_agents_by_category('engineering')

        for agent in engineering_agents:
            protocols = enforcer.get_agent_protocols(agent['name'])
            assert len(protocols) >= 11

    def test_design_agents_follow_all_protocols(self):
        """Design agents should follow all 11 protocols"""
        router = AgentRouter()
        enforcer = ProtocolEnforcer()

        design_agents = router.get_agents_by_category('design')

        for agent in design_agents:
            protocols = enforcer.get_agent_protocols(agent['name'])
            assert len(protocols) >= 11


# Pytest fixtures
@pytest.fixture
def enforcer():
    """Provide fresh ProtocolEnforcer instance"""
    return ProtocolEnforcer()


@pytest.fixture
def sample_task():
    """Provide sample task for testing"""
    return {
        'id': 'test-123',
        'description': 'Build React dashboard',
        'agent': 'Frontend Developer'
    }
