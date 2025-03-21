---
title: "Tarea 3: Crear Agente Supervisor"
weight: 35
---

# Detalles del Agente Supervisor

En esta sección, exploraremos cómo crear el Agente Supervisor, para poder habilitar la Colaboración Multi-Agente para el Chatbot FSI:

![Arquitectura del Agente Supervisor](/static/03-images/workshop-supervisor-agent-01.png)

## Crear Agente Bedrock

El primer paso es ir al Servicio Bedrock y hacer clic en "Create Agent". Luego procede a llenar los datos de la siguiente manera:

- Nombre: `supervisor-agent`
- Marcar: `Enable Multi-Agent Collaboration`

![Editar Agente Supervisor](/static/03-images/workshop-supervisor-agent-02.png)

Ahora procede a editar/configurar el agente de la siguiente manera:

- Marcar: Create and use a new service role
- Modelo: `Nova Pro - 1.0 - On-demand"
- Instrucciones:

```txt
You are 'Ruffy', the supervisor agent for Rufus Bank, orchestrating interactions between specialized agents
to provide the best user experience. Answer only in SPANISH or ENGLISH.

Introduce yourself with: "Hi there, I am Ruffy - your bank assistant! How can I help you today?"

Responsibilities:
1. If user is saying hi or does not ask anything, proceed to introduce yourself as Ruffy.

2. For EXISTING PRODUCTS, CREDITS or BANK PRODUCTS: call the 'financial-products' agent.

3. For CERTIFICATES or BANK CERTIFICATES: call the 'certificates' agent. and ONLY return the HTTP endpoint without instructions.

4. For BANK-REWARDS or RUFUS POINTS: call the 'rewards' agent.

5. For TRANSACTIONS (2 steps process): call the 'transactions' agent. For Step 2 ONLY return the HTTP endpoint without instructions.

General Rules:
    - Format responses within <answer></answer> tags.
    - If the request is unclear, ask for clarification. Answer in UTF-8 (accents included) SPANISH or ENGLISH.
    - NEVER share the steps or thoughts to the user, only the response. NEVER answer in PORTUGUESE.
```

::alert[Importante: elegir "Supervisor with routing"]{header="Collaboration Configuration" type="warning"}

Esto ayudará en el procesamiento para el caso del chatbot!

Luego haz clic en Guardar.

![Editar Agente Supervisor](/static/03-images/workshop-supervisor-agent-03.png)

Ahora procede a desplazarte hacia abajo hasta la sección "Multi-Agent". Haz clic en Editar:

![Editar Agente Supervisor](/static/03-images/workshop-supervisor-agent-04.png)

## Agregar Agentes Secundarios (Los 5 Agentes existentes)

Dentro de la Edición Multi-Agente, agrega cada uno de los agentes necesarios de la siguiente manera:

### Agente de Recompensas

```txt
Use the 'rewards' agent for questions about Bank Rewards or Bank Points.

1. For questions about RUFUS-POINTS or Bank Rewards:
    - Use the <GetBankRewards> tool for Rufus Points or Rewards.
```

Así es como se ve en la Consola AWS (todos los agentes seguirán el mismo enfoque - repite los pasos y copia/pega la instrucción correspondiente):

![Editar Agente Supervisor](/static/03-images/workshop-supervisor-agent-05.png)

### Agente de Certificados

```txt
Use the 'certificates' agent for questions about Certificates and don't require any parameter.
```

### Agente de Productos Financieros

```txt
Use the 'financial-products' agent for questions about fetching existing products or creating a credit.

1. For questions about EXISTING PRODUCTS or BANK PRODUCTS:
    - Use the <FetchUserProducts> tool for User Products.

2. For questions about CREDITS:
    - Use the <CreateCredit> tool for creating a credit and pass the 'product_amount' for the credit if found.
```

### Agente de Transacciones

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

### Agente Asistente

```txt
Use the 'assistant' agent for questions about Q&A related to Rufus Bank theory, history, directives or any question about Rufus.
```

## Resumen de la Estructura Multi-Agente

Después de seguir los pasos anteriores, deberías tener:

![Editar Agente Supervisor](/static/03-images/workshop-supervisor-agent-06.png)

![Editar Agente Supervisor](/static/03-images/workshop-supervisor-agent-07.png)

Ahora procede a hacer clic en "Save and Exit" y "Prepare".

Finalmente, crea una versión y un alias, para que el agente pueda ser referenciado más tarde en el Backend que se conecta con la capa Gen-AI:

![Editar Agente Supervisor](/static/03-images/workshop-supervisor-agent-08.gif)

## Probar el Agente en el Playground

Procede a ir a la derecha e interactuar con cualquiera de los 5 agentes con cualquier tipo de preguntas.

Ejemplos de preguntas:

- `¿Cuáles son mis productos bancarios?`
- `¿Cuántos Puntos Rufus tengo?`
- `¿Quién es el CEO de Rufus Bank?`
- `Iniciar transacción a llave = user543, monto 50`
- `Confirmar transacción`
- `Abrir crédito por monto 10`
- `Generar mi certificado bancario`
- `¿Cuál es la historia de Rufus?`

![Editar Agente Supervisor](/static/03-images/workshop-supervisor-agent-09.gif)
![Editar Agente Supervisor](/static/03-images/workshop-supervisor-agent-10.gif)
