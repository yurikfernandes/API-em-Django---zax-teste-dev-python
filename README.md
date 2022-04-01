# ZAX - Processo Seletivo - Desenvolvedor(a) Python

Desafio lógico: Distribuir pedidos de lojas para motoboys

### Regras
- Motoboys não podem ficar sem pedido
- Motoboys podem atender exclusivamente determinada loja e tem prioridade
- As lojas não tem exclusividade com motoboys

### Output:
Ao chamar a rota passando como parâmetro o id do motoboy, deve retornar:

| id do motoboy | pedidos/lojas entregues | quanto vai ganhar |

## ✨ Solução

Os dados de entrada mais detalhados e a explicação da solução pode ser vista em:
https://docs.google.com/presentation/d/14J8kPTRAWp7Hb7FGDPQpx0vuHw0m_XXcIggPebsfMzc/edit?usp=sharing

## 🚀 Começando

Essas instruções permitirão que você obtenha uma cópia do projeto em operação na sua máquina local.

### 🔧 Instalação


Clone o repositório:

```
git clone https://github.com/yurikfernandes/zax-teste-dev-python.git
```

1. Entre no diretorio

```
cd zax-teste-dev-python
```

2. Inicialize um ambiente virtual:

```
python3 -m venv venv
```

3. Ative o ambiente virtual:

Para Unix ou MacOS:
```
source venv/bin/activate
```
Para windows:
```
venv\Scripts\activate.bat
```


4. Instale as bibliotecas necessárias usando o arquivo requirement.txt

```
pip install -r requirements.txt
```

5. Entre na pasta do projeto django:

```
cd teste
```

6. Faça as migrações necessárias:
```
python3 manage.py migrate --run-syncdb
python3 manage.py makemigrations
```

7. Preencha o banco de dados com dados testes disponibilizados em 'lojas.json', 'motoboys.json' e 'pedidos.json':

```
python3 manage.py loaddata lojas.json motoboys.json pedidos.json
```

8. Inicialize a aplicação
```
python3 manage.py runserver
```

## 🎮 Utilizando a ferramenta

Acesse a rota sem nenhum parâmetro para visualizar a distribuição total de pedidos:

```
localhost:8000/
```

```json
[   
    {
        "motoboy_id": 4,
        "pedidos": [
            {
                "id": 1,
                "loja": 1
            },
            {
                "id": 2,
                "loja": 1
            }
        ],
        "total_recebido": 9.0
    },

    ...

]

```


Acesse a rota com o parâmetro de id do motoboy para ver somente informações desse motoboy:

```
localhost:8000/1
```

```json
{
    "motoboy_id": 4,
    "pedidos": [
        {
            "id": 1,
            "loja": 1
        },
        {
            "id": 2,
            "loja": 1
        }
    ],
    "total_recebido": 9.0
}
```
