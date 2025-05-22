# Agent Script Troubleshooting

This document addresses a common error encountered when running the `agent.py` script from the Azure AI Agents lab and provides the solution.

---

## Fixing the `ValueError: HTTP transport has already been closed` Error 🐛

When running the `agent.py` script, you might encounter the following traceback after successfully setting up the agent and thread and then entering the first prompt (e.g., "I have a technical problem"):

Traceback (most recent call last):
File "/workspaces/mslearn-ai-agents/Labfiles/03-ai-agent-functions/Python/agent.py", line XXX, in <module> # Line number may vary
main()
File "/workspaces/mslearn-ai-agents/Labfiles/03-ai-agent-functions/Python/agent.py", line YYY, in main # Line number may vary, often where messages.create is called
message = agent_client.messages.create(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
... (Additional traceback lines)
File "/workspaces/mslearn-ai-agents/Labfiles/03-ai-agent-functions/Python/labenv/lib/python3.12/site-packages/azure/core/pipeline/transport/_requests_basic.py", line ZZZ, in open # Line number may vary
raise ValueError(
ValueError: HTTP transport has already been closed. You may check if you're calling a function outside of the with of your client creation, or if you called close() on your client already.


**Problem Description:**

This error indicates that the `agent_client` object, which manages the connection and communication with the Azure AI service backend, was accessed after its underlying network connection had been closed. 🤔

**Root Cause:**

1.  **Incorrect `with` Statement Scope:** The `azure.ai.agents.AgentsClient` object is designed to be used within a Python `with` statement (`with AgentsClient(...) as client:`). The `with` statement ensures that resources are properly managed, including automatically closing the client's connection when the code exits the `with` block.
2.  In the original script structure, the `with agent_client:` block only included the initial setup steps (creating the agent and the thread).
3.  Immediately after these setup steps, the code exited the `with` block. At this point, the `agent_client`'s internal HTTP connection was automatically closed.
4.  The main interactive loop (`while True`) that handles user input and performs subsequent interactions with the agent (sending messages, processing runs, listing history) was located *outside* of this initial, now-closed `with` block.
5.  When the user entered the first prompt, the code attempted to call `agent_client.messages.create` inside the `while` loop. Since the client had already been closed upon exiting the initial `with` block, this call failed with the `ValueError`.

**Secondary Issue (Minor):**

The code attempted to use `MessageRole.AGENT` without explicitly importing `MessageRole` from `azure.ai.agents.models`. This would cause a `NameError` if the code reached that line.

**Solution:**

The fix involves extending the scope of the `with agent_client:` block to encompass all code that needs to use the `agent_client`, including the main interactive loop. This ensures the client connection remains open for the entire duration of the user session. ✨

Here are the specific changes:

1.  **Extend `with` Block Scope ✨:** Move the entire `while True` loop (responsible for handling user input and interacting with the agent) *inside* the `with AgentsClient(...) as agent_client:` block.
2.  **Add Missing Import ✅:** Add `MessageRole` to the import statement at the top of the file: `from azure.ai.agents.models import ..., MessageRole`.
3.  **Adjust Cleanup Placement (Improved Logic) 🧹:** Move the agent deletion call (`agent_client.delete_agent()`) to execute *after* the `while` loop breaks (when the user types 'quit'), but still *within* the extended `with` block. This is the logical place to clean up the agent resource, and it ensures the client is still open when the deletion is attempted. Added a `try...except` block around the deletion for robustness.

**Illustrative Code Change:**

Conceptually, the structure of your `main` function should change from this (simplified):

```python
def main():
    # ... setup env ...
    with AgentsClient(...) as agent_client:
        # Setup code (create agent, thread)
        agent = agent_client.create_agent(...)
        thread = agent_client.threads.create(...)
    # The 'with' block finishes here, client is closed

    # This loop runs AFTER the client is closed
    while True:
        # user input
        # agent_client.messages.create(...) # <-- FAILS here
        # ... rest of interaction code ...


To this (corrected):

def main():
    # ... setup env ...
    with AgentsClient(...) as agent_client:
        # Setup code (create agent, thread) - still inside 'with'
        agent = agent_client.create_agent(...)
        thread = agent_client.threads.create(...)
        print(...) # Initial welcome message

        # This loop runs INSIDE the 'with' block
        while True:
            # user input
            # agent_client.messages.create(...) # <-- SUCCEEDS now
            # ... rest of interaction code ...
            if user_input == 'quit':
                break # Exit the loop, but still inside 'with'

        # Cleanup code runs after loop, still inside 'with'
        try:
            agent_client.delete_agent(agent.id)
            print("Deleted agent")
        except Exception as e:
            print(f"Could not delete agent: {e}")

    # The 'with' block finishes here, client is closed automatically after all usage

# ... rest of file ...

By implementing these changes, the agent_client will remain valid and active for the entire duration of the user's chat session, resolving the HTTP transport has already been closed error. 🚀
