import streamlit as st
from typing import Dict, Any, Callable, List, Union
import inspect
import json
from functools import wraps
from taskflowai import Task
from pydantic import BaseModel, Field

class ToolCall(BaseModel):
    tool: str
    params: Dict[str, Any] = Field(default_factory=dict)
    result: Union[str, Dict[str, Any], None] = None

def tool_call_component(call: ToolCall):
    with st.expander(f"🛠️ Tool Call: {call.tool}", expanded=False):
        st.markdown("**Tool:**")
        st.code(f"{call.tool}", language="text")
        if call.params:
            st.markdown("**Parameters:**")
            st.code(json.dumps(call.params, indent=2), language="json")
        else:
            st.code("No parameters provided", language="text")
        
        st.markdown("**Result**")
        if isinstance(call.result, str):
            st.code(call.result, language="text")
        elif isinstance(call.result, dict):
            st.code(json.dumps(call.result, indent=2), language="json")
        else:
            st.code(json.dumps(call.result, indent=2, default=str), language="json")

    return {"role": "assistant", "content": f"Tool '{call.tool}' was called."}

def wrap_task_func(task_func):
    @wraps(task_func)
    def wrapper(*args, **kwargs):
        task_result = {"tool_calls": [], "content": "", "error": None}

        def callback(result: Dict[str, Any]):
            if result["type"] == "tool_call":
                # Stringify the result if it's not a string or dict
                if not isinstance(result["result"], (str, dict)):
                    result["result"] = json.dumps(result["result"], default=str)
                tool_call = ToolCall(**result)
                tool_call_component(tool_call)
                task_result["tool_calls"].append(tool_call)
            elif result["type"] == "final_response":
                task_result["content"] = result["content"]
                st.write(result["content"])
            elif result["type"] == "error":
                task_result["error"] = result["content"]

        # Remove 'callback' from kwargs if it's there
        kwargs.pop('callback', None)

        # Check if the original function accepts a 'callback' parameter
        sig = inspect.signature(task_func)
        if 'callback' in sig.parameters:
            response = task_func(*args, **kwargs, callback=callback)
        else:
            # If the original function doesn't accept a callback, we need to modify its behavior
            original_create = Task.create

            def wrapped_create(*create_args, **create_kwargs):
                create_kwargs['callback'] = callback
                return original_create(*create_args, **create_kwargs)

            # Temporarily replace Task.create with our wrapped version
            Task.create = wrapped_create
            try:
                response = task_func(*args, **kwargs)
            finally:
                # Restore the original Task.create
                Task.create = original_create

        if isinstance(response, Exception):
            task_result["error"] = str(response)
            st.error(f"Error: {str(response)}")
        elif not task_result["content"] and not task_result["error"]:
            task_result["content"] = response if isinstance(response, str) else str(response)
            st.write(task_result["content"])

        return task_result

    return wrapper

def run_workflow(workflow_steps: List[Callable], form_data: Dict[str, Any]):
    results = {}
    for step in workflow_steps:
        step_name = step.__name__
        sig = inspect.signature(step)

        # Get the input arguments for the current step
        args = {}
        for param_name in sig.parameters:
            if param_name in form_data:
                args[param_name] = form_data[param_name]
            elif param_name in results:
                args[param_name] = results[param_name]

        st.subheader(f"{step_name.replace('_', ' ').title()}")
        with st.spinner(f"Running {step_name.replace('_', ' ').title()}..."):
            # Execute the step and get the result
            result = wrap_task_func(step)(**args)

        if isinstance(result, dict) and "error" in result and result["error"]:
            st.error(f"{step_name.replace('_', ' ').title()} encountered an error: {result['error']}")
            break
        else:
            st.success(f"{step_name.replace('_', ' ').title()} completed!")
            # Store the result using the parameter name of the next step
            next_step_params = inspect.signature(workflow_steps[workflow_steps.index(step) + 1]).parameters if workflow_steps.index(step) < len(workflow_steps) - 1 else {}
            for param_name in next_step_params:
                results[param_name] = result["content"]

    return results

def process_task(task_name: str, task_func: Callable, **kwargs) -> Any:
    result = task_func(**kwargs)
    if isinstance(result, Task):
        # If the result is a Task object, we need to execute it
        result = result.execute()
    st.write(result)
    return result

def create_workflow_ui(title: str, workflow_steps: List[Callable], input_fields: List[Dict[str, str]]) -> None:
    st.title(title)

    # Create input fields based on the provided input_fields list
    form_data = {}
    for field in input_fields:
        for key, label in field.items():
            form_data[key] = st.text_input(label)

    if st.button("Submit"):
        if all(form_data.values()):
            run_workflow(workflow_steps, form_data)
        else:
            st.error("Please fill in all required fields.")