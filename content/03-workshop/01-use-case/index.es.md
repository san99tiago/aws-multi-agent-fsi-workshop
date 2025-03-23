---
title: "Caso de Uso"
weight: 31
---

# Caso de Uso de RUFUS Bank con IA Generativa 🏦

## Antecedentes y Desafíos

![Logo de Rufus Bank](/static/03-images/rufus-bank-logo.png)

RUFUS Bank, una institución financiera tradicional con fuerte presencia en el mercado, está embarcándose en un viaje de transformación digital aprovechando las tecnologías de IA Generativa. Su objetivo principal es modernizar las interacciones con los clientes mientras mantiene los más altos estándares de seguridad.

### Situación Actual

- Canales bancarios tradicionales alcanzando limitaciones
- Necesidad de servicio al cliente inteligente 24/7
- Presión competitiva de bancos digitales
- Creciente demanda de servicio instantáneo por parte de los clientes

### Visión Estratégica

Implementar un sistema de chatbot multi-agente seguro e inteligente usando Amazon Bedrock que pueda:

- Atender a clientes a través de múltiples canales
- Comenzar con integración en portal web
- Mantener estrictos estándares de seguridad
- Escalar con necesidades bancarias futuras

## 🎯 Alcance del Proyecto

![Arquitectura Propuesta del Chatbot de Rufus Bank](/static/03-images/original-architecture-pending-items.png)

IMPORTANTE: ¡Los servicios/componentes en ROJO se desarrollarán desde cero en este taller! Los otros son parte del trabajo que los Ingenieros de Rufus Bank ya han finalizado.

### Fase 1: Chatbot Inteligente para Portal Web

Implementación de un sistema chatbot multi-agente con cinco funcionalidades especializadas:

1. **Agente de Información de Productos**

   - Acceso en tiempo real al catálogo de productos
   - Información real sobre Cuentas de Ahorro y Corrientes

2. **Agente de Transacciones**

   - Transferencias seguras de fondos
   - Procesamiento de pagos
   - Recibos y validaciones de transacciones

3. **Agente de Gestión de Certificados**

   - Generación de documentos oficiales
   - Entrega de certificados digitales
   - Servicios de verificación con cumplimiento QR gubernamental

4. **Agente de Servicios de Crédito**

   - Gestión de líneas de crédito
   - Procesamiento de solicitudes
   - Consultas de estado de crédito

5. **Agente de Atención al Cliente**
   - Gestión de consultas generales
   - Procesamiento de documentos PDF
   - Respuestas contextuales basadas en RAG

## 🛡️ Requisitos de Seguridad

### Controles de Contenido Prohibido

- No revelar información personal
- Evitar estrictamente:
  - Discusiones políticas
  - Comparaciones con competidores
  - Temas relacionados a sexualidad
  - Manejo de clientes enojados
  - Información no verificada

## 🏗️ Progreso Actual

### Completado

- 4 de 5 agentes AI especializados desarrollados y probados
- Implementación del UI Frontend conectado al Backend

## 🎮 Plan de Acción del Líder de Desarrollo

### 1. Validación de los 4 Agentes Existentes

- Revisar funcionalidades existentes
- Realizar pruebas exhaustivas
- Profundizar en sus características

### 2. Creación del Agente AI Final con RAG

- Desarrollar Agente de Atención al Cliente
- Implementar pipeline de procesamiento PDF
- Crear arquitectura RAG eficiente
- Probar precisión de recuperación de conocimiento
- Probar funcionalidad del Agente

### 3. Orquestación Multi-Agente

- Diseñar arquitectura del agente supervisor
- Implementar lógica de enrutamiento
- Crear protocolos de comunicación entre agentes
- Probar flujos end-to-end para cada uno de los 5 agentes

### 4. Implementación de Seguridad

- Desplegar Guardrails de Bedrock
- Implementar filtrado de contenido
- Probar límites de seguridad para temas denegados
- Probar escenarios de ataques de inyección de prompts

### 5. Hoja de Ruta de Mejoras

#### Mejoras Propuestas

- Explorar cómo esta solución puede mejorarse con diferentes enfoques

## ⚠️ Descargo de Responsabilidad -- Este es un proyecto de Banco DEMO

---

::alert[Este documento sirve como referencia principal para el Taller de RUFUS Bank sobre IA Generativa para solución Multi-Agentes para FSI.]{header="Solo para Propósitos DEMO" type="warning"}
