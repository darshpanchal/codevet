import httpx
from .llmService import LLMService

class GitService:
    def __init__(self, config):
        self.config = config

    def prCreated(self):
        pass

    def getPrDiff(self):
        pass

    def postReviewOnGit(self, review):
        pass


class GiteaService(GitService):
    def __init__(self, config, requestData):
        super().__init__(config)
        self.owner = requestData["repository"]["owner"]["username"]
        self.repo = requestData["repository"]["name"]
        self.index = requestData["pull_request"]["id"]
        self.headers = {'authorization' : "Basic {userToken}".format(userToken = self.config['GITEA']['userToken'])}

    def prCreated(self):
        diffData = self.getPrDiff()
        review = LLMService(self.config).getReviewFromLLM(diffData)
        response = self.postReviewOnGit(review)
        return response

    def getPrDiff(self):
        url = self.config["GITEA"]['diffUrl'].format(baseUrl = self.config['GITEA']['baseUrl'], owner = self.owner,repo = self.repo, index = str(self.index))
        response = httpx.get(url, headers=self.headers, verify=False)
        if response.status_code == 200:
            diffData = response.text
        else:
            self.postReviewOnGit("Failed to get PR Diff.")
        return diffData

    def postReviewOnGit(self, commentText):
        url = self.config["GITEA"]['issueCommentUrl'].format(baseUrl = self.config['GITEA']['baseUrl'], owner = self.owner,repo = self.repo, index = str(self.index))
        comment = {"body" : commentText}
        response = httpx.post(url, headers=self.headers, json = comment, verify=False)
        if response.status_code != 201:
            raise HTTPException(status_code=500, detail="Failed to post review comment on Gitea.")
        
        return "Posted the Review Comment to Issue"


class GitHubService(GitService):
    def __init__(self, config, requestData):
        super().__init__(config)
        self.owner = requestData["repository"]["owner"]["login"]
        self.repo = requestData["repository"]["name"]
        self.index = requestData["pull_request"]["number"]
        self.headers = {'authorization' : "Bearer {accessToken}".format(accessToken = self.config['GITHUB']['accessToken']), 'X-GitHub-Api-Version': '2022-11-28'}

    def prCreated(self):
        diffData = self.getPrDiff()
        review = LLMService(self.config).getReviewFromLLM(diffData)
        response = self.postReviewOnGit(review)
        return response

    def getPrDiff(self):
        url = self.config["GITHUB"]['diffUrl'].format(owner = self.owner,repo = self.repo, index = str(self.index))
        response = httpx.get(url, headers=self.headers, verify=False)
        if response.status_code == 200:
            diffUrl = response.json()['diff_url']
            diffResponse = httpx.get(diffUrl, headers=self.headers, verify=False)
            diffData = diffResponse.text
        else:
            self.postReviewOnGit("Failed to get PR Diff.")
        return diffData

    def postReviewOnGit(self, commentText):
        headers = self.headers
        headers['Accept'] = 'application/vnd.github+json'
        url = self.config["GITHUB"]['issueCommentUrl'].format(owner = self.owner,repo = self.repo, index = str(self.index))
        comment = {"body" : commentText}
        response = httpx.post(url, headers=headers, json = comment, verify=False)
        if response.status_code != 201:
            raise HTTPException(status_code=500, detail="Failed to post review comment on GitHub.")
        
        return "Posted the Review Comment to Issue"
