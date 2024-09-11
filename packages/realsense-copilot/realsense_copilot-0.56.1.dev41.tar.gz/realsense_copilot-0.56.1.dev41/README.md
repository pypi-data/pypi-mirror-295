
<!-- Edit README.md, not index.md -->

# RealSense Copilot is AI pair programming tool for Intel RealSense cameras in your terminal.

RealSense Copilot (based on Aider) lets you pair program with LLMs,
to write and edit code in your local git repository.
Start a new project or work with an existing git repo.
Realsense works best with GPT-4o & Claude 3.5 Sonnet and can
[connect to almost any LLM](https://aider.chat/docs/llms.html).

## Getting started

You can get started quickly like this:

```
$ pip install realsense-copilot

# Change directory into a git repo
cd /to/your/git/repo

# Work with Claude 3.5 Sonnet on your repo
$ export ANTHROPIC_API_KEY=your-key-goes-here
$ realsense demo.py

# Work with GPT-4o on your repo
$ export OPENAI_API_KEY=your-key-goes-here
$ realsense demo.py
```

See the
[installation instructions](https://aider.chat/docs/install.html)
and other
[documentation](https://aider.chat/docs/usage.html)
for more details.

## Features

- Run realsense copilot with the files you want to edit: `realsense <file1> <file2> ...`
- `realsense demo.py`
- Ask for changes:
  - Detect a person and their distance. Move the robot to the person. Stop when it reaches their feet.
  - `/run python3 demo.py`
  - If the resulting code, outputs a bug, simply add it to the chat by pressing "y" and Realsense will attempt to fix the bug so you can re /run your app.
  - Add new features or test cases.
- Realsense will edit your files to complete your request.
- Realsense [automatically git commits](https://aider.chat/docs/git.html) changes with a sensible commit message.
- Realsense works with [most popular languages](https://aider.chat/docs/languages.html): python, javascript, typescript, php, html, css, and more...
- Realsense works best with GPT-4o & Claude 3.5 Sonnet and can [connect to almost any LLM](https://aider.chat/docs/llms.html).
- Realsense can edit multiple files at once for complex requests.
- Realsense uses a [map of your entire git repo](https://aider.chat/docs/repomap.html), which helps it work well in larger codebases.
- Edit files in your editor while chatting with aider, and it will always use the latest version.
