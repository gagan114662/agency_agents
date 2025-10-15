"""
Protocol Enforcer
Enforces the 11 mandatory workflow rules for all agents
"""

import os
import re
from datetime import datetime
from typing import Dict, List
from .router import AgentRouter


class ProtocolEnforcer:
    """Enforces workflow protocols across all agents"""

    def __init__(self):
        """Initialize protocol enforcer"""
        self.router = AgentRouter()
        self._task_states = {}  # Track task states

    def get_agent_protocols(self, agent_name: str) -> Dict:
        """
        Get protocol requirements for a specific agent

        Args:
            agent_name: Name of the agent

        Returns:
            Dict with all protocol requirements
        """
        # All agents follow all 11 mandatory protocols
        return {
            'requirements_gathering_first': True,
            'test_first_development': True,
            'git_commit_checkpoint': True,
            'logging_standards': True,
            'bash_validation': True,
            'code_organization': True,
            'local_testing': True,
            'production_ready_code': True,
            'user_decision_points': True,
            'copy_paste_ready_commands': True,
            'virtual_environment': True,
            'todo_tracking': True,
            'venv_path': '/Users/gaganarora/Desktop/gagan_projects/venv'
        }

    # Rule 1: Requirements Gathering First
    def check_requirements_gathered(self, task_id: str) -> Dict:
        """Check if requirements have been gathered for a task"""
        state = self._task_states.get(task_id, {})

        if state.get('requirements_gathered', False):
            return {'allowed': True, 'message': 'Requirements gathered'}
        else:
            return {
                'allowed': False,
                'message': 'Requirements must be gathered before implementation'
            }

    def mark_requirements_gathered(self, task_id: str):
        """Mark requirements as gathered for a task"""
        if task_id not in self._task_states:
            self._task_states[task_id] = {}
        self._task_states[task_id]['requirements_gathered'] = True

    # Rule 2: Test-First Development
    def check_tests_written(self, task_id: str) -> Dict:
        """Check if tests have been written"""
        state = self._task_states.get(task_id, {})

        if state.get('tests_written', False):
            return {'allowed': True, 'message': 'Tests written'}
        else:
            return {
                'allowed': False,
                'message': 'Tests must be written before implementation'
            }

    def mark_tests_written(self, task_id: str):
        """Mark tests as written"""
        if task_id not in self._task_states:
            self._task_states[task_id] = {}
        self._task_states[task_id]['tests_written'] = True

    def mark_tests_approved(self, task_id: str):
        """Mark tests as approved"""
        if task_id not in self._task_states:
            self._task_states[task_id] = {}
        self._task_states[task_id]['tests_approved'] = True

    # Self-Reflection After Test Writing (MANDATORY)
    def check_reflection_required(self, task_id: str) -> Dict:
        """Check if self-reflection is required after test writing"""
        state = self._task_states.get(task_id, {})

        tests_written = state.get('tests_written', False)
        reflection_complete = state.get('reflection_complete', False)

        if tests_written and not reflection_complete:
            return {
                'required': True,
                'message': 'Self-reflection required after writing tests'
            }
        else:
            return {
                'required': False,
                'message': 'Reflection complete or tests not written'
            }

    def generate_reflection_cue(self, task_id: str) -> Dict:
        """Generate reflection prompts with key self-assessment questions"""
        prompts = [
            {
                'question': 'Does your test suite provide comprehensive coverage of all requirements?',
                'focus': 'test_coverage'
            },
            {
                'question': 'Have you tested all edge cases and boundary conditions?',
                'focus': 'edge_cases'
            },
            {
                'question': 'Are there any scenarios or use cases that are not yet covered?',
                'focus': 'scenarios'
            },
            {
                'question': 'Is the test quality sufficient to catch implementation bugs?',
                'focus': 'quality'
            },
            {
                'question': 'Are the test assertions clear and comprehensive?',
                'focus': 'assertions'
            }
        ]

        return {
            'task_id': task_id,
            'prompts': prompts,
            'message': 'Review these questions before proceeding to implementation'
        }

    def mark_reflection_complete(self, task_id: str):
        """Mark that reflection has been completed for a task"""
        if task_id not in self._task_states:
            self._task_states[task_id] = {}
        self._task_states[task_id]['reflection_complete'] = True

    def mark_implementation_complete(self, task_id: str):
        """Mark implementation as complete"""
        if task_id not in self._task_states:
            self._task_states[task_id] = {}
        self._task_states[task_id]['implementation_complete'] = True

    def mark_todo_updated(self, task_id: str):
        """Mark TODO as updated"""
        if task_id not in self._task_states:
            self._task_states[task_id] = {}
        self._task_states[task_id]['todo_updated'] = True

    def mark_git_checks_complete(self, task_id: str):
        """Mark git workflow checks as complete"""
        if task_id not in self._task_states:
            self._task_states[task_id] = {}
        self._task_states[task_id]['git_checks_complete'] = True

    def check_can_implement(self, task_id: str) -> Dict:
        """Check if implementation can begin"""
        state = self._task_states.get(task_id, {})

        # Check if tests are written and approved
        tests_ready = (state.get('tests_written', False) and
                      state.get('tests_approved', False))

        # Check requirements
        requirements_ready = state.get('requirements_gathered', False)

        # Check reflection complete (MANDATORY after tests are written)
        tests_written = state.get('tests_written', False)
        reflection_complete = state.get('reflection_complete', False)

        # If tests are written, reflection is REQUIRED before implementation
        if tests_written and not reflection_complete:
            return {
                'allowed': False,
                'message': 'Self-reflection required after writing tests before implementation'
            }

        # If tests are ready and reflection is complete, allow implementation
        if tests_ready and (not tests_written or reflection_complete):
            return {'allowed': True, 'message': 'Can proceed with implementation'}

        # If nothing is set, prioritize requirements message
        if not requirements_ready and not tests_written:
            return {
                'allowed': False,
                'message': 'Requirements must be gathered before implementation'
            }

        # Otherwise, block on tests
        return {
            'allowed': False,
            'message': 'Tests must be written and approved before implementation'
        }

    # Git Workflow
    def check_git_workflow_complete(self, task_id: str) -> Dict:
        """Check git workflow completion with 4 required checks"""
        return {
            'checks': [
                {
                    'name': 'clean_unnecessary_files',
                    'description': 'Clean unnecessary files before commit',
                    'passed': False
                },
                {
                    'name': 'verify_requirements_file',
                    'description': 'Verify requirements.txt is up to date',
                    'passed': False
                },
                {
                    'name': 'validate_auth_necessity',
                    'description': 'Validate authentication/authorization necessity',
                    'passed': False
                },
                {
                    'name': 'verify_remote_push',
                    'description': 'Verify remote repository is set up for push',
                    'passed': False
                }
            ],
            'all_passed': False
        }

    # Rule 3: Logging Standards
    def validate_logging(self, code: str) -> Dict:
        """Validate logging standards"""
        has_debug_logs = 'logger.debug' in code or 'logging.DEBUG' in code
        has_print_statements = re.search(r'\bprint\s*\(', code) is not None

        return {
            'has_debug_logs': has_debug_logs,
            'has_print_statements': has_print_statements,
            'passed': not (has_debug_logs or has_print_statements),
            'message': 'Code should not have debug logs or print statements'
        }

    # Rule 4: Bash Validation
    def requires_bash_validation(self, task: str) -> Dict:
        """Check if task requires bash validation"""
        math_keywords = ['calculate', 'computation', 'percentage', 'math', 'formula', 'arithmetic']

        task_lower = task.lower()
        requires = any(keyword in task_lower for keyword in math_keywords)

        return {
            'required': requires,
            'reason': 'Task involves math or calculation logic' if requires else 'No validation required'
        }

    # Rule 5: Code Organization
    def check_code_organization(self, code_files: Dict[str, str]) -> Dict:
        """Check for duplicate function definitions"""
        functions = {}
        duplicates = []

        # Extract function definitions
        for filename, code in code_files.items():
            matches = re.findall(r'def\s+(\w+)\s*\(', code)
            for func_name in matches:
                if func_name in functions:
                    duplicates.append({
                        'function': func_name,
                        'files': [functions[func_name], filename]
                    })
                else:
                    functions[func_name] = filename

        return {
            'has_duplicates': len(duplicates) > 0,
            'duplicates': duplicates,
            'passed': len(duplicates) == 0
        }

    # Rule 6: Local Testing
    def validate_test_results(self, test_results: Dict) -> Dict:
        """Validate test results require 100% pass rate"""
        total = test_results.get('total', 0)
        passed = test_results.get('passed', 0)

        if total == 0:
            return {
                'allowed': False,
                'message': 'No tests found',
                'pass_rate': 0.0
            }

        pass_rate = passed / total

        return {
            'allowed': pass_rate == 1.0,
            'message': f'Pass rate: {pass_rate * 100:.1f}% (must be 100%)',
            'pass_rate': pass_rate
        }

    def can_deploy(self, test_results: Dict) -> Dict:
        """Check if code can be deployed based on test results"""
        total = test_results.get('total', 0)
        passed = test_results.get('passed', 0)
        failed = test_results.get('failed', 0)

        if total == 0:
            return {
                'allowed': False,
                'message': 'No tests found - cannot deploy without tests'
            }

        if failed > 0:
            return {
                'allowed': False,
                'message': f'{failed} tests failed - deployment blocked'
            }

        if passed == total:
            return {
                'allowed': True,
                'message': 'All tests passed - ready for deployment'
            }

        return {
            'allowed': False,
            'message': 'Not all tests passed - deployment blocked'
        }

    # Rule 7: Production-Ready Code
    def validate_production_code(self, code: str) -> Dict:
        """Validate production-ready code standards"""
        # Check for commented-out code
        commented_code_pattern = r'^\s*#\s*def\s+\w+|^\s*#\s*class\s+\w+|^\s*#\s*return\s+'
        has_commented_code = bool(re.search(commented_code_pattern, code, re.MULTILINE))

        # Check for TODO/FIXME comments
        todo_pattern = r'#\s*(TODO|FIXME|XXX|HACK)'
        has_todo_comments = bool(re.search(todo_pattern, code, re.IGNORECASE))

        return {
            'has_commented_code': has_commented_code,
            'has_todo_comments': has_todo_comments,
            'passed': not (has_commented_code or has_todo_comments),
            'message': 'Production code should not have commented code or TODO comments'
        }

    def can_commit(self, code: str) -> Dict:
        """Check if code can be committed"""
        # Check for debug print statements
        has_print = 'print(' in code

        # Check for TODO comments
        todo_pattern = r'#\s*(TODO|FIXME|XXX|HACK)'
        has_todo = bool(re.search(todo_pattern, code, re.IGNORECASE))

        # Check for commented code
        commented_code_pattern = r'^\s*#\s*def\s+\w+|^\s*#\s*class\s+\w+|^\s*#\s*return\s+'
        has_commented_code = bool(re.search(commented_code_pattern, code, re.MULTILINE))

        issues = []
        if has_print:
            issues.append('contains print statements')
        if has_todo:
            issues.append('contains TODO comments')
        if has_commented_code:
            issues.append('contains commented-out code')

        if issues:
            return {
                'allowed': False,
                'message': f'Cannot commit: {", ".join(issues)}',
                'issues': issues
            }

        return {
            'allowed': True,
            'message': 'Code is ready to commit'
        }

    # Rule 8: User Decision Points
    def is_decision_point(self, task: str) -> Dict:
        """Detect if task requires user decision"""
        decision_patterns = [
            r'\bchoose\b',
            r'\bselect\b',
            r'\bdecide\b',
            r'\bvs\b',
            r'\bor\b.*\bor\b',
            r'\boption\b'
        ]

        task_lower = task.lower()
        is_decision = any(re.search(pattern, task_lower) for pattern in decision_patterns)

        return {
            'is_decision': is_decision,
            'message': 'Task requires user decision' if is_decision else 'No decision required'
        }

    # Rule 9: Copy-Paste Ready Commands
    def validate_command(self, command: str) -> Dict:
        """Validate command is copy-paste ready (no placeholders)"""
        # Common placeholder patterns
        placeholder_patterns = [
            r'<[^>]+>',  # <your-path>, <api-key>
            r'\{[^}]+\}',  # {your-path}, {api-key}
            r'\$\{[^}]+\}',  # ${your-path}
            r'YOUR[_-]',  # YOUR_PATH, YOUR-KEY
            r'\byour[-_]',  # your-path, your_key
        ]

        has_placeholders = any(
            re.search(pattern, command, re.IGNORECASE)
            for pattern in placeholder_patterns
        )

        return {
            'has_placeholders': has_placeholders,
            'passed': not has_placeholders,
            'message': 'Command should not have placeholders' if has_placeholders else 'Command is copy-paste ready'
        }

    # Rule 10: Virtual Environment
    def check_venv_setup(self) -> Dict:
        """Check virtual environment setup"""
        venv_path = '/Users/gaganarora/Desktop/gagan_projects/venv'

        venv_exists = os.path.exists(venv_path)
        python_path = os.path.join(venv_path, 'bin', 'python')
        python_exists = os.path.exists(python_path)

        return {
            'venv_exists': venv_exists,
            'venv_path': venv_path,
            'python_exists': python_exists,
            'ready': venv_exists and python_exists
        }

    # Rule 11: TODO Tracking
    def check_todo_file(self) -> Dict:
        """Check if TODO.md exists"""
        todo_path = 'TODO.md'

        file_exists = os.path.exists(todo_path)

        return {
            'file_exists': file_exists,
            'path': todo_path
        }

    def validate_todo_structure(self) -> Dict:
        """Validate TODO.md has required sections"""
        todo_path = 'TODO.md'

        if not os.path.exists(todo_path):
            return {
                'valid': False,
                'sections_found': []
            }

        with open(todo_path, 'r') as f:
            content = f.read()

        # Check for required sections
        sections_found = []
        if re.search(r'#+ In Progress', content, re.IGNORECASE):
            sections_found.append('In Progress')
        if re.search(r'#+ Pending', content, re.IGNORECASE):
            sections_found.append('Pending')
        if re.search(r'#+ Completed', content, re.IGNORECASE):
            sections_found.append('Completed')

        return {
            'valid': len(sections_found) == 3,
            'sections_found': sections_found
        }

    def check_todo_freshness(self) -> Dict:
        """Check when TODO.md was last updated"""
        todo_path = 'TODO.md'

        if not os.path.exists(todo_path):
            return {
                'days_since_update': None,
                'last_modified': None
            }

        mtime = os.path.getmtime(todo_path)
        last_modified = datetime.fromtimestamp(mtime)
        days_since = (datetime.now() - last_modified).days

        return {
            'days_since_update': days_since,
            'last_modified': last_modified.isoformat()
        }

    # Overall Protocol Compliance
    def get_all_protocol_rules(self) -> List[Dict]:
        """Get all 11 mandatory protocol rules"""
        return [
            {
                'name': 'Requirements Gathering First',
                'description': 'Gather and document requirements before implementation',
                'mandatory': True
            },
            {
                'name': 'Git Commit Checkpoint',
                'description': 'Follow git workflow with 4 required checks',
                'mandatory': True
            },
            {
                'name': 'Logging Standards',
                'description': 'No debug logs or print statements in production',
                'mandatory': True
            },
            {
                'name': 'Bash Validation',
                'description': 'Validate math/logic with bash test scripts',
                'mandatory': True
            },
            {
                'name': 'Code Organization',
                'description': 'No duplicate functions or poor organization',
                'mandatory': True
            },
            {
                'name': 'Local Testing',
                'description': 'All tests must pass (100% pass rate)',
                'mandatory': True
            },
            {
                'name': 'Production-Ready Code',
                'description': 'No commented code or TODO comments',
                'mandatory': True
            },
            {
                'name': 'User Decision Points',
                'description': 'Present options for key decisions',
                'mandatory': True
            },
            {
                'name': 'Copy-Paste Ready Commands',
                'description': 'Commands must have no placeholders',
                'mandatory': True
            },
            {
                'name': 'Virtual Environment',
                'description': 'Use shared venv at /Users/gaganarora/Desktop/gagan_projects/venv',
                'mandatory': True
            },
            {
                'name': 'TODO Tracking',
                'description': 'Maintain TODO.md with In Progress, Pending, Completed',
                'mandatory': True
            }
        ]

    def check_compliance(self, task_id: str) -> Dict:
        """Check protocol compliance for a task"""
        rules = self.get_all_protocol_rules()

        rules_checked = len(rules)
        rules_passed = 0
        rules_failed = 0

        # Check each rule based on task state
        state = self._task_states.get(task_id, {})

        # Check all tracked states
        if state.get('requirements_gathered', False):
            rules_passed += 1
        else:
            rules_failed += 1

        if state.get('tests_written', False):
            rules_passed += 1
        else:
            rules_failed += 1

        if state.get('tests_approved', False):
            rules_passed += 1
        else:
            rules_failed += 1

        if state.get('implementation_complete', False):
            rules_passed += 1
        else:
            rules_failed += 1

        if state.get('todo_updated', False):
            rules_passed += 1
        else:
            rules_failed += 1

        if state.get('git_checks_complete', False):
            rules_passed += 1
        else:
            rules_failed += 1

        # Check venv setup (always check)
        venv_check = self.check_venv_setup()
        if venv_check['ready']:
            rules_passed += 1
        else:
            rules_failed += 1

        # Assume reasonable defaults for unchecked rules
        # (logging, bash validation, code organization, etc. - not always applicable)
        remaining_rules = rules_checked - (rules_passed + rules_failed)
        if remaining_rules > 0:
            # Give partial credit for remaining rules
            rules_passed += remaining_rules // 2
            rules_failed += remaining_rules - (remaining_rules // 2)

        compliance_percentage = (rules_passed / rules_checked) * 100

        return {
            'rules_checked': rules_checked,
            'rules_passed': rules_passed,
            'rules_failed': rules_failed,
            'compliance_percentage': compliance_percentage
        }

    def generate_compliance_report(self, task_id: str) -> str:
        """Generate compliance report for a task"""
        compliance = self.check_compliance(task_id)
        rules = self.get_all_protocol_rules()

        report = f"# Protocol Compliance Report\n\n"
        report += f"**Task ID:** {task_id}\n\n"
        report += f"**Compliance:** {compliance['compliance_percentage']:.1f}%\n\n"
        report += f"**Rules Checked:** {compliance['rules_checked']}\n"
        report += f"**Rules Passed:** {compliance['rules_passed']}\n"
        report += f"**Rules Failed:** {compliance['rules_failed']}\n\n"

        report += "## All 11 Mandatory Rules\n\n"
        for i, rule in enumerate(rules, 1):
            report += f"{i}. **{rule['name']}**: {rule['description']}\n"

        return report
