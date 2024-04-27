<p align="center">
  <a href="/">
    <img src="assets/codevet-bg.png" width="318px" alt="CodeVet logo" />
</a>
<h3 align="center">Open-source LLM Powered Code Review Tool</h3>
<p align="center">
  <a href="/">
    <img src="https://img.shields.io/github/stars/darshpanchal/codevet
    " alt="GitHub Stars" />
  </a>
</p>

CodeVet is an LLM powered git pull request review tool for Gitea and GitHub. Supports OpenAI and self-hosted open-source OpenAI compatible servers like [llama-cpp-python](https://github.com/abetlen/llama-cpp-python).

### Working

This tool uses webhooks of Gitea/GitHub. Once webhook is triggered on 'Pull Request' event, this tool will fetch the git diff
of the opened pull request and then send it to LLM for reviewing. Once LLM returns the review, this tool will push that review to Gitea/GitHub as a comment on the pull request. If there is any kind of failure, a generic error message would be posted to pull request as a comment indicating failure.

### Prerequisites

- Edit `config.ini` and change `modelAlias` to name of the model you are using.
- Edit `config.ini` and change `userToken` to base64 of text `username:password` of your Gitea account. Also `baseUrl` for `GITEA` to your gitea instance URL. (Alternative, for GitHub create a personal access token and paste it in config file under `accessToken` for `GITHUB`)

### Usage

Build the container:
```bash
docker build -t codevet .
```
Run the container: (change OPENAI_API_KEY as per your OpenAI API key)
```bash
docker run -d --name codevet -p 8001:8001 -v $PWD:/home -e UVICORN_HOST=0.0.0.0 -e OPENAI_API_KEY=sk-xxxx codevet
```

Once the containers are up, create a webhook in Gitea repo for `http://<host-server>:8001/review`

### OpenAI Compatible Models

If you prefer using self-hosted models. You can use any OpenAI compatible server like [llama-cpp-python](https://github.com/abetlen/llama-cpp-python).

> **Checkout my other repo [llm-server](https://github.com/darshpanchal/llm-server), its a dockerized OpenAI compatible server based on [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)**

Once you have server deployed, modify `config.ini` and change `baseUrl` (under `LLMSERVER`) value to the server link. 

### Limitations
- So far it only works on `opened` event for PR.
- Provided user prompt for LLM might not work for you, so you can change it according the model you are using.
- Can be inaccurate if git diff doesn't have enough changes.

### Future
- [ ] Supporting Gitlab
- [ ] Supporting other events like Push and PR updates.

### Libraries Used
- [fastapi](https://github.com/tiangolo/fastapi)
- [openai-python](https://github.com/openai/openai-python)
- [uvicorn](https://github.com/encode/uvicorn)
- [httpx](https://github.com/encode/httpx/)

## Authors

- [@darshpanchal](https://www.github.com/darshpanchal)
