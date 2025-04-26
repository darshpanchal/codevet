from src.gitService import GitHubService, GiteaService
from src.util import getGitandEventType
from src.llmService import LLMService
import json

def get_git_service(config, request, request_data):
    """
    Factory function to return the appropriate Git service instance.
    Determines the Git provider (GitHub or Gitea) and initializes the corresponding service.
    """
    git, _ = getGitandEventType(request)  # Identify the Git provider and event type
    llm_service = LLMService(config)  # Instantiate the LLMService

    if git == 'GitHub':
        # Parse request data for GitHub
        request_data = json.loads(request_data["payload"])
        return GitHubService(config, llm_service, request_data)
    elif git == 'Gitea':
        # Initialize Gitea service
        return GiteaService(config, llm_service, request_data)
    else:
        # Raise an error for unsupported Git providers
        raise ValueError("Unsupported Git provider")