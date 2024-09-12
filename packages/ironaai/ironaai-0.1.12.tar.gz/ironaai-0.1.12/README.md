# Getting started with Irona AI

Irona AI is an AI model router that automatically determines which LLM is best-suited to respond to any query, improving LLM output quality by combining multiple LLMs into a **meta-model** that learns when to call each LLM.

# Key features

- **[Maximize output quality](https://ironaai.readme.io/docs/quickstart)**: Irona AI [outperforms every foundation model](https://ironaai.readme.io/docs/benchmark-performance) on major evaluation benchmarks by always calling the best model for every prompt.
- **[Reduce cost and latency](https://ironaai.readme.io/docs/cost-and-latency-tradeoffs)**: Irona AI lets you define intelligent cost and latency tradeoffs to efficiently leverage smaller and cheaper models without degrading quality.
- **[Train your own router](https://ironaai.readme.io/docs/router-training-quickstart)**: Irona AI lets you train your own custom routers optimized to your data and use case.
- **[Python](https://python.ironaai.ai/), [TypeScript](https://www.npmjs.com/package/ironaai), and [REST API](https://ironaai.readme.io/reference/api-introduction) support**: Irona AI works across a variety of stacks.

# Installation

**Python**: Requires **Python 3.10+**. It’s recommended that you create and activate a [virtualenv](https://virtualenv.pypa.io/en/latest/) prior to installing the package. For this example, we'll be installing the optional additional `create` dependencies, which you can learn more about [here](https://ironaai.readme.io/docs/model_select-vs-create).

```shell
pip install ironaai
```

# Setting up

Create a `.env` file with your [Irona AI API key](https://app.ironaai.ai/keys) and the [API keys of the models](https://ironaai.readme.io/docs/api-keys) you want to route between:

```shell
IRONAAI_API_KEY = "YOUR_IRONAAI_API_KEY"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
ANTHROPIC_API_KEY = "YOUR_ANTHROPIC_API_KEY"
```

# Sending your first Irona AI API request

Create a new file in the same directory as your `.env` file and copy and run the code below (you can toggle between  Python and TypeScript in the top left of the code block):

```python
from ironaai import IronaAI

# Define the Irona AI routing client
client = IronaAI()

# The best LLM is determined by Irona AI based on the messages and specified models
result, session_id, provider = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Concisely explain merge sort."}  # Adjust as desired
    ],
    model=['openai/gpt-3.5-turbo', 'openai/gpt-4o', 'anthropic/claude-3-5-sonnet-20240620']
)

print("ND session ID: ", session_id)   # A unique ID of Irona AI's recommendation
print("LLM called: ", provider.model)  # The LLM routed to
print("LLM output: ", result.content)  # The LLM response
```
