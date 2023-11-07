from flask import  Flask, request, redirect, url_for, render_template
from database import myDb

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['JSON_SORT_KEY'] = False

# Cria o usuário quando o botão de cadastrar com todas as variáveis é acionado
@app.route("/users/create", methods=['POST'])
def create_user():
    nome = request.form.get('nome')
    email = request.form.get('email')   # variáveis são criadas resgatando os valores do formulário em cadastro.html
    senha = request.form.get('senha')
    telefone = request.form.get('telefone')

    # Conecta com o banco de dados e insere os dados
    myCursor = myDb.cursor()
    sql = f"INSERT INTO users (nome, senha, email, telefone) VALUES ('{nome}','{senha}','{email}','{telefone}')"
    myCursor.execute(sql)
    myDb.commit()

    # Agora obtenha o ID do usuário recém-criado
    userId = myCursor.lastrowid

    # Redirecione o usuário para a página de perfil pessoal com base no ID do usuário
    return redirect(url_for('perfil', userId=userId))

# O retorno é essa rota, a qual é responsável por retornar outra página
@app.route("/perfil/<int:userId>")
def perfil(userId):
    myCursor = myDb.cursor()
    sql = f"SELECT * FROM users WHERE id = {userId}" # Procura no banco de dados o id que foi passado no retorno da função "create_user"
    myCursor.execute(sql)
    usuario = myCursor.fetchone() # Aqui um linha do banco de dados é recuperada com a informação necessária"

    if usuario:
        # Renderize a página de perfil personalizada com as informações do usuário
        return render_template("perfil.html", usuario=usuario)
    else:
        # Trate o caso em que o usuário não existe (por exemplo, exiba uma mensagem de erro)
        return render_template("perfil_nao_encontrado.html")


# Essa rota é onde irá ser criado um estabelecimento 
@app.route("/establishment/create", methods=['POST'])
def create_establishment():
    estalecimento = request.form.get('nome')  # As variáveis criadas pegam o valor que veio do formulário de "landingPage.html"
    email = request.form.get('email') 
    myCursor = myDb.cursor()
    sql = f"INSERT INTO establishmentlist (estabelecimento, email) VALUES ('{estalecimento}', '{email}')" # Insere as informações no banco de dados
    myCursor.execute(sql)
    myDb.commit()

    return redirect(url_for('login')) # Por enquanto, a função retorna para a rota login

# Na rota login é renderizada a página de login
@app.route("/login", methods=['GET'])
def login():
    return render_template("login.html")


if '__main__' == __name__:
    app.run(debug=True)