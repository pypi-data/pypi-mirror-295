# chatollama

[![PyPI version](https://badge.fury.io/py/chatollama.svg)](https://badge.fury.io/py/chatollama)

**chatollama** is a simple interface for running chat-based Ollama models directly in your code. It provides an easy way to interact with large language models like LLaMA, enabling seamless message handling, streaming responses, and tool integration within Python applications.

## Features

- **Easy Integration**: Quickly integrate chat models into your applications with minimal setup.
- **Asynchronous Response Handling**: Runs responses in a separate thread, allowing your main application to continue running without blocking.
- **Streamlined Message Management**: Use `ChatMessages` to manage a branching message log, including user inputs, assistant responses, and system messages.
- **Tool Integration**: Allows for the execution of tool calls directly from the model's responses, enabling dynamic function handling.
- **Warmup Capability**: Easily warm up your models to reduce initial response latency.

## Installation

You can install this package via pip:

```bash
pip install chatollama
```


## Examples

Simple usage:
```py
from chatollama import ChatEngine

# Initialize the chat engine with the desired model
engine = ChatEngine(model="llama3.1:8b")

# Warm up the model
engine.warmup() # will ask the model to respond with the word Ready behind the scenes, this is a blocking function that will wait for it to finish

engine.messages.user("Hi can you help me?")
engine.messages.Assistant("As an AI I am happy to help!")
engine.messages.user("What is the capital of Egypt")
engine.chat() # this will start a thread to stream the models response. It will say something like 

# "The capital of Egypt is Cairo (also known as Al-Qāhira in Arabic)."

engine.wait() # this is a blocking function that will wait until the stream finishes
```

Message class:
```py
from chatollama import ChatMessages

# creates a message object that stores not just conversations but also branching conversations like the ChatGPT website
messages = ChatMessages()
message.system("You are JokeAI, an ai that tells jokes no matter what!!!")
message.user("Why am I having a hard time at school?")
message.assistant("Poor kid, can't even get school right. Probably because you're not laughing your way to A's, haha!")
message.user("That wasn't very nice...")
```


Using custom Stream and Tool callbacks:
```py
from chatollama import ChatEngine

# Define custom callback functions
# This function is called before the stream starts, as the stream is running, and after it finishes
def custom_stream_callback(mode, delta, text):
    if mode == 0: # before
        print("Starting Response:") 
    elif mode == 1: # during
        print(delta, end="")
    elif mode == 2: # after
        print("\nResponse Complete.")

# Define custom tool callback
# if the model supports tools, you can define a callback that returns that parsed tool response.
def custom_tool_callback(tool_response):
    print("Tool call made:", tool_response)

# Initialize the chat engine with custom callbacks
engine = ChatEngine()
engine.callback = custom_stream_callback
engine.tool_callback = custom_tool_callback

# How to use stream mode or tool mode
engine.use_tools = True/False
engine.tools = [] # Add your tools here

# Start the chat with callbacks
engine.chat()
```