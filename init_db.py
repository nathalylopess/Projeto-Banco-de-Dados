# Importando o conector MySQL
import mysql.connector

# Configurações de conexão
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost'
}

conn = None

try:
    # Conectando ao MySQL sem especificar o banco de dados
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Tentando criar o banco de dados se ele não existir
    cursor.execute("CREATE DATABASE IF NOT EXISTS gerenciador_tarefas")
    print("Banco de dados gerenciador_tarefas verificado/criado com sucesso.")

    # Seleciona o banco de dados criado
    cursor.execute("USE gerenciador_tarefas")
    
except mysql.connector.Error as erro:
    print(f"Erro ao conectar ou criar banco de dados: {erro}")
finally:
    if conn is not None:
        conn.close()

# Continuar com o script
db_config['database'] = 'gerenciador_tarefas'

if conn is not None:
    # Abre conexão novamente para executar o script SQL
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Localização do SQL
    SCHEMA = "database/database.sql"

    # Lê e executa o script SQL
    with open(SCHEMA, 'r') as f:
        sql_script = f.read()

    # Executa cada comando SQL
    for statement in sql_script.split(';'):
        if statement.strip():
            try:
                cursor.execute(statement)
            except mysql.connector.Error as e:
                print(f"Erro ao executar statement: {e}")

    # Finaliza a transação
    conn.commit()
    cursor.close()
    conn.close()
    print("Script executado com sucesso.")
