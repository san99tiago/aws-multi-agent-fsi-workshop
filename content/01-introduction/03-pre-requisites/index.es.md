---
title: "Pre-Requisitos"
weight: 31
---

## Acceso a Modelos de Bedrock 🎇

Amazon Bedrock es un servicio completamente administrado que ofrece una selección de modelos base (FMs) de alto rendimiento de empresas líderes en IA, incluyendo Amazon, Anthropic, AI21 Labs, Stability AI, Cohere y muchos más, junto con un amplio conjunto de capacidades para construir aplicaciones de IA generativa, simplificando el desarrollo mientras mantiene la privacidad y seguridad.

## Comenzar con Amazon Bedrock

Puedes acceder a los FMs disponibles en Amazon Bedrock a través de la Consola de Administración de AWS, los SDK de AWS y frameworks de código abierto como LangChain, LangGraph, CrewAI, Llama-Index y muchos más.

## Habilitar acceso a modelos en Bedrock

Necesitamos habilitar el acceso a los modelos para este workshop:

::alert[NOTA: Para este workshop, solo podrás trabajar con los modelos mencionados. Por favor no te suscribas a otros modelos ya que podrían no funcionar como se espera en esta cuenta de AWS. Para cuentas regulares de AWS, no existe tal restricción.]{header="Importante" type="warning"}

1. Navega a la consola de Amazon Bedrock buscando Bedrock en la barra de búsqueda de la Consola AWS y haciendo clic en Amazon Bedrock.

![Pre-Requisitos 01](/static/01-images/pre-requisites-01.png)

![Pre-Requisitos 02](/static/01-images/pre-requisites-02.png)

2. Haz clic en Vista General para revisar todos los modelos disponibles en Bedrock:

![Pre-Requisitos 03](/static/01-images/pre-requisites-03.png)

3. Desde el panel izquierdo, haz clic en la página de Acceso a modelos. En la página de acceso a modelos, haz clic en Habilitar modelos específicos en la parte superior izquierda:

![Pre-Requisitos 04](/static/01-images/pre-requisites-04.png)

Luego, habilita solo los siguientes modelos:

- `Nova Pro`

![Pre-Requisitos 05](/static/01-images/pre-requisites-05.png)

Espera unos segundos en la página hasta que el Estado de Acceso para estos modelos cambie a Acceso Concedido. Es posible que necesites actualizar la página para ver todos los cambios.

::alert[¡Felicitaciones! Has habilitado exitosamente los Modelos de Amazon Bedrock. Ahora puedes avanzar y comenzar los laboratorios.]{header="Felicitaciones" type="success"}
