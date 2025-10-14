"""
Agent Configuration Loader
Loads and validates agent configuration from YAML
"""

import os
import yaml
from typing import Dict, List, Optional
from .errors import AgentConfigError


class AgentConfig:
    """Loads and manages agent configuration"""

    _instance = None
    _config_cache = None
    _cached_path = None

    def __new__(cls, config_path: Optional[str] = None):
        """Singleton pattern for config caching"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration loader"""
        if config_path is None:
            self.config_path = os.path.join(
                os.path.dirname(__file__),
                'agents.yaml'
            )
        else:
            self.config_path = config_path

        # Load config if not cached or path changed
        if AgentConfig._config_cache is None or AgentConfig._cached_path != self.config_path:
            self._load_config()
            AgentConfig._cached_path = self.config_path

        self.agents = AgentConfig._config_cache

    def _load_config(self):
        """Load configuration from YAML file"""
        try:
            if not os.path.exists(self.config_path):
                raise AgentConfigError(f"Config file not found: {self.config_path}")

            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)

            if config is None:
                raise AgentConfigError("Config file is empty")

            # Validate and cache
            self._validate_config(config)
            AgentConfig._config_cache = config

        except yaml.YAMLError as e:
            raise AgentConfigError(f"Invalid YAML: {e}")
        except Exception as e:
            raise AgentConfigError(f"Failed to load config: {e}")

    def _load_from_path(self, path: str):
        """Load configuration from a specific path (used for testing)"""
        if not os.path.exists(path):
            raise AgentConfigError(f"Config file not found: {path}")

        with open(path, 'r') as f:
            config = yaml.safe_load(f)

        if config is None:
            raise AgentConfigError("Config file is empty")

        # Validate and cache
        self._validate_config(config)
        self.agents = config

    def _validate_config(self, config: Dict):
        """Validate configuration structure"""
        if not isinstance(config, dict):
            raise AgentConfigError("Config must be a dictionary")

        # Check for at least some categories
        if len(config) == 0:
            raise AgentConfigError("Config has no agent categories")

        # Validate each agent
        all_names = set()
        for category, agents in config.items():
            if not isinstance(agents, list):
                raise AgentConfigError(f"Category {category} must contain a list")

            for agent in agents:
                self._validate_agent(agent)

                # Check for duplicates
                if agent['name'] in all_names:
                    raise AgentConfigError(f"Duplicate agent name: {agent['name']}")
                all_names.add(agent['name'])

    def _validate_agent(self, agent: Dict):
        """Validate individual agent definition"""
        required_fields = ['name', 'description', 'keywords', 'file_path']

        for field in required_fields:
            if field not in agent:
                raise AgentConfigError(f"Agent missing required field: {field}")

        # Validate keywords
        if not isinstance(agent['keywords'], list) or len(agent['keywords']) == 0:
            raise AgentConfigError(f"Agent {agent['name']} must have keywords list")

        # Validate file path
        if not os.path.exists(agent['file_path']):
            raise AgentConfigError(f"Agent file not found: {agent['file_path']}")

    def _check_duplicates(self):
        """Check for duplicate agent names"""
        all_names = []
        for category, agents in self.agents.items():
            for agent in agents:
                all_names.append(agent['name'])

        if len(all_names) != len(set(all_names)):
            raise AgentConfigError("Duplicate agent names found")

    def get_agent_by_name(self, name: str) -> Optional[Dict]:
        """Get agent by name"""
        for category, agents in self.agents.items():
            for agent in agents:
                if agent['name'] == name:
                    return {**agent, 'category': category}
        return None

    def get_agents_by_category(self, category: str) -> List[Dict]:
        """Get all agents in a category"""
        if category not in self.agents:
            return []

        agents = []
        for agent in self.agents[category]:
            agents.append({**agent, 'category': category})
        return agents

    def get_all_agents(self) -> List[Dict]:
        """Get all agents as flat list"""
        all_agents = []
        for category, agents in self.agents.items():
            for agent in agents:
                all_agents.append({**agent, 'category': category})
        return all_agents

    def get_default_agent(self) -> Dict:
        """Get default agent (Senior Developer)"""
        for agent in self.get_all_agents():
            if agent.get('is_default', False):
                return agent

        # Fallback: return first engineering agent
        return self.get_agents_by_category('engineering')[0]

    def search_agents(self, keyword: str) -> List[Dict]:
        """Search agents by keyword"""
        keyword_lower = keyword.lower()
        results = []

        for agent in self.get_all_agents():
            # Search in keywords
            for kw in agent['keywords']:
                if keyword_lower in kw.lower():
                    results.append(agent)
                    break

        return results

    def reload(self):
        """Reload configuration from file"""
        AgentConfig._config_cache = None
        self._load_config()
        self.agents = AgentConfig._config_cache

    @classmethod
    def clear_cache(cls):
        """Clear singleton instance and cache (useful for testing)"""
        cls._instance = None
        cls._config_cache = None
        cls._cached_path = None
