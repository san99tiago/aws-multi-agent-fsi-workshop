---
title: "Task 2: Create New Agent"
weight: 34
---

# Create the Assistant Agent

The next step is to create from scratch our last Generative AI Bedrock Agent!

The goal is to be able to create an AI Agent that is able to answer questions about Rufus Bank based on some Knowledge Base for the Bank.

![New Assistant Agent](/static/03-images/workshop-new-agent-01.png)

In order to create the Assistant Agent, we will have to execute the following steps:

1. Create an S3 Bucket.
2. Load Rufus Bank PDF files to the S3 Bucket.
3. Create a Bedrock Knowledge Base associated to the S3 Bucket.
4. Create a Bedrock Agent with a detailed "Assistant Instruction for Rufus Bank" with the KB associated to it.
5. Test the Agent with Assistant Question and KB questions.
6. Publish a version for the Assistant Agent.

## Create S3 Bucket

Go to AWS Console and create and S3 Bucket. The name must be Unique:

- Bucket Name: `assets-rag-{RANDOM_LONG_NAME}` (Make sure to have an unique name for the S3 Bucket)

![Create S3 Bucket](/static/03-images/workshop-new-agent-02.gif)

## Upload Rufus Bank PDFs to Bucket

Download these 3 PDF files corresponding to Rufus Bank History, C-Levels and Products:

- [PDF: Rufus Bank History](https://ws-assets-prod-iad-r-iad-ed304a55c2ca1aee.s3.us-east-1.amazonaws.com/86a37a0d-4310-4582-acac-04a0b7eafc83/rufus-bank-history.pdf)
- [PDF: Rufus Bank Directives](https://ws-assets-prod-iad-r-iad-ed304a55c2ca1aee.s3.us-east-1.amazonaws.com/86a37a0d-4310-4582-acac-04a0b7eafc83/rufus-bank-directives.pdf)
- [PDF: Rufus Bank Products](https://ws-assets-prod-iad-r-iad-ed304a55c2ca1aee.s3.us-east-1.amazonaws.com/86a37a0d-4310-4582-acac-04a0b7eafc83/rufus-products.pdf)

After downloading them, proceed to upload them to the S3 Bucket that you just created.

![Upload Files to S3 Bucket](/static/03-images/workshop-new-agent-03.gif)

## Create Bedrock Knowledge Base for Rufus Bank

Go to "Amazon Bedrock" service, and enter "Knowledge Bases":

![Create Bedrock Knowledge Base](/static/03-images/workshop-new-agent-04.png)

- Select the `Knowledge Base with Vector Store`.
- Name: `knowledge-base-rufus-bank`
- IAM Permissions: `Create and use a new service role` (default)

![Add Bedrock KB Details](/static/03-images/workshop-new-agent-05.gif)

- Select the name: `knowledge-base-rufus`
- Select the S3 bucket that has `rag` in the name.
- Choose default settings for chunking strategy.
- Select: `Amazon OpenSearch Serverless` (default)
- Click on `Create Knowledge Base` (finish creation)

![Add Bedrock KB Details](/static/03-images/workshop-new-agent-06.gif)

::alert[Important: this could take a couple of minutes to create!]{header="Important Remark" type="warning"}

This should create the Bedrock Knowledge Base with access to the S3 bucket for the PDF (enabling RAG with Data from the PDFs related to Rufus Bank)!

Now proceed to Sync the files from the S3 Data Source:

![Sync Files S3 Data Source](/static/03-images/workshop-new-agent-07.gif)

At this point, the Knowledge Base (Bedrock KB is ready to play with / interact). Some possible questions are:

- `Who is the CEO of Rufus Bank?`
- `What are Rufus Bank Products?`
- `Who are the C-Levels of Rufus?`
- `What is Rufinator?`

![Test KB](/static/03-images/workshop-new-agent-08.gif)

Now we are ready to define the last agent's instruction!

## Create Bedrock Agent - Assistant

Go to "Amazon Bedrock" service, click on "Agents" and click the "Create Agent":

![Create Bedrock Agent](/static/03-images/workshop-new-agent-09.gif)

Click on "Edit in Agent Builder":

![Edit Bedrock Agent](/static/03-images/workshop-new-agent-10.png)

Proceed to fill the details as follow:

- Name: `assistant-agent` (or any similar name)
- Check: Create and use a new service role
- Model: `Nova Pro - 1.0 - On-demand"
- Instructions:

```txt
You are a specialized agent in Rufus Bank Questions and Answers.
Leverage existing KB to figure out possible questions about Rufus Bank.
If the result is not found in the KB, proceed to answer:
- "This information is outside of my knowledge, please call the official Rufus Galaxy Contact Center"
```

Then Click Save.

![Edit Agent](/static/03-images/workshop-new-agent-11.png)

Proceed to add the KB to the Agent:

- Select the created KB in the previous step.
- Add the instruction: `Leverage existing KB to figure out possible questions about Rufus Bank.`

![Edit Agent](/static/03-images/workshop-new-agent-12.gif)

![Edit Agent](/static/03-images/workshop-new-agent-13.png)

Finally click on the "Prepare Agent" and then proceed to create an Alias "v1":

## Test the Assistant Agent in the Playground

You can now directly interact with the newly created Bedrock Agent and ask these questions:

- `Who is the CEO of Rufus Bank?`
- `What are Rufus Bank Products?`
- `Who are the C-Levels of Rufus?`
- `What is Rufinator?`

![Edit Agent](/static/03-images/workshop-new-agent-14.gif)

![Edit Agent](/static/03-images/workshop-new-agent-15.gif)

![Edit Agent](/static/03-images/workshop-new-agent-16.png)

::alert[Congrats, you should have all 5 child Rufus Bank Agents!]{header="Child Agents Ready!" type="success"}

In the next section we will explore how to create the Supervisor Agent with Multi-Agent Collaboration!
