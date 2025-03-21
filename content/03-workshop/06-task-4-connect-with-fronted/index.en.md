---
title: "Task 4: Connect with Frontend"
weight: 36
---

# Let's Bring the Chatbot to a Real Frontend!

First, go to "Cloudfront", and go to the distribution:

![CloudFront](/static/03-images/workshop-frontend-01.png)

Copy the URL and open it in another tab in your browser. You should be able to see the Chatbot FSI Interface:

![Frontend](/static/03-images/workshop-frontend-02.png)

As you can see, the Chatbot is only missing one main step. Configure the Backend to leverage the Agent ID and Agent Version, so that the request can be correctly routed:

![Frontend](/static/03-images/workshop-frontend-03.png)

## Configure the Agent ID and Agent Alias for Backend

First, let's get the Agent ID and Agent Alias ID from the Supervisor Bedrock Agent.

Go to Bedrock Agents, click on the Supervisor, and get these values:

![Frontend](/static/03-images/workshop-frontend-04.png)

Important to COPY these values:

- `Agent ID`
- `Agent Alias ID`

The current solution leverages Systems Manager Parameters to share the Agent ID configuration. In order to correctly configure it, proceed to go to "Systems Manager", and click on "Parameters":

![Frontend](/static/03-images/workshop-frontend-05.png)

We now need to update the parameters as follows:

- Replace the `/prod/RufusBank/bedrock-agent-alias-id` with `Agent Alias ID` value
- Replace the `/prod/RufusBank/bedrock-agent-id` with `Agent ID` value

![Frontend](/static/03-images/workshop-frontend-06.png)
![Frontend](/static/03-images/workshop-frontend-07.png)

Now we should be ready to test Ruffy Again!!

## Testing Ruffy now in the integrated Fronted

Go back to the CloudFront URL, and start chatting with Ruffy, your FSI Next-Generation Chatbot for agentic workflows!

![Frontend](/static/03-images/workshop-frontend-08.gif)
![Frontend](/static/03-images/workshop-frontend-09.png)
