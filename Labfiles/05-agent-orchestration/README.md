# 🤖 Agent Orchestration - Multi-Agent System

Welcome to the Agent Orchestration lab! This project demonstrates how to build a sophisticated multi-agent system using Azure AI and Semantic Kernel for automated incident management.

## 📋 Overview

This application simulates a real-world DevOps incident management system where two AI agents work together to analyze log files and automatically resolve issues:

- 🕵️ **Incident Manager Agent**: Analyzes log files and determines appropriate actions
- 🛠️ **DevOps Assistant Agent**: Executes the recommended remediation actions

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Log Files   │───▶│ Incident Manager│───▶│ DevOps Assistant│
│                 │    │     Agent       │    │     Agent       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        📄                      🧠                      ⚙️
```

## 🔧 Core Components

### 1. 🎯 Main Application (`main()`)

The main function orchestrates the entire workflow:

```python
async def main():
    # 🧹 Clear the console for clean output
    os.system('cls' if os.name=='nt' else 'clear')
    
    # 📁 Copy sample log files to working directory
    # 🔐 Set up Azure authentication
    # 🤖 Create and configure AI agents
    # 💬 Initialize group chat between agents
    # 🔄 Process each log file iteratively
```

**Key Features:**
- ✅ Automatic log file management
- 🔒 Secure Azure credential handling
- ⏱️ Rate limiting to prevent API throttling
- 🛡️ Exception handling for robust operation

### 2. 🕵️ Incident Manager Agent

**Purpose**: The "brain" of the system that analyzes problems and makes decisions.

```python
INCIDENT_MANAGER_INSTRUCTIONS = """
Analyze the given log file or the response from the devops assistant.
Recommend which one of the following actions should be taken:

Restart service {service_name}      # 🔄 Service restart
Rollback transaction               # ↩️ Transaction rollback  
Redeploy resource {resource_name}  # 🚀 Resource redeployment
Increase quota                     # 📈 Quota adjustment
"""
```

**Capabilities:**
- 📖 Reads and analyzes log files using `LogFilePlugin`
- 🎯 Identifies specific issues and their severity
- 📋 Recommends appropriate corrective actions
- 🚨 Escalates complex issues when needed

### 3. 🛠️ DevOps Assistant Agent

**Purpose**: The "hands" of the system that executes remediation actions.

```python
DEVOPS_ASSISTANT_INSTRUCTIONS = """
Read the instructions from the INCIDENT_MANAGER and apply the appropriate resolution function.
Return the response as "{function_response}"
"""
```

**Available Actions:**
- 🔄 **restart_service()**: Restarts failed services
- ↩️ **rollback_transaction()**: Reverts problematic transactions
- 🚀 **redeploy_resource()**: Redeploys failed resources
- 📈 **increase_quota()**: Adjusts system quotas
- 🆘 **escalate_issue()**: Escalates unresolvable issues

### 4. 🎭 Agent Orchestration Strategies

#### 🔄 Selection Strategy
```python
class SelectionStrategy(SequentialSelectionStrategy):
    """Determines which agent speaks next in the conversation"""
```

**Logic Flow:**
```
User Message ──▶ Incident Manager ──▶ DevOps Assistant ──▶ Incident Manager
     🧑                🕵️                    🛠️                 🕵️
```

#### 🛑 Termination Strategy
```python
class ApprovalTerminationStrategy(TerminationStrategy):
    """Determines when the conversation should end"""
```

**Termination Conditions:**
- ✅ Issue resolved ("no action needed")
- 🔢 Maximum iterations reached (10)
- 🔄 Automatic reset for next log file

### 5. 🔌 Plugin System

#### 📄 LogFilePlugin
```python
@kernel_function(description="Accesses the given file path string and returns the file contents")
def read_log_file(self, filepath: str = "") -> str:
    # Safely reads log files and returns content
```

#### ⚙️ DevopsPlugin
Contains all the remediation functions with detailed logging:

```python
@kernel_function(description="A function that restarts the named service")
def restart_service(self, service_name: str = "", logfile: str = "") -> str:
    # 📝 Logs the restart process
    # ✅ Returns success confirmation
```

## 🚀 Workflow Example

1. 📥 **Input**: System processes `log1.log`
2. 🔍 **Analysis**: Incident Manager reads and analyzes the log
3. 💡 **Decision**: Determines "Restart service WebAPI" is needed
4. 🛠️ **Action**: DevOps Assistant executes the restart
5. 📝 **Logging**: Updates log file with remediation actions
6. ✅ **Completion**: Incident Manager confirms resolution

## 🛡️ Error Handling & Rate Limiting

The system includes robust error handling:

```python
try:
    # 🤖 Agent conversation
    async for response in chat.invoke():
        # Process responses
except Exception as e:
    if "Rate limit is exceeded" in str(e):
        print("Waiting...")
        await asyncio.sleep(60)  # ⏰ Wait for rate limit reset
```

## 📊 Key Features

- 🔄 **Asynchronous Processing**: Handles multiple operations concurrently
- 📝 **Comprehensive Logging**: Detailed audit trail of all actions
- 🎯 **Targeted Remediation**: Specific actions for different issue types
- 🔒 **Secure Authentication**: Azure credential management
- 🛡️ **Fault Tolerance**: Graceful handling of API limits and errors
- 📈 **Scalable Architecture**: Easy to add new agents and capabilities

## 🎮 Running the Application

```bash
# 🐍 Activate your Python environment
source labenv/bin/activate

# 📦 Install dependencies (if needed)
pip install -r requirements.txt

# 🚀 Run the application
python agent_chat.py
```

## 📁 File Structure

```
05-agent-orchestration/
├── 📄 agent_chat.py          # Main application
├── 📖 README.md              # This documentation
├── 📁 sample_logs/           # Template log files
├── 📁 logs/                  # Working log files
└── 📁 labenv/                # Python environment
```

## 🔮 Advanced Concepts

### 🧠 Agent Collaboration
The agents use a sophisticated communication pattern:
- 📤 **Asynchronous messaging** between agents
- 🔄 **Turn-based conversation** with intelligent selection
- 📋 **Context preservation** across multiple interactions

### 🎯 Plugin Architecture
- 🔌 **Modular design** allows easy extension
- 🏷️ **Function decorators** enable automatic discovery
- 📝 **Rich descriptions** help agents understand capabilities

### 🛠️ DevOps Integration
- 📊 **Real-time log analysis**
- 🔧 **Automated remediation**
- 📈 **Performance monitoring**
- 🚨 **Escalation procedures**

---

🎉 **Congratulations!** You now have a powerful multi-agent system that can automatically detect, analyze, and resolve infrastructure issues. This represents a significant step toward autonomous IT operations! 🚀
