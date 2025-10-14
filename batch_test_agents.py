#!/usr/bin/env python
"""Batch test all agent routing to identify failures"""

from agent_router.router import AgentRouter
from agent_router.config import AgentConfig

# Force reload
AgentConfig._config_cache = None
AgentConfig._cached_path = None

router = AgentRouter()

# Test data from test_all_37_agents.py
test_data = {
    'DevOps Automator': [
        "Set up CI/CD pipeline with GitHub Actions",
        "Configure Docker containers for deployment",
        "Create Kubernetes deployment manifests",
        "Automate infrastructure with Terraform",
        "Set up monitoring with Prometheus and Grafana",
        "Configure AWS Lambda functions",
        "Build automated deployment pipeline"
    ],
    'Rapid Prototyper': [
        "Build quick prototype to test idea",
        "Create MVP in 24 hours",
        "Rapid prototype for user testing",
        "Build proof of concept quickly",
        "Create functional demo for stakeholders",
        "Quick mockup with working features"
    ],
    'Senior Developer': [
        "Help me with my project",
        "Fix this bug",
        "Improve code quality",
        "General refactoring needed",
        "Review architecture decisions",
        "Mentor junior developers",
        "Complex system design needed"
    ]
}

print("Testing agent routing...\n")

for agent_name, tasks in test_data.items():
    print(f"=== {agent_name} ===")
    failures = []
    for task in tasks:
        selected = router.select_agent(task)
        if selected['name'] != agent_name:
            failures.append((task, selected['name']))

    if failures:
        print(f"  ✗ {len(failures)}/{len(tasks)} failed:")
        for task, wrong_agent in failures:
            print(f"    - '{task[:45]}' -> {wrong_agent}")
    else:
        print(f"  ✓ All {len(tasks)} tasks passed")
    print()
