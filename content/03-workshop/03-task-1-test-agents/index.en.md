---
title: "Task 1: Test Existing Agents"
weight: 33
---

# Access Bedrock Agents

The first step is to go to the Bedrock Service, and check the existing Agents.

![Workshop Agents Access](/static/03-images/workshop-agents-01.gif)

As of now, you should have 4 existing Bedrock Agents already created by the previous Rufus Bank Engineers.

## Existing Agents for Rufus Bank

In the following table you can dive deep into the existing Bedrock Agents already created for Rufus Bank functionalities desired for the Chatbot:

| Select Agent                                 | Name               | Status   | Description                                                                                                                                          |
| -------------------------------------------- | ------------------ | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| fsi-multi-agents-agent-v1-bank-rewards       | Bank Rewards       | Prepared | Agent specialized in bank rewards. Is able to get user rewards with `<GetBankRewards>`.                                                              |
| fsi-multi-agents-agent-v1-transactions       | Transactions       | Prepared | Agent specialized in bank rewards. Is able to start transactions with `<GetTransactions>` and confirm them with `<ConfirmTransaction>`.              |
| fsi-multi-agents-agent-v1-certificates       | Certificates       | Prepared | Agent specialized in certificates. Is able to generate PDF certificates with `<GenerateCertificates>`.                                               |
| fsi-multi-agents-agent-v1-financial-products | Financial Products | Prepared | Agent specialized in financial products. Is able to run CRUD operations towards the user products such as `<FetchUserProducts>` or `<CreateCredit>`. |

<br>

![Agent Understanding](/static/03-images/workshop-agents-00.png)

<br>

---

## Testing Bedrock Agent 1 - Bank Rewards

Proceed to access the Bedrock Agent for Bank Rewards. Here you can explore and validate the Agent 1 configurations for the "Bank Rewards" system.

![Agent Bank Rewards](/static/03-images/workshop-agents-02.png)

Agent Capabilities:

- This agent is able to connect to the Bank's Rewards Backend and fetch their Bank Reward Points for the connected user.

In order to test the agent, go to the Bedrock Playground and ask it questions similar to:

- `How many Rufus Points do I have?`
- `What are my points?`

Example for testing:

![Agent Bank Rewards](/static/03-images/workshop-agents-03.gif)

---

## Testing Bedrock Agent 2 - Financial Products

Proceed to access the Bedrock Agent for Financial Products. Here you can explore and validate the Agent 2 configurations for the "Financial Products" system.

![Agent Financial Products](/static/03-images/workshop-agents-04.png)

Agent Capabilities:

- Fetch and see the existing bank products.
- Get the current amount stored in the bank account.
- Create a Bank Credit.

In order to test the agent, go to the Bedrock Playground and ask it questions similar to:

- `Ruffy, what are my bank products?`
- `Can I see my bank products?`
- `How much money do I have in my bank savings?`
- `Can I open a credit for 10.000?`

Example for testing:

![Agent Financial Products](/static/03-images/workshop-agents-05.gif)

## Testing Bedrock Agent 3 - Bank Certificates

Proceed to access the Bedrock Agent for Bank Certificates. Here you can explore and validate the Agent 2 configurations for the "Bank Certificates" system.

![Agent Bank Certificates](/static/03-images/workshop-agents-06.png)

Agent Capabilities:

- Get a PDF Certificate for the Bank Products.
- Note: Agent returns an S3 Pre-Signed URL in the current version.

In order to test the agent, go to the Bedrock Playground and ask it questions similar to:

- `Generate bank certificate`
- `Get certificate`

Example for testing:

![Agent Bank Certificates](/static/03-images/workshop-agents-07.gif)

## Testing Bedrock Agent 4 - Transactions

Proceed to access the Bedrock Agent for Transactions. Here you can explore and validate the Agent 2 configurations for the "Transactions" system.

![Agent Transactions](/static/03-images/workshop-agents-08.png)

Agent Capabilities:

- Step 1: Initiate a transaction with the inputs: `key` and `amount`.
- Step 2: Confirm a transaction based on Step 1.
- Generates and ID that the frontend will later render as an image receipt.

In order to test the agent, go to the Bedrock Playground and ask it questions similar to:

- Step 1: `I want to transfer 10 to the key user123`
- Setp 2: `Confirm`

Example for testing:

![Agent Transactions](/static/03-images/workshop-agents-09.png)

## Testing Complete!

::alert[Congrats, you have successfully tested the existing 4 Generative-AI Agents for Rufus Bank]{header="Testing Complete, Get Ready to Create an Agent!" type="success"}
