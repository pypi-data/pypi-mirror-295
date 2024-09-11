# TaskFlowAI UI

TaskFlowAI UI is a set of user interface components built on top of the TaskFlowAI framework. It provides an easy way to create interactive chat-based and form-based interfaces for TaskFlowAI workflows.

## Installation

To install TaskFlowAI UI, run the following command:

```bash
pip install taskflowai_ui
```

## Components

TaskFlowAI UI includes two main components:

1. **ChatUI**: A multi-message chat interface for interacting with a single agent.
2. **FormUI**: A form-based interface for multi-agent, multi-task workflows.

### ChatUI

ChatUI is a user interface component that allows users to have a multi-message conversation with a single agent. It provides a chat-like experience where users can input messages and receive responses from the agent.

![ChatUI Example](chatui_image.png)

#### Implementing ChatUI

To implement ChatUI, follow these steps:

1. Create a TaskFlowAI agent using the `taskflowai` framework. Define the agent's role, goal, attributes, LLM, and tools. Here's an example from `math_agent.py`:

```python
from taskflowai.agent import Agent
from taskflowai.llm import OpenaiModels
from taskflowai.tools import CalculatorTools

math_agent = Agent(
    role="math agent",
    goal="use tools to assist the user with their request",
    attributes="hardworking, diligent, thorough, comprehensive.",
    llm=OpenaiModels.gpt_4o_mini,
    tools=[CalculatorTools.basic_math]
)
```

2. Define a task function that takes user input and conversation history as parameters and returns the agent's response. Here's an example from `math_agent.py`:

```python
def math_task(user_input, conversation_history):
    math_solution = Task.create(
        agent=math_agent,
        context=f"Conversation History: {conversation_history}\n------\nUser Request: {user_input}",
        instruction=f"Use your tools to solve the given math problem: {user_input}."
    )
    return math_solution
```

3. Create a ChatUI instance using the `create_chat_ui` function, passing the title and the task function as parameters. Here's an example from `math_agent_app.py`:

```python
from taskflowai_ui import create_chat_ui
from math_agent import math_task

chat_ui = create_chat_ui("Math Assistant", math_task)
chat_ui.render()
```

### FormUI

FormUI is a user interface component designed for multi-agent, multi-task workflows. It provides a form-based interface where users can input data, and the workflow is executed based on the provided input.

![FormUI Example](formui_image.png)

#### Implementing FormUI

To implement FormUI, follow these steps:

1. Create TaskFlowAI agents for each task in the workflow using the `taskflowai` framework. Define each agent's role, goal, attributes, LLM, and tools. Here's an example from `math_team.py`:

```python
from taskflowai import Agent, CalculatorTools, OpenaiModels

math_agent = Agent(
    role="math agent",
    goal="assist the user with their request",
    attributes="hardworking, diligent, thorough, comprehensive.",
    llm=OpenaiModels.gpt_4o_mini,
    tools=[CalculatorTools.basic_math]
)

tutor_agent = Agent(
    role="math tutor agent",
    goal="enhance given solutions",
    attributes="friendly, hardworking, and comprehensive and extensive in reporting back to users",
    llm=OpenaiModels.gpt_4o_mini,
)
```

2. Define task functions for each step in the workflow. Each task function should take the necessary input parameters and return the agent's response. Here's an example from `math_team.py`:

```python
def math_task(user_input):
    math_solution = Task.create(
        agent=math_agent,
        instruction=f"Use your tools to solve the given math problem: {user_input}."
    )
    return math_solution

def explanation_task(user_input, math_solution):
    explanation = Task.create(
        agent=tutor_agent,
        context=f"User Input: {user_input}\nMath Solution: {math_solution}",
        instruction="Given user input and the math solution, explain the solution in a way a 5th grader would understand."
    )
    return explanation
```

3. Define the workflow steps and input fields for the FormUI. The workflow steps should be a list of task functions, and the input fields should be a list of dictionaries specifying the key and label for each input field. Here's an example from `math_team_app.py`:

```python
from taskflowai_ui import create_workflow_ui
from math_team import math_task, explanation_task

workflow_steps = [
    math_task,
    explanation_task
]

input_fields = [
    {"key": "user_input", "label": "Enter your math problem"}
]

create_workflow_ui("Math Problem Solver", workflow_steps, input_fields)
```

## Usage

To use TaskFlowAI UI, follow these steps:

1. Install the `taskflowai_ui` package.
2. Import the desired component (`create_chat_ui` or `create_workflow_ui`) from `taskflowai_ui`.
3. Define your TaskFlowAI workflow using the TaskFlowAI framework.
4. Create an instance of the desired UI component, passing the necessary parameters.
5. Render the UI component to display the interface with 'streamlit run app_name_here.py'

For detailed examples and usage patterns, refer to the [TaskFlowAI UI documentation](https://taskflowai.org/ui).

## Contributing

Contributions to TaskFlowAI UI are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the [TaskFlowAI UI GitHub repository](https://github.com/taskflowai/taskflowai-ui).

## License

TaskFlowAI UI is released under the [MIT License](https://opensource.org/licenses/MIT).