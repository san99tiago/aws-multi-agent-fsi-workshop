---
title: "Pre-Requisites"
weight: 31
---

## Bedrock Model Access 🎇

Amazon Bedrock is a fully managed service that offers a choice of high-performing foundation models (FMs) from leading AI companies, including Amazon, Anthropic, AI21 Labs, Stability AI, Cohere and much more, along with a broad set of capabilities to build generative AI applications, simplifying the development while maintaining privacy and security.

## Get Started with Amazon Bedrock

You can access available FMs in Amazon Bedrock through the AWS Management Console, AWS SDKs, and open-source frameworks such as LangChain, LangGraph, CrewAI, Llama-Index and many more.

## Enable models access in Bedrock

We need to enable access to models for this workshop:

::alert[NOTE: For this workshop, you will only be able to work with the models mentioned in this workshop. Please do not subscribe to other models as they might not work as expected in this AWS account. For regular AWS accounts, there is no such restriction.]{header="Important" type="warning"}

1. Navigate to Amazon Bedrock console by searching for Bedrock in the search bar on AWS Console and clicking on Amazon Bedrock.

![Pre-Requisites 01](/static/01-images/pre-requisites-01.png)

![Pre-Requisites 02](/static/01-images/pre-requisites-02.png)

2. Click on Overview to review all the models available in Bedrock:

![Pre-Requisites 03](/static/01-images/pre-requisites-03.png)

3. From the left pane, click on Model access page. On the model access page, click on Enable specific models at top left:

![Pre-Requisites 04](/static/01-images/pre-requisites-04.png)

Then, enable only the following models:

- `Nova Pro`
- `Titan Text Embeddings V2`

![Pre-Requisites 05](/static/01-images/pre-requisites-05.gif)

Wait for few seconds in the page until Access Status for these models are changed to Access Granted. You might need to refresh the page to see all the changes.

::alert[Congratulations! You have successfully enabled Amazon Bedrock Models. Now you can move forward and start the labs.]{header="Congratulations" type="success"}
