#Aplicativo principal
from flask import Flask, render_template, url_for, redirect, request
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models import *
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
import email.message


login_manager = LoginManager()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUPERMEGADIFICIL'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/', methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        user = User.select_data_user_email(email)
        hash = user.senha
        if user and check_password_hash(hash, senha):
            login_user(user)

            return redirect(url_for('inicial'))
    return render_template('index.html')

@app.route('/cadastro', methods = ["POST", "GET"])
def cadastro():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        nome = request.form["nome"]
        hash = generate_password_hash(senha)

        User.insert_data_user(nome, email, hash)
        user = User.select_data_user_email(email)
        login_user(user)

        corpo = f"""
        <html lang="pt-BR">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email da Biblioteca</title>
  </head>
  <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4;">
    <!-- Container principal -->
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f4f4f4; padding: 20px;">
      <tr>
        <td>
          <!-- Tabela interna para layout do email -->
          <table align="center" cellpadding="0" cellspacing="0" width="600" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <!-- Cabeçalho -->
            <tr>
              <td align="center" style="background-color: #0056b3; padding: 20px 0; border-radius: 8px 8px 0 0;">
                <h1 style="color: #ffffff; margin: 0;">Bem-vindo à Biblioteca</h1>
              </td>
            </tr>
            <!-- Conteúdo principal -->
            <tr>
              <td style="padding: 20px;">
                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                  Prezado(a) Leitor(a) {current_user.nome},
                </p>
                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                  Estamos felizes em recebê-lo em nossa comunidade de leitores! A partir de agora, você terá acesso a uma vasta coleção de livros, eBooks, audiolivros e eventos exclusivos em nossa biblioteca.
                </p>
                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                  Para começar, sugerimos que explore nossa <a href="{url_for("login")}" style="color: #00796b; text-decoration: none;">seção de livros</a> ou participe de um dos nossos <strong>clubes de leitura</strong> semanais!
                </p>
                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                  Se precisar de ajuda, nossa equipe está à disposição para oferecer orientações e recomendações personalizadas.
                </p>
                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                  Aproveite ao máximo tudo o que nossa biblioteca tem a oferecer. Esperamos vê-lo em breve!
                </p>
              </td>
            </tr>
            <!-- Rodapé -->
            <tr>
              <td align="center" style="background-color: #0056b3; padding: 10px; border-radius: 0 0 8px 8px;">
                <p style="color: #ffffff; font-size: 14px; margin: 0;">
                  Biblioteca Virtual | Endereço: Rua IFRN, 123, Caicó | Telefone: (84) 99827-2514
                </p>
                <p style="color: #ffffff; font-size: 14px; margin: 0;">
                  <a href="{url_for("inicial")}" style="color: #80cbc4; text-decoration: none;">Visite nosso site</a> | <a href="mailto:bibliotecavirtual432@gmail.com" style="color: #80cbc4; text-decoration: none;">Entre em contato</a>
                </p>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
        """
        assunto = "Cadastro Bem Sucedido!"
        destinatario = current_user.email


        User.enviar_email(corpo, assunto, destinatario)



        return redirect(url_for("inicial"))
    return render_template('cadastro.html')

@app.route("/inicial")
@login_required
def inicial():
    user = current_user.nome
    return render_template("inicial.html", user = user)

@app.route("/logout", methods=['POST', 'GET'])
@login_required
def logout():
    if request.method == "POST":
        logout_user()
        return redirect(url_for("login"))
    return render_template("logout.html")

# Rotas adicionadas

@app.route('/listar_tarefas', methods=['GET'])
def listar_tarefas():
  descricao = request.args.get('descricao')
  status = request.args.get('status')
  data_inicio = request.args.get('data_inicio')
  data_fim = request.args.get('data_fim')
  prioridade = request.args.get('prioridade')
  categoria = request.args.get('categoria')

  print(f"Filtros aplicados: descricao={descricao}, status={status}, data_inicio={data_inicio}, data_fim={data_fim}, prioridade={prioridade}, categoria={categoria}")

    
  tarefas = buscar_tarefas(
        descricao=descricao,
        status=status,
        data_inicio=data_inicio,
        data_fim=data_fim,
        prioridade=prioridade,
        categoria=categoria
    )

  return render_template('listar_tarefas.html', tarefas=tarefas)

@app.route('/criar_editar_excluir', methods=['GET', 'POST'])
@app.route('/criar_editar_excluir/<int:tarefa_id>', methods=['GET', 'POST'])
def criar_editar_excluir(tarefa_id=None):
    if request.method == 'POST':
        descricao = request.form['descricao']
        data = request.form['data']
        prazo = request.form['prazo']
        status = request.form['status']
        prioridade = request.form['prioridade']
        categoria = request.form['categoria']
        
        if tarefa_id:
            # Atualizar tarefa
            editar_tarefa(tarefa_id, descricao, data, prazo, status, prioridade, categoria)
        else:
            # Criar nova tarefa
            criar_tarefa(descricao, data, prazo, status, prioridade, categoria)
        
        return redirect(url_for('listar_tarefas'))
    
    tarefa = None
    if tarefa_id:
        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_tarefas WHERE tar_id=%s", (tarefa_id,))
        tarefa = cursor.fetchone()
        cursor.close()
        conn.close()
    
    return render_template('criar_editar_excluir.html', tarefa=tarefa)

@app.route('/excluir_tarefa/<int:tarefa_id>', methods=['POST'])
def chama_excluir_tarefa(tarefa_id):
    excluir_tarefa(tarefa_id)
    return redirect(url_for('listar_tarefas'))

if __name__ == '__main__':
    app.run(debug=True)
