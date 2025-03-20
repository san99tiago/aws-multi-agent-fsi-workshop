---
title: "Architecture"
weight: 32
---

# Original Architecture 🏗️

![Original Architecture](/static/03-images/original-architecture-pending-items.png)

Based on the initial architecture provided by RUFUS Bank, you were able to detect the key functionalities and enhance it towards a more robust and organized diagram:

> Note: the RED components in the original diagram are part of your duties in the Workshop!

<br>

![Enhanced Architecture](/static/multi-agent-chatbot-fsi-v1.png)

# Enhanced Architecture 🏗️

## System Components

### Frontend Layer 🖥️

- **Content Delivery**: Amazon CloudFront distribution
- **Static Hosting**: Amazon S3 bucket
- **Features**:
  - Responsive chat interface
  - Real-time message updates
  - Secure user session management
  - Browser-based PDF document upload

### Backend Services 🔧

- **API Layer**: Amazon API Gateway
- **Processing**: AWS Lambda functions
- **Data Storage**: Amazon DynamoDB
  - Chat history persistence
  - User session management
  - Transaction logs
- **Key Functions**:
  - Real-time message routing
  - Conversation state management
  - Document handling

### Generative AI Engine 🤖

- **Supervisor Agent**

  - Built on Amazon Bedrock (Amazon Nova Pro)
  - Orchestrates all child agents
  - Maintains conversation context
  - Routes requests based on intent

- **Specialized Agents**:

  1. Product Information Agent
  2. Transaction Management Agent
  3. Certificate Generation Agent
  4. Credit Services Agent
  5. Customer Support Agent (RAG-enabled)

- **Support Systems**:
  - Knowledge Base for Q&A
  - RAG for document processing
  - Custom LLM instruction for assistant

### Security Controls 🛡️

- **Bedrock Guardrails**:
  - Content filtering
  - Topic restrictions
  - Personal data protection
  - Compliance enforcement

## Data Flow

1. User request enters through CloudFront
2. API Gateway routes to appropriate Lambda
3. Lambda initiates Gen-AI processing
4. Supervisor Agent analyzes request
5. Task routed to specialized agent
6. Response filtered through Guardrails
7. Result stored in DynamoDB
8. Response returned to user

---

::alert[This architecture represents the enhanced version of RUFUS Bank's original design.]{header="Architecture Note" type="info"}
