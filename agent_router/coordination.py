"""
Agent Coordination Planner
Generates coordination plans for multi-agent tasks
"""

from typing import Dict, List, Optional
from .router import AgentRouter
from .config import AgentConfig


class CoordinationPlanner:
    """Plans and coordinates multi-agent workflows"""

    def __init__(self):
        """Initialize coordination planner"""
        self.router = AgentRouter()
        self.config = AgentConfig()

    def generate_plan(self, task: str) -> Dict:
        """
        Generate coordination plan for a task

        Args:
            task: Task description

        Returns:
            Dict with complete coordination plan
        """
        # Analyze task to determine required agents
        analysis = self.router.analyze_task(task)

        # Get agents
        if analysis['is_multi_agent']:
            agents = analysis['required_agents']
        else:
            agents = [self.router.select_agent(task)]

        # Build agent details with roles and responsibilities
        agent_details = []
        for agent in agents:
            agent_details.append({
                'name': agent['name'],
                'category': agent['category'],  # Keep category for compatibility
                'role': agent['category'],
                'responsibilities': self._get_agent_responsibilities(agent, task)
            })

        # Generate sequence of steps
        sequence = self._generate_sequence(agents, task)

        # Generate handoff points
        handoff_points = self._generate_handoffs(agents, sequence)

        # Map dependencies
        dependencies = self._map_dependencies(sequence)

        # Estimate time
        estimated_time = self._estimate_time(sequence)

        # Identify parallel work opportunities
        parallel_groups = self._identify_parallel_work(agents, task)

        return {
            'task': task,
            'agents': agent_details,
            'sequence': sequence,
            'handoff_points': handoff_points,
            'dependencies': dependencies,
            'estimated_time': estimated_time,
            'parallel_groups': parallel_groups
        }

    def _get_agent_responsibilities(self, agent: Dict, task: str) -> List[str]:
        """Determine agent responsibilities based on role and task"""
        responsibilities = []

        category = agent['category']

        if category == 'design':
            responsibilities = [
                'Create design mockups and wireframes',
                'Define user experience flows',
                'Establish design system and components'
            ]
        elif category == 'engineering':
            if 'Frontend' in agent['name']:
                responsibilities = [
                    'Implement UI components',
                    'Integrate with backend APIs',
                    'Ensure responsive design'
                ]
            elif 'Backend' in agent['name']:
                responsibilities = [
                    'Design and implement API endpoints',
                    'Setup database schema',
                    'Handle business logic'
                ]
            else:
                responsibilities = [
                    'Gather and document requirements',
                    'Design technical architecture',
                    'Implement core functionality'
                ]
        elif category == 'testing':
            responsibilities = [
                'Write comprehensive test cases',
                'Perform integration testing',
                'Validate against requirements'
            ]
        elif category == 'product':
            responsibilities = [
                'Define product requirements',
                'Prioritize features',
                'Coordinate between teams'
            ]
        else:
            responsibilities = [
                'Complete assigned tasks',
                'Follow development protocols',
                'Deliver quality work'
            ]

        return responsibilities

    def _generate_sequence(self, agents: List[Dict], task: str) -> List[Dict]:
        """Generate ordered sequence of steps"""
        sequence = []
        step_number = 1

        # Step 1: Requirements gathering (always first)
        primary_agent = agents[0]
        sequence.append({
            'step_number': step_number,
            'agent': primary_agent['name'],
            'action': 'Gather and document requirements',
            'deliverable': 'Requirements document with clear specifications',
            'duration': '2 hours',
            'protocols': ['Requirements gathering first', 'Create TODO list', 'Git branch setup']
        })
        step_number += 1

        # Determine if there's a design phase
        has_designer = any('Designer' in agent['name'] or 'UX' in agent['name'] for agent in agents)

        if has_designer:
            designer = next((a for a in agents if 'Designer' in a['name'] or 'UX' in a['name']), None)
            if designer:
                sequence.append({
                    'step_number': step_number,
                    'agent': designer['name'],
                    'action': 'Design system architecture and user interface',
                    'deliverable': 'Design mockups, wireframes, and component library',
                    'duration': '4 hours',
                    'protocols': ['Follow design system', 'Create reusable components', 'Document decisions']
                })
                step_number += 1

        # Implementation phase - each agent does their work
        for agent in agents:
            if 'Designer' not in agent['name'] and 'UX' not in agent['name'] and \
               'Tester' not in agent['name'] and 'Checker' not in agent['name']:

                action = self._get_implementation_action(agent)
                deliverable = self._get_implementation_deliverable(agent)

                sequence.append({
                    'step_number': step_number,
                    'agent': agent['name'],
                    'action': action,
                    'deliverable': deliverable,
                    'duration': '6 hours',
                    'protocols': ['Test-first development', 'Git commits', 'Virtual environment', 'Follow TODO list']
                })
                step_number += 1

        # Testing phase (always include for implementation tasks)
        if any(word in task.lower() for word in ['build', 'implement', 'create', 'develop']):
            # Find a tester or use primary agent for testing
            tester = next((a for a in agents if 'Tester' in a['name'] or 'Checker' in a['name']), primary_agent)

            sequence.append({
                'step_number': step_number,
                'agent': tester['name'],
                'action': 'Test implementation and validate requirements',
                'deliverable': 'Test results, bug reports, and validation report',
                'duration': '3 hours',
                'protocols': ['Comprehensive testing', 'Test coverage', 'QA checklist']
            })
            step_number += 1

        # Deployment phase (if deployment mentioned or DevOps agent involved)
        if any(word in task.lower() for word in ['deploy', 'deployment', 'production', 'release']):
            # Find DevOps engineer or use primary agent
            devops = next((a for a in agents if 'DevOps' in a['name']), primary_agent)

            sequence.append({
                'step_number': step_number,
                'agent': devops['name'],
                'action': 'Deploy to production and setup monitoring',
                'deliverable': 'Deployed application with monitoring and CI/CD pipeline',
                'duration': '4 hours',
                'protocols': ['Infrastructure as code', 'Automated deployment', 'Monitoring setup']
            })
            step_number += 1

        return sequence

    def _get_implementation_action(self, agent: Dict) -> str:
        """Get implementation action based on agent type"""
        if 'Frontend' in agent['name']:
            return 'Implement frontend components and user interface'
        elif 'Backend' in agent['name']:
            return 'Implement backend APIs and business logic'
        elif 'Mobile' in agent['name']:
            return 'Implement mobile application features'
        elif 'AI' in agent['name']:
            return 'Implement AI models and integration'
        elif 'DevOps' in agent['name']:
            return 'Setup deployment pipeline and infrastructure'
        else:
            return 'Implement core functionality and features'

    def _get_implementation_deliverable(self, agent: Dict) -> str:
        """Get expected deliverable based on agent type"""
        if 'Frontend' in agent['name']:
            return 'Working frontend with all UI components'
        elif 'Backend' in agent['name']:
            return 'Functional backend with tested API endpoints'
        elif 'Mobile' in agent['name']:
            return 'Tested mobile application build'
        elif 'AI' in agent['name']:
            return 'Trained models and integration code'
        elif 'DevOps' in agent['name']:
            return 'Deployment pipeline and infrastructure code'
        else:
            return 'Implemented functionality with tests'

    def _generate_handoffs(self, agents: List[Dict], sequence: List[Dict]) -> List[Dict]:
        """Generate handoff points between agents"""
        handoffs = []

        # Create handoffs between consecutive different agents
        for i in range(len(sequence) - 1):
            current_step = sequence[i]
            next_step = sequence[i + 1]

            if current_step['agent'] != next_step['agent']:
                handoff = {
                    'from_agent': current_step['agent'],
                    'to_agent': next_step['agent'],
                    'deliverable': current_step['deliverable'],
                    'success_criteria': self._get_success_criteria(current_step, next_step)
                }
                handoffs.append(handoff)

        return handoffs

    def _get_success_criteria(self, from_step: Dict, to_step: Dict) -> List[str]:
        """Generate success criteria for handoff"""
        criteria = []

        # Generic criteria
        criteria.append('All deliverables completed and documented')
        criteria.append('Code committed to git repository')

        # Specific criteria based on step type
        if 'requirements' in from_step['action'].lower():
            criteria.append('Requirements clearly defined and validated')
            criteria.append('Acceptance criteria documented')

        if 'design' in from_step['action'].lower():
            criteria.append('Design approved by stakeholders')
            criteria.append('All components documented')

        if 'implement' in from_step['action'].lower():
            criteria.append('All tests passing')
            criteria.append('Code review completed')

        return criteria

    def _map_dependencies(self, sequence: List[Dict]) -> Dict[int, List[int]]:
        """Map dependencies between steps"""
        dependencies = {}

        # Each step depends on all previous steps (sequential workflow)
        for i, step in enumerate(sequence):
            step_num = step['step_number']
            if step_num > 1:
                # Depends on immediately previous step
                dependencies[step_num] = [step_num - 1]

        return dependencies

    def _estimate_time(self, sequence: List[Dict]) -> Dict:
        """Estimate total time for plan"""
        total_hours = 0

        for step in sequence:
            duration = step['duration']
            # Parse duration string (e.g., "2 hours")
            if 'hour' in duration:
                hours = float(duration.split()[0])
                total_hours += hours

        return {
            'total': total_hours,
            'unit': 'hours',
            'breakdown': {step['step_number']: step['duration'] for step in sequence}
        }

    def _identify_parallel_work(self, agents: List[Dict], task: str) -> List[List[str]]:
        """Identify opportunities for parallel work"""
        parallel_groups = []

        # Check if we have independent frontend and backend work
        has_frontend = any('Frontend' in agent['name'] for agent in agents)
        has_backend = any('Backend' in agent['name'] for agent in agents)

        if has_frontend and has_backend:
            parallel_groups.append([
                'Frontend Developer',
                'Backend Architect'
            ])

        # Check for multiple independent features
        if len(agents) >= 3:
            # Could potentially parallelize after design phase
            impl_agents = [
                agent['name'] for agent in agents
                if 'Designer' not in agent['name'] and
                   'Tester' not in agent['name'] and
                   'Product' not in agent['name']
            ]
            if len(impl_agents) >= 2:
                parallel_groups.append(impl_agents)

        return parallel_groups

    def generate_handoff_message(self, handoff: Dict) -> str:
        """
        Generate handoff message for communication

        Args:
            handoff: Handoff information dict

        Returns:
            Formatted handoff message
        """
        message = f"🔄 **Handoff: {handoff['from_agent']} → {handoff['to_agent']}**\n\n"
        message += f"**Deliverable:** {handoff['deliverable']}\n\n"
        message += "**Success Criteria:**\n"

        for criterion in handoff['success_criteria']:
            message += f"- {criterion}\n"

        return message

    def generate_mermaid_diagram(self, plan: Dict) -> str:
        """
        Generate Mermaid diagram of coordination flow

        Args:
            plan: Coordination plan

        Returns:
            Mermaid diagram string
        """
        diagram = "graph TD\n"

        # Add nodes for each step
        for step in plan['sequence']:
            step_num = step['step_number']
            agent = step['agent'].replace(' ', '_')
            action = step['action'][:40]  # Truncate for readability

            diagram += f"    Step{step_num}[\"{step_num}. {agent}: {action}\"]\n"

        # Add edges based on dependencies
        for step_num, deps in plan['dependencies'].items():
            for dep in deps:
                diagram += f"    Step{dep} --> Step{step_num}\n"

        # Add handoff annotations
        for handoff in plan['handoff_points']:
            from_agent = handoff['from_agent']
            to_agent = handoff['to_agent']
            diagram += f"    %% Handoff: {from_agent} to {to_agent}\n"

        return diagram

    def generate_summary(self, plan: Dict) -> str:
        """
        Generate text summary of coordination plan

        Args:
            plan: Coordination plan

        Returns:
            Human-readable summary
        """
        summary = f"## Coordination Plan: {plan['task']}\n\n"

        # Agents involved
        summary += f"**Agents Involved:** {len(plan['agents'])} specialists\n"
        for agent in plan['agents']:
            summary += f"- **{agent['name']}** ({agent['role']})\n"

        summary += "\n"

        # Sequence overview
        summary += f"**Execution Sequence:** {len(plan['sequence'])} steps\n"
        for step in plan['sequence']:
            summary += f"{step['step_number']}. {step['agent']}: {step['action']} ({step['duration']})\n"

        summary += "\n"

        # Handoffs
        if plan['handoff_points']:
            summary += f"**Handoff Points:** {len(plan['handoff_points'])}\n"
            for i, handoff in enumerate(plan['handoff_points'], 1):
                summary += f"{i}. {handoff['from_agent']} → {handoff['to_agent']}\n"

            summary += "\n"

        # Time estimate
        summary += f"**Estimated Time:** {plan['estimated_time']['total']} {plan['estimated_time']['unit']}\n"

        # Parallel work opportunities
        if plan['parallel_groups']:
            summary += f"\n**Parallel Work Opportunities:** {len(plan['parallel_groups'])} groups\n"
            for i, group in enumerate(plan['parallel_groups'], 1):
                summary += f"{i}. {', '.join(group)}\n"

        return summary
