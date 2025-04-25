# python-test

## Rodando localmente

1. Criar o arquivo `.env` a partir do `.env.example`.
   - Basta renomear o `.env.example` para `.env`.
   - O conteúdo já está configurado corretamente para o ambiente de testes.

2. Subir os containers com Docker Compose:

```bash
docker compose up --build
```

> Obs: Execute o comando a partir da raiz do projeto (`python-test/`). Caso não tenha o Docker e o Docker Compose instalados, será necessário instalá-los primeiro.

3. Acessar a API:

- A aplicação estará disponível em: [http://localhost:8000](http://localhost:8000)

</br>

## Documentação da API

A documentação Swagger é gerada automaticamente utilizando FastAPI.

Após subir os containers, acesse:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Endpoints principais

### `POST /v1/scraping/`

Inicia uma task de scraping.

**Exemplo de requisição:**

```json
{
  "cnpj": "12345678000195"
}
```

**Resposta esperada:**

```json
{
  "task_id": "some-task-id"
}
```

### `GET /v1/results/{task_id}`

Consulta o resultado de uma task de scraping enviada anteriormente.

**Exemplo de resposta (task concluída com sucesso):**

```json
{
  "status": "SUCCESS",
  "data": {
    "razao_social": "Empresa Exemplo LTDA",
    "inscricao_estadual": "123456789",
    "nome_fantasia": "Exemplo Fantasia",
    "endereco": "Rua Exemplo, 123 - Bairro - Cidade/UF",
    "situacao_cadastral": "Ativa"
  }
}
```

**Exemplo de resposta (task pendente):**

```json
{
  "status": "PENDING"
}
```

**Exemplo de resposta (task com erro):**

```json
{
  "status": "FAILURE",
  "error": "Descrição do erro"
}
```
