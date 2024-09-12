# pypigz

## Descrição

O `pypigz` é um pacote Python para leitura de arquivos Excel contendo dados de produtos e inserção desses dados em um banco de dados MySQL. Ele também inclui uma função para ser executada em uma função AWS Lambda, permitindo a automação do processo de leitura e inserção de dados.

## Instalação

Para instalar as dependências do projeto, utilize o Poetry:

```bash
poetry install
```

## Configuração

Crie um arquivo .env na raiz do projeto com as seguintes variáveis de ambiente:

``` dotenv
DB_HOST=localhost
DB_USER=user
DB_PASS=password
DB_NAME=database
DB_PORT=3306
```

## Utilização

Executando Localmente

Para executar o script localmente, utilize o seguinte comando:

```python
    python pypigz/main.py
```

## Executando na AWS Lambda

### Crie a função Lambda:

- No console da AWS, vá para o serviço Lambda e crie uma nova função.
- Escolha "Author from scratch" e forneça um nome para a função.
- Escolha um runtime compatível, como Python 3.8 ou superior.
- Crie ou escolha uma role que tenha permissões para acessar o S3 e o banco de dados.

### Configure o código da função Lambda:

- No editor de código da função Lambda, adicione o código do arquivo lambda_function.py.

### Configure as variáveis de ambiente:

- No console da AWS Lambda, vá para a seção "Configuration" e depois "Environment variables".
- Adicione as variáveis de ambiente necessárias para a conexão com o banco de dados (DB_HOST, DB_USER, DB_PASS, DB_NAME, DB_PORT).

### Configure o trigger do S3:

- No console da AWS Lambda, vá para a seção "Configuration" e depois "Triggers".
- Adicione um novo trigger para o S3 e configure-o para acionar a função Lambda quando um novo arquivo for carregado no bucket especificado.

### Teste a função Lambda:

- No console da AWS Lambda, vá para a seção "Test" e crie um novo evento de teste com o seguinte formato:

```json
{
  "merchantId": 1,
  "s3Bucket": "nome-do-seu-bucket",
  "s3Key": "caminho/para/o/arquivo.xlsx"
}
```

- Execute o teste e verifique se a função Lambda processa o arquivo corretamente e insere os dados no banco de dados.

## Estrutura do Projeto
- pypigz/main.py: Função principal para leitura e inserção de dados.
- pypigz/connection.py: Funções para conexão e execução de queries no banco de dados.
- pypigz/product.py: Classe para manipulação de dados de produtos e geração de queries SQL.
- .env: Arquivo de configuração com variáveis de ambiente.
- pyproject.toml: Arquivo de configuração do Poetry.
- poetry.lock: Arquivo de lock do Poetry.