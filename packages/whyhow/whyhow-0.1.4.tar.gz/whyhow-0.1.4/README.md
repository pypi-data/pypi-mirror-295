# WhyHow Knowledge Graph Studio SDK

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](https://opensource.org/licenses/MIT)
[![PyPI Version](https://img.shields.io/pypi/v/whyhow)](https://pypi.org/project/whyhow/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](https://img.shields.io/badge/mypy-checked-blue)](https://mypy-lang.org/)
<a href="https://discord.gg/9bWqrsxgHr" alt="WhyHow Discord community">
<picture>
  <img alt="WhyHow Discord community" src="https://invidget.switchblade.xyz/9bWqrsxgHr?theme=dark">
</picture>
</a>

The WhyHow Knowledge Graph Studio SDK enables you to quickly and easily build automated knowledge graphs tailored to your unique worldview. Instantly build, extend, and query well-scoped KGs with your data.

> [!WARNING]
> This SDK is currently in a closed beta. To get an API key, [please schedule some time to chat with us](https://calendly.com/whyhowai/intro-call-whyhow-ai).

# Installation

## Prerequisites

- Python 3.10 or higher

## Install from PyPI

You can install the SDK directly from PyPI using pip:

```shell
pip install whyhow

export WHYHOW_API_KEY=<YOUR_WHYHOW_API_KEY>
```

## Install from Github

Alternatively, you can clone the repo and install the package

```shell

git clone git@github.com:whyhow-ai/whyhow.git
cd whyhow
pip install .

export WHYHOW_API_KEY=<YOUR_WHYHOW_API_KEY>
```

# Examples

Navigate to the `examples/`.

## Initialize SDK

Import the SDK and initialize the client using your WhyHow API key.

```shell
from whyhow import WhyHow

client = WhyHow(api_key=<your whyhow api key>, base_url="https://api.whyhow.ai")
```

### Support

WhyHow.AI is building tools to help developers bring more determinism and control to their RAG pipelines using graph structures. If you're thinking about, in the process of, or have already incorporated knowledge graphs in RAG, we’d love to chat at team@whyhow.ai, or follow our newsletter at [WhyHow.AI](https://www.whyhow.ai/). Join our discussions about rules, determinism and knowledge graphs in RAG on our [Discord](https://discord.com/invite/9bWqrsxgHr).

We appreciate your interest.