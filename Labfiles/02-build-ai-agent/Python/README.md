# 🤖 AI Data Analysis Agent 📊

## What is this? 🤔

This simple Python script (`agent.py`) creates an AI agent that can analyze data files and make charts for you!

## How it works 🛠️

1. 📁 **Loads your data file**: The script reads the data from `data.txt`
2. 🔌 **Connects to Azure AI**: Uses your Azure credentials to connect to Azure AI services
3. 📤 **Uploads your data**: Sends your data to the AI agent
4. 🧠 **Creates an AI agent**: Makes a smart AI agent that can analyze your data
5. 💬 **Chats with you**: You can type questions about your data
6. 📊 **Creates charts**: If you ask for a chart, it will make one and save it as a PNG file
7. 🔄 **Keeps chatting until you type "quit"**
8. 💾 **Saves any charts**: All charts are saved to your current folder

## How to use it 👨‍💻

1. Make sure you have a `.env` file with:
   ```
   PROJECT_ENDPOINT=your_azure_endpoint
   MODEL_DEPLOYMENT_NAME=your_model_name
   ```

2. Run the script:
   ```
   python agent.py
   ```

3. Ask questions about your data! Try these:
   - "Summarize this data for me"
   - "Create a bar chart showing the trends"
   - "Calculate the average values"
   - "Make a pie chart of the distribution"

4. Type "quit" to exit

## Example conversation 💬

```
> Enter a prompt: What patterns do you see in this data?
Agent: I notice there's a seasonal trend with higher values in summer months...

> Enter a prompt: Make a line chart showing the monthly trend
Agent: I've created a line chart showing the monthly trends. The image has been saved.

> Enter a prompt: quit
```

## What's happening behind the scenes 🔍

The script uses:
- 🔑 Azure AI credentials to access Azure services
- 🧩 Azure AI Agents API to create and manage the AI agent
- 📝 Code interpreter tool that lets the AI run Python code to analyze data
- 📷 Image saving capability to save charts as PNG files

That's it! Now you can chat with an AI about your data file! 🎉
