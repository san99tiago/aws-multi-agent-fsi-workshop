---
title: "Tarea 2: Crear Nuevo Agente"
weight: 34
---

# Crear el Agente Asistente

El siguiente paso es crear desde cero nuestro último Agente de IA Generativa con Bedrock!

El objetivo es poder crear un Agente de IA que sea capaz de responder preguntas sobre Rufus Bank basándose en una Base de Conocimientos del Banco.

![Nuevo Agente Asistente](/static/03-images/workshop-new-agent-01.png)

Para crear el Agente Asistente, necesitaremos ejecutar los siguientes pasos:

1. Crear un Bucket S3.
2. Cargar archivos PDF de Rufus Bank al Bucket S3.
3. Crear una Base de Conocimientos de Bedrock asociada al Bucket S3.
4. Crear un Agente Bedrock con "Instrucciones detalladas para el Asistente de Rufus Bank" con la KB asociada.
5. Probar el Agente con preguntas al Asistente y preguntas a la KB.
6. Publicar una versión del Agente Asistente.

## Crear Bucket S3

Ve a la Consola AWS y crea un Bucket S3. El nombre debe ser único:

- Nombre del Bucket: `assets-rag-{NOMBRE_LARGO_ALEATORIO}` (Asegúrate de tener un nombre único para el Bucket S3)

![Crear Bucket S3](/static/03-images/workshop-new-agent-02.gif)

## Subir PDFs de Rufus Bank al Bucket

Descarga estos 3 archivos PDF correspondientes a la Historia, Directivos y Productos de Rufus Bank:

- [PDF: Historia de Rufus Bank](https://ws-assets-prod-iad-r-iad-ed304a55c2ca1aee.s3.us-east-1.amazonaws.com/86a37a0d-4310-4582-acac-04a0b7eafc83/rufus-bank-history.pdf)
- [PDF: Directivos de Rufus Bank](https://ws-assets-prod-iad-r-iad-ed304a55c2ca1aee.s3.us-east-1.amazonaws.com/86a37a0d-4310-4582-acac-04a0b7eafc83/rufus-bank-directives.pdf)
- [PDF: Productos de Rufus Bank](https://ws-assets-prod-iad-r-iad-ed304a55c2ca1aee.s3.us-east-1.amazonaws.com/86a37a0d-4310-4582-acac-04a0b7eafc83/rufus-products.pdf)

Después de descargarlos, procede a subirlos al Bucket S3 que acabas de crear.

![Subir Archivos al Bucket S3](/static/03-images/workshop-new-agent-03.gif)

## Crear Base de Conocimientos Bedrock para Rufus Bank

Ve al servicio "Amazon Bedrock" y entra en "Knowledge Bases":

![Crear Base de Conocimientos Bedrock](/static/03-images/workshop-new-agent-04.png)

- Selecciona `Knowledge Base with Vector Store`.
- Nombre: `knowledge-base-rufus-bank`
- Permisos IAM: `Create and use a new service role` (por defecto)

![Agregar Detalles de KB Bedrock](/static/03-images/workshop-new-agent-05.gif)

- Selecciona el nombre: `knowledge-base-rufus`
- Selecciona el bucket S3 que tiene `rag` en el nombre.
- Elige la configuración predeterminada para la estrategia de fragmentación.
- Selecciona: `Amazon OpenSearch Serverless` (por defecto)
- Haz clic en `Create Knowledge Base` (finalizar creación)

![Agregar Detalles de KB Bedrock](/static/03-images/workshop-new-agent-06.gif)

::alert[Importante: ¡esto podría tomar un par de minutos en crearse!]{header="Observación Importante" type="warning"}

¡Esto debería crear la Base de Conocimientos Bedrock con acceso al bucket S3 para el PDF (habilitando RAG con datos de los PDFs relacionados con Rufus Bank)!

Ahora procede a sincronizar los archivos desde la fuente de datos S3:

![Sincronizar Archivos Fuente de Datos S3](/static/03-images/workshop-new-agent-07.gif)

En este punto, la Base de Conocimientos (Bedrock KB está lista para usar / interactuar). Algunas preguntas posibles son:

- `¿Quién es el CEO de Rufus Bank?`
- `¿Cuáles son los productos de Rufus Bank?`
- `¿Quiénes son los directivos de Rufus?`
- `¿Qué es Rufinator?`

![Probar KB](/static/03-images/workshop-new-agent-08.gif)

¡Ahora estamos listos para definir las instrucciones del último agente!

## Crear Agente Bedrock - Asistente

Ve al servicio "Amazon Bedrock", haz clic en "Agents" y haz clic en "Create Agent":

![Crear Agente Bedrock](/static/03-images/workshop-new-agent-09.gif)

Haz clic en "Edit in Agent Builder":

![Editar Agente Bedrock](/static/03-images/workshop-new-agent-10.png)

Procede a llenar los detalles de la siguiente manera:

- Nombre: `assistant-agent` (o cualquier nombre similar)
- Marcar: Create and use a new service role
- Modelo: `Nova Pro - 1.0 - On-demand"
- Instrucciones:

```txt
You are a specialized agent in Rufus Bank Questions and Answers.
Leverage existing KB to figure out possible questions about Rufus Bank.
If the result is not found in the KB, proceed to answer:
- "This information is outside of my knowledge, please call the official Rufus Galaxy Contact Center"
```

Luego haz clic en Guardar.

![Editar Agente](/static/03-images/workshop-new-agent-11.png)

Procede a agregar la KB al Agente:

- Selecciona la KB creada en el paso anterior.
- Agrega la instrucción: `Aprovechar la KB existente para resolver posibles preguntas sobre Rufus Bank.`

![Editar Agente](/static/03-images/workshop-new-agent-12.gif)

![Editar Agente](/static/03-images/workshop-new-agent-13.png)

Finalmente haz clic en "Preparar Agente" y luego procede a crear un Alias "v1":

## Probar el Agente Asistente en el Playground

Ahora puedes interactuar directamente con el Agente Bedrock recién creado y hacer estas preguntas:

- `¿Quién es el CEO de Rufus Bank?`
- `¿Cuáles son los productos de Rufus Bank?`
- `¿Quiénes son los directivos de Rufus?`
- `¿Qué es Rufinator?`

![Editar Agente](/static/03-images/workshop-new-agent-14.gif)

![Editar Agente](/static/03-images/workshop-new-agent-15.gif)

![Editar Agente](/static/03-images/workshop-new-agent-16.png)

::alert[¡Felicitaciones, deberías tener los 5 agentes secundarios de Rufus Bank!]{header="¡Agentes Secundarios Listos!" type="success"}

¡En la siguiente sección exploraremos cómo crear el Agente Supervisor con Colaboración Multi-Agente!
