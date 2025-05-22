import os
from dotenv import load_dotenv
from typing import Any
from pathlib import Path


# Add references
from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import FunctionTool, ToolSet, ListSortOrder, MessageRole


# Assuming user_functions is a Python file defining functions
from user_functions import user_functions


def main():

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    # Load environment variables from .env file
    load_dotenv()
    project_endpoint= os.getenv("PROJECT_ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")


    # Connect to the Agent client
    # The 'with' statement should encompass the entire usage of the client
    with AgentsClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        )
    ) as agent_client: # Use 'as' to assign the client within the 'with' block

        functions = FunctionTool(user_functions)
        toolset = ToolSet()
        toolset.add(functions)
        agent_client.enable_auto_function_calls(toolset)

        agent = agent_client.create_agent(
            model=model_deployment,
            name="support-agent",
            instructions="""You are a technical support agent.
                         When a user has a technical issue, you get their email address and a description of the issue.
                         Then you use those values to submit a support ticket using the function available to you.
                         If a file is saved, tell the user the file name.
                      """,
            toolset=toolset
        )

        thread = agent_client.threads.create()
        print(f"You're chatting with: {agent.name} ({agent.id})")


        # Loop until the user types 'quit'
        # THIS WHILE LOOP MUST BE INSIDE THE 'with agent_client:' BLOCK
        while True:
            # Get input text
            user_prompt = input("Enter a prompt (or type 'quit' to exit): ")
            if user_prompt.lower() == "quit":
                break
            if len(user_prompt) == 0:
                print("Please enter a prompt.")
                continue

            # Send a prompt to the agent - Now inside the 'with' block
            message = agent_client.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_prompt
            )
            run = agent_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)

            # Check the run status for failures
            if run.status == "failed":
                print(f"Run failed: {run.last_error}")

            # Show the latest response from the agent
            last_msg = agent_client.messages.get_last_message_text_by_role(
                thread_id=thread.id,
                role=MessageRole.AGENT,
            )
            if last_msg:
                print(f"Last Message: {last_msg.text.value}")

            # Get the conversation history
            print("\nConversation Log:\n")
            messages = agent_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
            for message in messages:
                if message.text_messages:
                    last_msg = message.text_messages[-1]
                    print(f"{message.role}: {last_msg.text.value}\n")

            # Note: Agent deletion is better done once after the loop,
            # outside the loop but still potentially managed by the client's scope.
            # However, if you want to delete the agent immediately after the chat session ends (user types 'quit'),
            # the cleanup should happen *after* the loop breaks but *before* the 'with' block finishes.
            # Let's move the cleanup *after* the loop, but it's still within the 'with' block's influence
            # which is fine as the client is still open.

    # Cleanup after the loop finishes (when user types 'quit') - This block is now outside the while loop,
    # but still inside the 'with' block's scope, so agent_client is valid here.
    try:
        # Note: The thread cleanup might also be desired here, but wasn't in the original code.
        # agent_client.threads.delete(thread.id)
        agent_client.delete_agent(agent.id)
        print("Deleted agent")
    except Exception as e:
        # This catch is useful if deletion fails for some reason
        print(f"Could not delete agent {agent.id}: {e}")

# The 'with' block finishes here, and agent_client is automatically closed.


if __name__ == '__main__':
    main()