import httpx
from abc import ABC, abstractmethod
import os

class GitService(ABC):
    """
    Abstract base class for Git services.
    Defines the interface for interacting with Git providers.
    """
    def __init__(self, config, llm_service):
        self.config = config
        self.llm_service = llm_service

    @abstractmethod
    def get_pr_diff(self):
        """Fetches the pull request diff."""
        pass

    @abstractmethod
    def post_review_on_git(self, comment_text):
        """Posts a review comment on the pull request."""
        pass

    def pr_created(self):
        """
        Handles the PR creation event.
        Fetches the diff, gets a review from the LLM, and posts the review.
        """
        diff_data = self.get_pr_diff()
        review = self.llm_service.getReviewFromLLM(diff_data)
        response = self.post_review_on_git(review)
        return response


class GiteaService(GitService):
    """
    Service class for interacting with Gitea.
    """
    def __init__(self, config, llm_service, request_data):
        super().__init__(config, llm_service)
        self.owner = request_data["repository"]["owner"]["username"]
        self.repo = request_data["repository"]["name"]
        self.index = request_data["pull_request"]["id"]
        self.headers = {
            'authorization': f"Basic {os.environ.get('GITEA_USER_TOKEN')}",
        }

    def get_pr_diff(self):
        """
        Fetches the pull request diff from Gitea.
        """
        url = self.config["GITEA"]['diffUrl'].format(
            baseUrl=self.config['GITEA']['baseUrl'],
            owner=self.owner,
            repo=self.repo,
            index=str(self.index)
        )
        response = httpx.get(url, headers=self.headers, verify=False)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception("Failed to get PR Diff.")

    def post_review_on_git(self, comment_text):
        """
        Posts a review comment on the Gitea pull request.
        """
        url = self.config["GITEA"]['issueCommentUrl'].format(
            baseUrl=self.config['GITEA']['baseUrl'],
            owner=self.owner,
            repo=self.repo,
            index=str(self.index)
        )
        comment = {"body": comment_text}
        response = httpx.post(url, headers=self.headers, json=comment, verify=False)
        if response.status_code != 201:
            raise Exception("Failed to post review comment on Gitea.")
        return "Posted the Review Comment to Issue"


class GitHubService(GitService):
    """
    Service class for interacting with GitHub.
    """
    def __init__(self, config, llm_service, request_data):
        super().__init__(config, llm_service)
        self.owner = request_data["repository"]["owner"]["login"]
        self.repo = request_data["repository"]["name"]
        self.index = request_data["pull_request"]["number"]
        self.headers = {
            'authorization': f"Bearer {os.environ.get('GITHUB_ACCESS_TOKEN')}",
            'X-GitHub-Api-Version': '2022-11-28'
        }

    def get_pr_diff(self):
        """
        Fetches the pull request diff from GitHub.
        """
        url = self.config["GITHUB"]['diffUrl'].format(
            owner=self.owner,
            repo=self.repo,
            index=str(self.index)
        )
        response = httpx.get(url, headers=self.headers, verify=False)
        if response.status_code == 200:
            diff_url = response.json()['diff_url']
            diff_response = httpx.get(diff_url, headers=self.headers, verify=False)
            return diff_response.text
        else:
            raise Exception("Failed to get PR Diff.")

    def post_review_on_git(self, comment_text):
        """
        Posts a review comment on the GitHub pull request.
        """
        url = self.config["GITHUB"]['issueCommentUrl'].format(
            owner=self.owner,
            repo=self.repo,
            index=str(self.index)
        )
        comment = {"body": comment_text}
        headers = self.headers.copy()
        headers['Accept'] = 'application/vnd.github+json'
        response = httpx.post(url, headers=headers, json=comment, verify=False)
        if response.status_code != 201:
            raise Exception("Failed to post review comment on GitHub.")
        return "Posted the Review Comment to Issue"
