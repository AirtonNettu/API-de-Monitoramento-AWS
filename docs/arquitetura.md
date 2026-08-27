# Arquitetura — API de Monitoramento AWS

## 1. Visão geral

A API de Monitoramento AWS é um projeto educacional desenvolvido em Python com FastAPI.

O projeto tem como objetivos:

- aprender Python por meio de uma aplicação real;
- compreender o funcionamento de uma API REST;
- aplicar funções, condicionais, tipagem e validação;
- consultar métricas de recursos da AWS;
- integrar Python com AWS utilizando Boto3;
- preparar a aplicação para execução futura com AWS Lambda e API Gateway.

A primeira versão funciona localmente e utiliza valores informados pelo usuário. Em versões posteriores, as métricas serão consultadas diretamente no Amazon CloudWatch.

---

## 2. Problema

Administradores precisam consultar métricas de servidores e interpretar se a utilização dos recursos está normal, em alerta ou em estado crítico.

A API receberá métricas, aplicará regras de classificação e retornará respostas em JSON.

Exemplo:

Entrada:

```text
GET /cpu/75