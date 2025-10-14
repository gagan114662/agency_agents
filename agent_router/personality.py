"""
Agent Personality Loader
Loads and parses agent personality definitions from .md files
"""

import os
import re
import yaml
from typing import Dict, List, Optional
from .config import AgentConfig
from .errors import PersonalityLoadError


class AgentPersonality:
    """Loads and manages agent personality from .md files"""

    def __init__(self):
        """Initialize personality loader"""
        self.config = AgentConfig()
        self._cache = {}

    def load_agent(self, agent_name: str) -> Optional[Dict]:
        """
        Load agent personality from .md file

        Args:
            agent_name: Name of the agent to load

        Returns:
            Dict with personality data or None if agent not found
        """
        # Check cache first
        if agent_name in self._cache:
            return self._cache[agent_name]

        # Get agent config
        agent = self.config.get_agent_by_name(agent_name)
        if not agent:
            return None

        file_path = agent['file_path']
        if not os.path.exists(file_path):
            return None

        try:
            # Read and parse .md file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse the personality data
            personality = self._parse_personality_file(content, agent)
            personality['file_path'] = file_path

            # Cache and return
            self._cache[agent_name] = personality
            return personality

        except Exception as e:
            raise PersonalityLoadError(f"Failed to load {agent_name}: {e}")

    def load_agent_from_file(self, file_path: str) -> Optional[Dict]:
        """
        Load agent personality directly from a file path

        Args:
            file_path: Path to the .md file

        Returns:
            Dict with personality data or None if file not found
        """
        if not os.path.exists(file_path):
            return None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Create minimal agent dict for parsing
            agent = {
                'name': 'Unknown Agent',
                'description': 'Agent loaded from file'
            }

            personality = self._parse_personality_file(content, agent)
            personality['file_path'] = file_path
            return personality

        except Exception as e:
            return None

    def parse_markdown(self, markdown_content: str) -> Optional[Dict]:
        """
        Parse markdown content into personality structure

        Args:
            markdown_content: Raw markdown content

        Returns:
            Dict with personality data or None if parsing fails
        """
        try:
            # Create minimal agent dict
            agent = {
                'name': '',  # No default name
                'description': 'Parsed from markdown'
            }

            personality = self._parse_personality_file(markdown_content, agent)

            # If no name was extracted from frontmatter, remove the name field
            if personality.get('name') == '':
                personality.pop('name', None)

            return personality

        except Exception:
            return None

    def _parse_personality_file(self, content: str, agent: Dict) -> Dict:
        """Parse .md file content into structured personality data"""

        # Parse YAML frontmatter
        frontmatter = {}
        markdown_content = content

        if content.strip().startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1])
                    markdown_content = parts[2]
                except yaml.YAMLError:
                    pass

        # Initialize personality structure with frontmatter or defaults
        personality = {
            'name': frontmatter.get('name', agent['name']),
            'description': frontmatter.get('description', agent['description']),
            'core_mission': [],
            'communication_style': {
                'tone': [],
                'examples': []
            },
            'deliverables': [],
            'workflow_process': [],
            'critical_rules': {
                'requirements_gathering_first': True,
                'test_first_development': True
            },
            'success_metrics': []
        }

        # Parse sections using regex
        sections = self._split_into_sections(markdown_content)

        # Extract core mission
        if 'core mission' in sections or 'mission' in sections:
            section_key = 'core mission' if 'core mission' in sections else 'mission'
            personality['core_mission'] = self._extract_list_items(sections[section_key])

        # Extract communication style
        if 'communication style' in sections:
            comm_section = sections['communication style']
            personality['communication_style']['tone'] = self._extract_tone(comm_section)
            personality['communication_style']['examples'] = self._extract_examples(comm_section)

        # Extract deliverables
        if 'deliverables' in sections or 'technical deliverables' in sections:
            section_key = 'technical deliverables' if 'technical deliverables' in sections else 'deliverables'
            personality['deliverables'] = self._extract_deliverables(sections[section_key])

        # Extract workflow process
        if 'workflow' in sections or 'workflow process' in sections:
            section_key = 'workflow process' if 'workflow process' in sections else 'workflow'
            personality['workflow_process'] = self._extract_list_items(sections[section_key])

        # Extract critical rules
        if 'critical rules' in sections or 'rules' in sections:
            section_key = 'critical rules' if 'critical rules' in sections else 'rules'
            personality['critical_rules'] = self._extract_critical_rules(sections[section_key])

        # Extract success metrics
        if 'success metrics' in sections or 'metrics' in sections:
            section_key = 'success metrics' if 'success metrics' in sections else 'metrics'
            personality['success_metrics'] = self._extract_list_items(sections[section_key])

        return personality

    def _split_into_sections(self, content: str) -> Dict[str, str]:
        """Split markdown content into sections by headers"""
        sections = {}

        # Split by level 2 headers (##) only - subsections stay with their parent
        header_pattern = r'^##\s+(.+?)$'
        lines = content.split('\n')

        current_section = None
        current_content = []

        for line in lines:
            header_match = re.match(header_pattern, line, re.MULTILINE)
            if header_match:
                # Save previous section
                if current_section:
                    sections[current_section.lower()] = '\n'.join(current_content)

                # Start new section - clean the header text
                header_text = header_match.group(1).strip()
                # Remove emojis and clean up
                header_text = re.sub(r'[^\w\s-]', '', header_text)  # Remove non-alphanumeric except spaces and dashes
                header_text = header_text.strip().lower()
                # Remove "your" prefix if present
                header_text = re.sub(r'^your\s+', '', header_text)

                current_section = header_text
                current_content = []
            else:
                if current_section:
                    current_content.append(line)

        # Save last section
        if current_section:
            sections[current_section.lower()] = '\n'.join(current_content)

        return sections

    def _extract_list_items(self, section_text: str) -> List[str]:
        """Extract list items from markdown section"""
        items = []

        # Match bullet points (-, *, or numbered lists)
        pattern = r'^[\s]*[-\*\d]+[\.\)]*\s+(.+)$'

        for line in section_text.split('\n'):
            match = re.match(pattern, line.strip())
            if match:
                items.append(match.group(1).strip())

        return items

    def _extract_tone(self, section_text: str) -> List[str]:
        """Extract tone characteristics from communication style section"""
        tone_items = []

        # Look for "Tone:" section or bullet points
        lines = section_text.split('\n')
        in_tone_section = False

        for line in lines:
            if 'tone:' in line.lower():
                in_tone_section = True
                continue

            if in_tone_section:
                # Extract bullet points
                if line.strip().startswith('-') or line.strip().startswith('*'):
                    tone_items.append(line.strip().lstrip('-*').strip())
                elif line.strip() and not line.strip().startswith('#'):
                    # Non-bullet item after tone section
                    if not any(c.isalpha() for c in line[:10]):  # Skip if starts with formatting
                        continue
                    break

        # If no tone section found, extract from general bullet points
        if not tone_items:
            tone_items = self._extract_list_items(section_text)[:3]  # Take first 3

        return tone_items

    def _extract_examples(self, section_text: str) -> List[str]:
        """Extract communication examples from section"""
        examples = []

        # Look for quoted text or "Example:" sections
        # Match quoted text
        quote_pattern = r'[">](.+)'

        for line in section_text.split('\n'):
            quote_match = re.match(quote_pattern, line.strip())
            if quote_match:
                examples.append(quote_match.group(1).strip())

        # If no quotes found, look for example markers
        if not examples:
            in_example = False
            for line in section_text.split('\n'):
                if 'example' in line.lower():
                    in_example = True
                    continue
                if in_example and line.strip():
                    examples.append(line.strip())
                    if len(examples) >= 3:
                        break

        return examples if examples else ['Professional and technical communication']

    def _extract_deliverables(self, section_text: str) -> List[Dict]:
        """Extract deliverable templates from section"""
        deliverables = []

        lines = section_text.split('\n')
        current_deliverable = None
        current_content = []
        in_code_block = False

        for line in lines:
            # Check for ### subsection headers (deliverable titles)
            subsection_match = re.match(r'^###\s+(.+)$', line.strip())
            if subsection_match:
                # Save previous deliverable
                if current_deliverable:
                    deliverables.append({
                        'title': current_deliverable,
                        'content': '\n'.join(current_content).strip()
                    })

                # Start new deliverable from subsection
                current_deliverable = subsection_match.group(1).strip()
                current_content = []
                continue

            # Detect code blocks
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                if current_deliverable:
                    current_content.append(line)
                continue

            # New deliverable (bullet point or numbered) - only if no subsections found
            if not deliverables and not current_deliverable:
                if (line.strip().startswith('-') or line.strip().startswith('*') or
                    re.match(r'^\d+\.', line.strip())) and not in_code_block:

                    # Start new deliverable
                    current_deliverable = re.sub(r'^[-\*\d]+[\.\)]*\s+', '', line.strip())
                    current_content = []
                    continue

            # Accumulate content for current deliverable
            if current_deliverable:
                current_content.append(line)

        # Save last deliverable
        if current_deliverable:
            deliverables.append({
                'title': current_deliverable,
                'content': '\n'.join(current_content).strip()
            })

        return deliverables if deliverables else [
            {'title': 'Technical Implementation', 'content': 'Detailed implementation according to requirements'}
        ]

    def _extract_critical_rules(self, section_text: str) -> Dict:
        """Extract critical rules from section"""
        rules = {
            'requirements_gathering_first': True,
            'test_first_development': True
        }

        text_lower = section_text.lower()

        # Check for specific rules
        if 'requirements' in text_lower and 'first' in text_lower:
            rules['requirements_gathering_first'] = True

        if 'test' in text_lower and 'first' in text_lower:
            rules['test_first_development'] = True

        return rules

    def generate_response(self, agent: str, context: str, response_content: str) -> str:
        """
        Generate response in agent's communication style

        Args:
            agent: Agent name
            context: Task context
            response_content: The actual response content

        Returns:
            Formatted response with agent header and style
        """
        header = f"🎯 Acting as: {agent}\n\n"
        return header + response_content

    def format_response(self, agent_name: str, content: str) -> str:
        """
        Format response with agent header

        Args:
            agent_name: Name of the agent
            content: Response content

        Returns:
            Formatted response with header
        """
        return f"🎯 Acting as: {agent_name}\n\n{content}"

    def clear_cache(self):
        """Clear the personality cache"""
        self._cache = {}
