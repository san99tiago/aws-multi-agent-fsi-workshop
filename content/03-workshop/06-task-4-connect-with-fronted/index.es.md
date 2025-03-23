---
title: "Tarea 4: Conectar con el Frontend"
weight: 36
---

# ¡Llevemos el Chatbot a un Frontend Real!

Primero, ve a "CloudFront" y accede a la distribución:

![CloudFront](/static/03-images/workshop-frontend-01.png)

Copia la URL y ábrela en otra pestaña de tu navegador. Deberías poder ver la Interfaz del Chatbot FSI:

![Frontend](/static/03-images/workshop-frontend-02.png)

Como puedes ver, al Chatbot solo le falta un paso principal. Configurar el Backend para aprovechar el ID del Agente y la Versión del Agente, para que la solicitud pueda ser correctamente enrutada:

![Frontend](/static/03-images/workshop-frontend-03.png)

## Configurar el ID del Agente y el Alias del Agente para el Backend

Primero, obtengamos el ID del Agente y el ID del Alias del Agente desde el Agente Supervisor de Bedrock.

Ve a Bedrock Agents, haz clic en el Supervisor y obtén estos valores:

![Frontend](/static/03-images/workshop-frontend-04.png)

Importante COPIAR estos valores:

- `Agent ID`
- `Agent Alias ID`

La solución actual utiliza Parámetros de Systems Manager para compartir la configuración del ID del Agente. Para configurarlo correctamente, procede a ir a "Systems Manager" y haz clic en "Parameters":

![Frontend](/static/03-images/workshop-frontend-05.png)

Ahora necesitamos actualizar los parámetros de la siguiente manera:

- Reemplaza el `/prod/RufusBank/bedrock-agent-alias-id` con el valor del `Agent Alias ID`
- Reemplaza el `/prod/RufusBank/bedrock-agent-id` con el valor del `Agent ID`

![Frontend](/static/03-images/workshop-frontend-06.png)
![Frontend](/static/03-images/workshop-frontend-07.png)

¡Ahora deberíamos estar listos para probar a Ruffy nuevamente!

## Probando a Ruffy ahora en el Frontend integrado

Vuelve a la URL de CloudFront y comienza a chatear con Ruffy, ¡tu Chatbot FSI de próxima generación para flujos de trabajo basados en agentes!

![Frontend](/static/03-images/workshop-frontend-08.gif)
![Frontend](/static/03-images/workshop-frontend-09.png)
