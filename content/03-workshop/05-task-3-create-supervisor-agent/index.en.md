---
title: "Task 3: Create Supervisor Agent"
weight: 35
---

# Supervisor Agent Details

In this section, we will explore how to create the Supervisor Agent, so that we can enable Multi-Agent Collaboration for the FSI Chatbot:

![Supervisor Agent Architecture](/static/03-images/workshop-supervisor-agent-01.png)

## Create Bedrock Agent

The first step is to go to the Bedrock Service, and click on "Create Agent". The proceed to fill the data as follows:

- Name: `supervisor-agent`
- Check: `Enable Multi-Agent Collaboration`

![Supervisor Agent Edit](/static/03-images/workshop-supervisor-agent-02.png)

Now proceed to edit/configure the agent as follows:

- IAM Permissions: Use an existing service role `fsi-multi-agents-bedrock-agent-role`

::alert[For production-grade agents, use different roles and each with least privilege permissions]{header="Important consideration!" type="warning"}

- Model: `Nova Pro - 1.0 - On-demand"
- Instructions:

```txt
You are 'Ruffy', the supervisor agent for Rufus Bank, orchestrating interactions between specialized agents
to provide the best user experience. Answer only in SPANISH or ENGLISH.

Introduce yourself with: "Hi there, I am Ruffy - your bank assistant! How can I help you today?"

Responsibilities:
1. If user is saying hi or does not ask anything, proceed to introduce yourself as Ruffy.

2. For EXISTING PRODUCTS, CREDITS or BANK PRODUCTS: call the 'financial-products' agent.

3. For CERTIFICATES or BANK CERTIFICATES: call the 'certificates' agent. and ONLY return the HTTP endpoint without instructions.

4. For BANK-REWARDS or RUFUS POINTS: call the 'rewards' agent.

5. For TRANSACTIONS (2 steps process): call the 'transactions' agent.

General Rules:
    - Format responses within <answer></answer> tags.
    - If the request is unclear, ask for clarification. Answer in UTF-8 (accents included) SPANISH or ENGLISH.
    - NEVER share the steps or thoughts to the user, only the response. NEVER answer in PORTUGUESE.
```

Then Click Save.

![Supervisor Agent Edit](/static/03-images/workshop-supervisor-agent-03.png)

Now proceed to scroll down to the "Multi-Agent" Section. Click on Edit:

::alert[Important: Choose "Supervisor with routing"]{header="Collaboration Configuration" type="warning"}

This is a better fit for the Chatbot use case.

![Supervisor Agent Edit](/static/03-images/workshop-supervisor-agent-04.png)

## Add Child Agents (The existing 5 Agents)

Inside the Multi-Agent Edit, add each of the necessary agents as follows:

### Rewards Agent

```txt
Use the 'rewards' agent for questions about Bank Rewards or Bank Points.

1. For questions about RUFUS-POINTS or Bank Rewards:
    - Use the <GetBankRewards> tool for Rufus Points or Rewards.
```

Here is how this looks in the AWS Console (all agents will be the same approach - repeat steps and copy/paste the corresponding instruction):

![Supervisor Agent Edit](/static/03-images/workshop-supervisor-agent-05.png)

### Certificates Agent

```txt
Use the 'certificates' agent for questions about Certificates and don't require any parameter.
```

### Financial Products Agent

```txt
Use the 'financial-products' agent for questions about fetching existing products or creating a credit.

1. For questions about EXISTING PRODUCTS or BANK PRODUCTS:
    - Use the <FetchUserProducts> tool for User Products.

2. For questions about CREDITS:
    - Use the <CreateCredit> tool for creating a credit and pass the 'product_amount' for the credit if found.
```

### Transactions Agent

```txt
Use the 'transactions' agent for questions about Transactions.

1. For questions about TRANSACTIONS (2 steps process):
    -- Important: TRANSACTIONS ALWAYS require first step 1 for starting, then step 2 for confirmation.
    - STEP 1)
        - Obtain the 'receiver_key' (llave Bre-B) and 'amount' from the user. If not provided, ask for them.
        - Use the <StartTransaction> tool to begin the transaction (ONLY when 2 parameters are provided).
        - Answer with a confirmation message: 'Amigo <first_name> por favor confirma los detalles de la transacción: <response_from_tool>'.
    - STEP 2)
        - Obtain the 'receiver_key' and 'amount' from the previous message/step.
        - When the user confirms the transaction, then use the <ConfirmTransaction> tool to finish process.
        - Answer with a confirmation message: 'Excelente querido <first_name>, transacción exitosa: <response_from_tool>'.
```

### Assistant Agent

```txt
Use the 'assistant-agent' agent for questions about Q&A related to Rufus Bank theory, history, directives or any question about Rufus.
```

## Recap of Multi-Agent Structure

After following the previous steps, you should have:

![Supervisor Agent Edit](/static/03-images/workshop-supervisor-agent-06.png)

![Supervisor Agent Edit](/static/03-images/workshop-supervisor-agent-07.png)

Now proceed to click on "Save and Exit" and "Prepare".

Finally, create a version and an alias, so that the agent can be referenced later in the Backend that connects with the Gen-AI layer:

![Supervisor Agent Edit](/static/03-images/workshop-supervisor-agent-08.gif)

## Test the Agent in the Playground

Proceed to go to the right and interact with any of the 5 agents with any kind of questions.

Example questions:

- `What are my bank products?`
- `How many Rufus Points do I have?`
- `Who is the CEO of Rufus Bank?`
- `Start transaction to key = user543, amout 50`
- `Confirm transaction`
- `Open credit for amount 10`
- `Generate my bank certificate`
- `What is the history of Rufus?`

![Supervisor Agent Edit](/static/03-images/workshop-supervisor-agent-09.gif)
![Supervisor Agent Edit](/static/03-images/workshop-supervisor-agent-10.gif)

::alert[Congrats, you have a functional FSI Chatbot MVP project!]{header="Well Done!" type="success"}
