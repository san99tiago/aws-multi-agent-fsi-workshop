---
title: "Tarea 1: Validar Agentes Existentes"
weight: 33
---

# Acceso a Agentes de Bedrock

El primer paso es ir al Servicio Bedrock y verificar los Agentes existentes.

![Workshop Agents Access](/static/03-images/workshop-agents-01.gif)

En este momento, deberías tener 4 Agentes de Bedrock ya creados por los Ingenieros anteriores de Rufus Bank.

## Agentes Existentes para Rufus Bank

En la siguiente tabla puedes profundizar en los Agentes de Bedrock existentes ya creados para las funcionalidades deseadas del Chatbot de Rufus Bank:

| Select Agent                                 | Name               | Status   | Description                                                                                                                                                   |
| -------------------------------------------- | ------------------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| fsi-multi-agents-agent-v1-bank-rewards       | Bank Rewards       | Prepared | Agente especializado en recompensas bancarias. Puede obtener recompensas de usuario con `<GetBankRewards>`.                                                   |
| fsi-multi-agents-agent-v1-transactions       | Transactions       | Prepared | Agente especializado en recompensas bancarias. Puede iniciar transacciones con `<GetTransactions>` y confirmarlas con `<ConfirmTransaction>`.                 |
| fsi-multi-agents-agent-v1-certificates       | Certificates       | Prepared | Agente especializado en certificados. Puede generar certificados PDF con `<GenerateCertificates>`.                                                            |
| fsi-multi-agents-agent-v1-financial-products | Financial Products | Prepared | Agente especializado en productos financieros. Puede ejecutar operaciones CRUD hacia los productos del usuario como `<FetchUserProducts>` o `<CreateCredit>`. |

<br>

![Agent Understanding](/static/03-images/workshop-agents-00.png)

<br>

---

## Prueba del Agente Bedrock 1 - Recompensas Bancarias

Procede a acceder al Agente Bedrock para Recompensas Bancarias. Aquí puedes explorar y validar las configuraciones del Agente 1 para el sistema de "Recompensas Bancarias".

![Agent Bank Rewards](/static/03-images/workshop-agents-02.png)

Capacidades del Agente:

- Este agente puede conectarse al Backend de Recompensas del Banco y obtener los Puntos de Recompensa bancarios para el usuario conectado.

Para probar el agente, ve al Playground de Bedrock y hazle preguntas similares a:

- `¿Cuántos Puntos Rufus tengo?`
- `¿Cuáles son mis puntos?`

Ejemplo de prueba:

![Agent Bank Rewards](/static/03-images/workshop-agents-03.gif)

---

## Prueba del Agente Bedrock 2 - Productos Financieros

Procede a acceder al Agente Bedrock para Productos Financieros. Aquí puedes explorar y validar las configuraciones del Agente 2 para el sistema de "Productos Financieros".

![Agent Financial Products](/static/03-images/workshop-agents-04.png)

Capacidades del Agente:

- Obtener y ver los productos bancarios existentes.
- Obtener el monto actual almacenado en la cuenta bancaria.
- Crear un Crédito Bancario.

Para probar el agente, ve al Playground de Bedrock y hazle preguntas similares a:

- `Ruffy, ¿cuáles son mis productos bancarios?`
- `¿Puedo ver mis productos bancarios?`
- `¿Cuánto dinero tengo en mi banco?`
- `¿Puedo abrir un crédito por 10.000?`

Ejemplo de prueba:

![Agent Financial Products](/static/03-images/workshop-agents-05.gif)

## Prueba del Agente Bedrock 3 - Certificados Bancarios

Procede a acceder al Agente Bedrock para Certificados Bancarios. Aquí puedes explorar y validar las configuraciones del Agente 3 para el sistema de "Certificados Bancarios".

![Agent Bank Certificates](/static/03-images/workshop-agents-06.png)

Capacidades del Agente:

- Obtener un Certificado PDF para los Productos Bancarios.
- Nota: El agente devuelve una URL Pre-firmada de S3 en la versión actual.

Para probar el agente, ve al Playground de Bedrock y hazle preguntas similares a:

- `Generar certificado bancario`
- `Obtener certificado`

Ejemplo de prueba:

![Agent Bank Certificates](/static/03-images/workshop-agents-07.gif)

## Prueba del Agente Bedrock 4 - Transacciones

Procede a acceder al Agente Bedrock para Transacciones. Aquí puedes explorar y validar las configuraciones del Agente 4 para el sistema de "Transacciones".

![Agent Transactions](/static/03-images/workshop-agents-08.png)

Capacidades del Agente:

- Paso 1: Iniciar una transacción con los inputs: `key` y `amount`.
- Paso 2: Confirmar una transacción basada en el Paso 1.
- Generar un recibo de imagen de la transacción exitosa.

Para probar el agente, ve al Playground de Bedrock y hazle preguntas similares a:

- Paso 1: `Quiero transferir 10 a la clave ********`
- Paso 2: `Confirmar transacción`

Ejemplo de prueba:

![Agent Transactions](/static/03-images/workshop-agents-09.png)
![Agent Transactions](/static/03-images/workshop-agents-10.png)

## ¡Pruebas Completadas!

::alert[¡Felicitaciones, has probado exitosamente los 4 Agentes de IA Generativa existentes para Rufus Bank!]{header="¡Pruebas Completadas, Prepárate para Crear un Agente!" type="success"}
