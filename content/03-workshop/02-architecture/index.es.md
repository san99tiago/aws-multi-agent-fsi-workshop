---
title: "Arquitectura"
weight: 32
---

# Arquitectura Original 🏗️

![Arquitectura Original](/static/03-images/original-architecture-pending-items.png)

Basado en la arquitectura inicial proporcionada por RUFUS Bank, se pudieron detectar las funcionalidades clave y mejorarla hacia un diagrama más robusto y organizado:

> Nota: ¡los componentes en ROJO en el diagrama original son parte de tus tareas en el Workshop!

<br>

![Arquitectura Mejorada](/static/multi-agent-chatbot-fsi-v1.png)

# Arquitectura Mejorada 🏗️

## Componentes del Sistema

### Capa Frontend 🖥️

- **Distribución de Contenido**: Distribución Amazon CloudFront
- **Alojamiento Estático**: Bucket Amazon S3
- **Características**:
  - Interfaz de chat responsiva
  - Actualizaciones de mensajes en tiempo real
  - Gestión segura de sesiones de usuario
  - Carga de documentos PDF desde el navegador

### Servicios Backend 🔧

- **Capa API**: Amazon API Gateway
- **Procesamiento**: Funciones AWS Lambda
- **Almacenamiento de Datos**: Amazon DynamoDB
  - Persistencia del historial de chat
  - Gestión de sesiones de usuario
  - Registros de transacciones
- **Funciones Clave**:
  - Enrutamiento de mensajes en tiempo real
  - Gestión del estado de conversación
  - Manejo de documentos

### Motor de IA Generativa 🤖

- **Agente Supervisor**:

  - Construido sobre Amazon Bedrock (Amazon Nova Pro)
  - Orquesta todos los agentes secundarios
  - Mantiene el contexto de la conversación
  - Enruta solicitudes según la intención

- **Agentes Especializados**:

  1. Agente de Información de Productos
  2. Agente de Gestión de Transacciones
  3. Agente de Generación de Certificados
  4. Agente de Servicios de Crédito
  5. Agente de Atención al Cliente (habilitado con RAG)

- **Sistemas de Soporte**:
  - Base de Conocimientos para Q&A
  - RAG para procesamiento de documentos
  - Instrucción LLM personalizada para asistente

### Controles de Seguridad 🛡️

- **Barreras de Protección de Bedrock**:
  - Filtrado de contenido
  - Restricciones de temas
  - Protección de datos personales
  - Cumplimiento normativo

## Flujo de Datos

1. La solicitud del usuario ingresa a través de CloudFront
2. API Gateway enruta a Lambda apropiado
3. Lambda inicia el procesamiento Gen-AI
4. El Agente Supervisor analiza la solicitud
5. Tarea enrutada al agente especializado
6. Respuesta filtrada a través de barreras de protección
7. Resultado almacenado en DynamoDB
8. Respuesta devuelta al usuario

---

::alert[Esta arquitectura representa la versión mejorada del diseño original de RUFUS Bank.]{header="Nota" type="info"}
