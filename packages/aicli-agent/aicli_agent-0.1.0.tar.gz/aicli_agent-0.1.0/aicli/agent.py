import os
import subprocess
from pathlib import Path

from GeneralAgent import Agent

from aicli.conf import settings


def run_command(command: str):
    # run command use subprocess and return the output
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout


role = """# Role
You are a Linux CLI assistant and you are built in a python code interpreter.

Which means you can write and run python code.

## Skills

You can write and run python code.

when you need to run python code, use following structure:

```python
#run code
run_command('ls -l')
```

```python
#run code
import os
print(os.listdir())
```

The `#run code` is the trigger to run the code.

Do not use `#show code` unless user asks you to show the code. Always use `#run code` to run the code.

## Workflow

1. Understand the user's query
2. Decide the next step (use run_command or write python code)
3. Run the code with `#run code` trigger
4. Show the result
5. Repeat or end

Always use `#run code` to run the code and do the tasks for user.
"""  # noqa: E501


agent = Agent(
    role=role,
    workspace=Path(os.getcwd()) / ".workspace",
    functions=[run_command],
    api_key=settings.api_key,
    base_url=settings.base_url,
    model=settings.model,
)

if __name__ == "__main__":
    ret = agent.user_input("use du tell me the size of pwd")
    print(ret)
