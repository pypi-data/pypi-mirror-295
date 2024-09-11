from __future__ import annotations
import streamlit as st
from typing import Dict, Any, Callable, List, Literal, Optional, Union, Tuple
from taskflowai import Utils, Task
from functools import wraps
from pydantic import BaseModel, Field
import inspect
import json

class ToolCall(BaseModel):
    tool: str
    params: Dict[str, Any] = Field(default_factory=dict)
    result: Union[str, Dict[str, Any], None] = None

class Message(BaseModel):
    role: Literal["user", "assistant"]
    type: Literal["text", "tool_call"]
    content: Union[str, ToolCall]

class ChatState(BaseModel):
    messages: List[Message] = Field(default_factory=list)
    conversation_history: List[Dict[str, str]] = Field(default_factory=list)

    def add_message(self, role: Literal["user", "assistant"], msg_type: Literal["text", "tool_call"], content: Union[str, ToolCall]):
        message = Message(role=role, type=msg_type, content=content)
        self.messages.append(message)
        if msg_type == "text":
            self.conversation_history = Utils.update_conversation_history(
                self.conversation_history,
                role.capitalize(),
                content if isinstance(content, str) else content.tool
            )
        elif msg_type == "tool_call":
            self.conversation_history = Utils.update_conversation_history(
                self.conversation_history,
                role.capitalize(),
                f"Tool Call: {content.tool}"
            )

class Response(BaseModel):
    tool_calls: List[ToolCall] = Field(default_factory=list)
    content: Optional[str] = None
    error: Optional[str] = None

def render_tool_call(tool_call: ToolCall):
    with st.expander(f"🛠️ Tool Call: {tool_call.tool}", expanded=False):
        st.markdown("**Request**")
        st.markdown(f"**Tool:** `{tool_call.tool}`")
        if tool_call.params:
            st.markdown("**Parameters:**")
            st.json(tool_call.params)
        else:
            st.markdown("No parameters provided")
        
        st.markdown("\n**Result**")
        if isinstance(tool_call.result, str):
            st.text(tool_call.result)
        elif isinstance(tool_call.result, dict):
            st.json(tool_call.result)
        else:
            st.code(json.dumps(tool_call.result, indent=2, default=str), language="json")

def wrap_respond_func(respond_func: Callable, chat_ui: 'ChatUI') -> Callable:
    @wraps(respond_func)
    def wrapper(*args, **kwargs) -> Response:
        response = Response()
        error_reported = False

        def callback(result: Dict[str, Any]):
            nonlocal error_reported
            if result["type"] == "tool_call":
                tool_call = ToolCall(**result)
                response.tool_calls.append(tool_call)
                chat_ui.add_message("assistant", "tool_call", tool_call)
            elif result["type"] == "final_response":
                response.content = result["content"]
                chat_ui.add_message("assistant", "text", result["content"])
            elif result["type"] == "error" and not error_reported:
                response.error = result["content"]
                chat_ui.add_message("assistant", "text", f"Error: {result['content']}")
                error_reported = True

        kwargs.pop('callback', None)
        sig = inspect.signature(respond_func)
        if 'callback' in sig.parameters:
            result = respond_func(*args, **kwargs, callback=callback)
        else:
            original_create = Task.create

            def wrapped_create(*create_args, **create_kwargs):
                create_kwargs['callback'] = callback
                return original_create(*create_args, **create_kwargs)

            Task.create = wrapped_create
            try:
                result = respond_func(*args, **kwargs)
            finally:
                Task.create = original_create

        if isinstance(result, Exception) and not error_reported:
            response.error = str(result)
            chat_ui.add_message("assistant", "text", f"Error: {str(result)}")
            error_reported = True
        elif not response.content and not response.error:
            response.content = result if isinstance(result, str) else str(result)

        return response

    return wrapper

class ChatUI:
    def __init__(self, title: str, respond_func: Callable):
        self.title = title
        self.respond_func = wrap_respond_func(respond_func, self)
        if "chat_state" not in st.session_state:
            st.session_state.chat_state = ChatState()
        self.header_container = st.container()
        self.chat_container = st.container()
        self.spinner_container = st.empty()
        self.input_container = st.container()
        self.message_placeholders = []
        self.spinner_placeholder = st.empty()  # Add this line

    def render(self):
        with self.header_container:
            st.title(self.title)
            if st.button("Clear Chat"):
                st.session_state.chat_state = ChatState()
                self._clear_messages()
                st.rerun()

        self._render_new_messages()
        self._handle_user_input()

    def add_message(self, role: Literal["user", "assistant"], msg_type: Literal["text", "tool_call"], content: Union[str, ToolCall]):
        st.session_state.chat_state.add_message(role, msg_type, content)
        with self.chat_container:
            with st.chat_message(role):
                if msg_type == "text":
                    st.markdown(content)
                elif msg_type == "tool_call":
                    render_tool_call(content)

    def _render_new_messages(self):
        with self.chat_container:
            for idx, message in enumerate(st.session_state.chat_state.messages):
                if idx >= len(self.message_placeholders):
                    self.message_placeholders.append(st.empty())
                
                with self.message_placeholders[idx].container():
                    with st.chat_message(message.role):
                        if message.type == "text":
                            st.markdown(message.content)
                        elif message.type == "tool_call":
                            render_tool_call(message.content)

    def _handle_user_input(self):
        if prompt := st.chat_input("Type your message here..."):
            self.add_message("user", "text", prompt)

            with self.chat_container:
                with self.spinner_placeholder.container():
                    with st.spinner("AI is thinking..."):
                        response = self.respond_func(prompt, st.session_state.chat_state.conversation_history)

            self.spinner_placeholder.empty()

    def _clear_messages(self):
        for placeholder in self.message_placeholders:
            placeholder.empty()
        self.message_placeholders = []

def create_chat_ui(title: str, respond_func: Callable) -> ChatUI:
    chatui = ChatUI(title, respond_func)
    chatui.render()