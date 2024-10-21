from flask_login import UserMixin
import mysql.connector as sql
import smtplib
import email.message

def obter_conexao():
    db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'genrenciador_tarefas'
}
    conn = sql.connect(**db_config)
    return conn

class User(UserMixin):
    id: str
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha


# Inserir funções de controle de login

    @classmethod
    def get(cls, id):
        conexao = obter_conexao()
        cursor = conexao.cursor()
        SELECT = 'SELECT * FROM tb_usuarios WHERE usu_id=%s'
        cursor.execute(SELECT, (id,))
        dados = cursor.fetchone()
        if dados:
            user = User(dados[1],dados[2], dados[3])
            user.id = dados[0]
        else: 
            user = None
        return user

# INSERIR USER
    @classmethod
    def insert_data_user(cls, nome, email, senha):
        conexao = obter_conexao()
        cursor = conexao.cursor()
        INSERT = 'INSERT INTO tb_usuarios (usu_nome, usu_email, usu_senha) VALUES (%s, %s, %s)'
        cursor.execute(INSERT, (nome, email, senha,))
        conexao.commit()
        cursor.close()
        conexao.close()

#ENVIAR EMAIL
    @classmethod
    def enviar_email(cls, corpo, assunto, destinatario):
        
        corpo_email = corpo
        msg = email.message.Message()
        msg["Subject"] = assunto
        msg["From"] = "bibliotecavirtual432@gmail.com"
        msg["To"] = destinatario
        password = "mjdiinyyrzelbicy"
        msg.add_header("Content-Type", "text/html")
        msg.set_payload(corpo_email)
        s = smtplib.SMTP("smtp.gmail.com: 587")
        s.starttls()
        s.login(msg["From"], password)
        s.sendmail(msg["From"], [msg["To"]], msg.as_string().encode("utf-8"))

# Funções do banco de dados nas tabelas usuarios 

# SELECIONAR USER POR EMAIL   
    @classmethod
    def select_data_user_email(cls, email):
        conexao = obter_conexao()
        cursor = conexao.cursor(buffered=True)
        SELECT = 'SELECT * FROM tb_usuarios WHERE usu_email=%s'
        cursor.execute(SELECT, (email,))
        dados = cursor.fetchone()
        if dados:
            user = User(dados[1], dados[2], dados[3])
            user.id = dados[0]

            conexao.commit()
            cursor.close()

            return user

class Tarefa:
    @staticmethod
    def buscar_tarefas(id_usuario, descricao=None, status=None, data_inicio=None, data_fim=None, prioridade=None, categoria=None):
        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True)

        # Base da query
        query = "SELECT * FROM tb_tarefas WHERE tar_usu_id = %s"
        params = [id_usuario]

        # Adiciona condições dinamicamente
        if descricao:
            query += " AND tar_descricao LIKE %s"
            params.append(f"%{descricao}%")
        
        if status   is not None :
            query += " AND tar_status = %s"
            params.append(status)
        
        if data_inicio:
            query += " AND tar_data >= %s"
            params.append(data_inicio)
        
        if data_fim:
            query += " AND tar_data <= %s"
            params.append(data_fim)
        
        if prioridade is not None:
            query += " AND tar_prioridade = %s"
            params.append(prioridade)
        
        if categoria is not None:
            query += " AND tar_categoria = %s"
            params.append(categoria)

        # Executa a query com os parâmetros
        cursor.execute(query, params)
        tarefas = cursor.fetchall()

        cursor.close()
        conn.close()

        return tarefas

    @staticmethod
    def criar_tarefa(descricao, data, prazo, status, prioridade, categoria, usu_id):
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tb_tarefas (tar_descricao, tar_data, tar_prazo, tar_status, tar_prioridade, tar_categoria, tar_usu_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (descricao, data, prazo, status, prioridade, categoria, usu_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def editar_tarefa(tarefa_id, descricao, data, prazo, status, prioridade, categoria):
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tb_tarefas SET tar_descricao=%s, tar_data=%s, tar_prazo=%s, tar_status=%s, tar_prioridade=%s, tar_categoria=%s WHERE tar_id=%s",
            (descricao, data, prazo, status, prioridade, categoria, tarefa_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def excluir_tarefa(tarefa_id):
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tb_tarefas WHERE tar_id=%s", (tarefa_id,))
        conn.commit()
        cursor.close()
        conn.close()
