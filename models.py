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


# Funções do banco de dados nas tabelas usuarios e livros

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
    
# SELECIONAR USER POR ID   
    @classmethod
    def select_data_user_id(cls, id):
        conexao = obter_conexao()
        cursor = conexao.cursor(dictionary=True)
        SELECT = 'SELECT * FROM tb_usuarios WHERE usu_email=%s'
        cursor.execute(SELECT, (id,))
        dados = cursor.fetchone()
        if dados:
            user = User(dados['usu_nome'], dados['usu_email'], dados['usu_senha'])
            user.id = dados['usu_id']

            cursor.close()
            conexao.close()

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

# Funções para gerenciar as tarefas

def buscar_tarefas(filtro=None):
    conn = obter_conexao()
    cursor = conn.cursor(dictionary=True)
    
    if filtro:
        # Exemplo de filtro (adapte conforme necessário)
        query = "SELECT * FROM tb_tarefas WHERE tar_descricao LIKE %s"
        cursor.execute(query, (f"%{filtro}%",))
    else:
        cursor.execute("SELECT * FROM tb_tarefas")
        
    tarefas = cursor.fetchall()
    cursor.close()
    conn.close()
    return tarefas

def criar_tarefa(descricao, data, prazo, status, prioridade, categoria):
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tb_tarefas (tar_descricao, tar_data, tar_prazo, tar_status, tar_prioridade, tar_categoria) VALUES (%s, %s, %s, %s, %s, %s)", 
                   (descricao, data, prazo, status, prioridade, categoria))
    conn.commit()
    cursor.close()
    conn.close()

def editar_tarefa(tarefa_id, descricao, data, prazo, status, prioridade, categoria):
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("UPDATE tb_tarefas SET tar_descricao=%s, tar_data=%s, tar_prazo=%s, tar_status=%s, tar_prioridade=%s, tar_categoria=%s WHERE tar_id=%s", 
                   (descricao, data, prazo, status, prioridade, categoria, tarefa_id))
    conn.commit()
    cursor.close()
    conn.close()

def excluir_tarefa(tarefa_id):
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tb_tarefas WHERE tar_id=%s", (tarefa_id,))
    conn.commit()
    cursor.close()
    conn.close()



