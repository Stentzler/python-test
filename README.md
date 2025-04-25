# python-test

## 1 - Rodando localmente

1.1 Criar o arquivo `.env` a partir do `.env.example`.
- Basta renomear o `.env.example` para `.env`.
- O conteúdo já está configurado corretamente para o ambiente de testes.

1.2 Subir os containers com Docker Compose:

```bash
docker compose up --build
```

> Obs: Execute o comando a partir da raiz do projeto (`python-test/`). Caso não tenha o Docker e o Docker Compose instalados, será necessário instalá-los primeiro.

1.3 Acessar a API:

- A aplicação estará disponível em: [http://localhost:8000](http://localhost:8000)

---

## 2 - Documentação da API

A documentação Swagger é gerada automaticamente utilizando FastAPI.

Após subir os containers, acesse:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 2.1 - `POST api/v1/scraping/`

Adiciona uma task de scraping na fila.

**Exemplo de Request:**

```json
{
  "cnpj": "12345678000195"
}
```

**Resposta 200 (Sucesso):**

```json
{
  "message": "Tarefa enviada com sucesso",
  "task_id": "f577fce5-e5b5-4b0c-a69a-91c65d24c472"
}
```

**Resposta 422 (Erro de validação):**

```json
{
    "detail": [
        {
            "type": "value_error",
            "loc": [
                "body",
                "cnpj"
            ],
            "msg": "Value error, CNPJ inválido: 00022244000177. Verifique se possui 14 dígitos e se estão corretos.",
            "input": "00022244000177",
            "ctx": {
                "error": {}
            }
        }
    ]
}
```

---

## 2.2 - `GET api/v1/results/{task_id}`

Consulta o status e o resultado da task de scraping.

**Exemplos de resposta:**

**Resposta 200 (Task enfileirada e pendente de processamento):**

```json
{
  "task_id": "f577fce5-e5b5-4b0c-a69a-91c65d24c472",
  "status": "pending",
  "data": null
}
```

**Resposta 200 (Task processada com sucesso, dados encontrados):**

```json
{
  "task_id": "f577fce5-e5b5-4b0c-a69a-91c65d24c472",
  "status": "done",
  "data": {
    "status": "success",
    "cnpj": "00022244999999",
    "razao_social": "RAZAO_SOCIAL",
    "nome_fantasia": "NOME_FANTASIA",
    "ie": "INSCRICAO_ESTADUAL",
    "regime": "Normal",
    "situacao": "Suspenso - NÃO HABILITADO",
    "unidade_auxiliar": "UNIDADE PRODUTIVA",
    "condicao_uso": "---",
    "data_final_contrato": "---",
    "data_cadastramento": "11/01/1989",
    "data_situacao": "05/07/2021",
    "operacoes_nf": "Habilitado",
    "atividade_principal": "ATIVIDADE_PRINCIPAL",
    "data_consulta": "25/04/2025 10:56:54",
    "endereco": "ENDEREÇO"
  }
}
```

**Resposta 200 (Task finalizada, mas sem dados encontrados):**

```json
{
  "task_id": "f577fce5-e5b5-4b0c-a69a-91c65d24c472",
  "status": "done",
  "data": {
    "status": "not_found",
    "cnpj": "00022244000175"
  }
}
```

**Resposta 404 (Task ID inválido ou não encontrado):**

```json
{
  "detail": "Nenhuma informação encontrada para o task_id: f577fce5-e5b5-4b0c-a69a-91c65d24c372"
}
```

---

## 3 - Rodando os testes

Este projeto possui testes automatizados separados para a API (`app/`) e para o worker (`worker/`).

### 3.1 - Instalando os requirements

Antes de rodar os testes localmente, é necessário instalar as dependências de cada serviço:

```bash
# Instalar dependências da API
pip install -r app/requirements.txt

# Instalar dependências do Worker
pip install -r worker/requirements.txt
```

> Obs: Ative seu ambiente virtual (venv, poetry, etc.) antes de instalar os pacotes.

### 3.2 - Executando os testes

Após instalar as dependências, execute:

```bash
pytest
```

O arquivo `pytest.ini` já está configurado para definir o diretório raiz (`rootdir`) e garantir que os testes rodem corretamente.

Você também pode executar os testes individualmente:

```bash
# Testes da API (FastAPI)
pytest tests/app

# Testes do Worker (Celery)
pytest tests/worker
```

---