# 🧠 Semantic Kernel AI Agent for Expense Processing

This project demonstrates how to use Microsoft's Semantic Kernel framework to create an AI agent that processes expense data and simulates sending expense reports via email.

## 📋 Project Overview

The application uses an AI agent powered by Semantic Kernel to:
- 📂 Read expense data from a file
- 💬 Accept user instructions through prompts
- 📧 Process and send expense claims via a simulated email function
- 🤖 Interact with Azure AI services

## 🛠️ Technical Components

### Key Technologies
- **Semantic Kernel**: Framework for building AI agents with natural language processing capabilities
- **Azure AI**: Backend AI services that power the agent's intelligence
- **Python asyncio**: For asynchronous operations

### Code Structure

- **📄 semantic-kernel.py**: Main script that initializes and runs the AI agent
- **📄 data.txt**: Contains sample expense data in CSV format
- **📄 .env**: Configuration file for Azure AI services (requires setup)

### How It Works

1. 🔄 **Initialization**: Loads expense data and environment variables
2. 👨‍💼 **Agent Definition**: Creates an AI agent with specific instructions for expense processing
3. 🔌 **Plugin Integration**: Adds email functionality through a custom plugin
4. 💻 **User Interaction**: Accepts a prompt from the user about what to do with expense data
5. 📤 **Processing**: The agent processes the request and performs the requested action

## 🚀 Sample Usage & Output

When running the script, you'll see:

```
Here is the expenses data in your file:

date,description,amount
07-Mar-2025,taxi,24.00
07-Mar-2025,dinner,65.50
07-Mar-2025,hotel,125.90


What would you like me to do with it?

Submit an expense claim

To: expenses@contoso.com
Subject: Expense Claim
Expense Claim Submission:

Date: 07-Mar-2025
1. Taxi - $24.00
2. Dinner - $65.50
3. Hotel - $125.90

Total: $215.40 


# expenses_agent:
Your expense claim has been submitted with the following details:

- Taxi: $24.00
- Dinner: $65.50
- Hotel: $125.90
- Total: $215.40

A confirmation has been sent to the expenses department.
```

## ⚙️ Setup Instructions

1. Create a virtual environment using Python's venv:
   ```bash
   python -m venv labenv
   source labenv/bin/activate  # On Windows: labenv\Scripts\activate
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your `.env` file with:
   ```
   AZURE_AI_AGENT_ENDPOINT="your_project_endpoint_from_azure_ai_foundry"
   AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME="your_model_deployment"
   ```

4. Run the application:
   ```bash
   python semantic-kernel.py
   ```

## 🔑 Key Concepts

- **🧩 Plugins**: Extend the agent with custom functions (like email sending)
- **🤝 Agent Instructions**: Define the agent's behavior through natural language instructions
- **🧵 Agent Thread**: Manages the conversation state between user and agent

## 📝 Notes

- This is a demonstration using simulated email functionality
- For production use, replace the email plugin with actual email service integration
- Azure AI credentials must be properly configured in the .env file
