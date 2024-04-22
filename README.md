# ChatLMSYS

ChatLMSYS is a Python package that automates chat.lmsys.org and enables you to run LLM programmatically.

## Installation

You can install ChatLMSYS using pip:
```bash
pip install git+https://github.com/neodyland/chat-lmsys
```

## Example

```py
import asyncio
from ChatLMSYS import ChatLMSYS, Model


chat = ChatLMSYS()

async def main():
    result = await chat.ask(
        Model.LLAMA_3_70B_INSTRUCT, "PythonでHello, World!を出力してください。"
    )
    print(result)

asyncio.run(main())

```
