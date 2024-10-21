# Sistema de Gerenciamento de Tarefas

## Descrição
Este projeto é um sistema de gerenciamento de tarefas que permite aos usuários se cadastrarem, fazerem login e gerenciarem suas tarefas com funcionalidades de criação, edição, exclusão e filtragem.

## Tecnologias Utilizadas
* Flask: Framework para desenvolvimento web em Python.
* MySQL: Sistema de gerenciamento de banco de dados.
* HTML/CSS: Para a construção do front-end.

## Passo a passo:

### 1. Instalação das Dependências
Instale as bibliotecas e dependências necessárias através do `requirements.txt`. Recomenda-se que utilize um ambiente virtual para evitar conflitos de pacotes.

```bash
pip install -r requirements.txt
```
### 2. Crie a Database com o `init_db.py`

**Linux:**
```bash
python3 init_db.py
```

**Windows**
```bash
python init_db.py
```

### 3. Execute a aplicação
```bash
flask run --debug
```

