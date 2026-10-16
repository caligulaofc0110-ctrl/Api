
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Dados fictícios para testes
alunos = [
    {
        "id": 1,
        "nome": "Ana Silva",
        "primeiroBimestre": 8.0,
        "segundoBimestre": 9.0
    },
    {
        "id": 2,
        "nome": "Pedro Santos",
        "primeiroBimestre": 7.0,
        "segundoBimestre": 8.5
    },
    {
        "id": 3,
        "nome": "Maria Oliveira",
        "primeiroBimestre": 9.5,
        "segundoBimestre": 8.0
    }
]


# Rota inicial para testar a API
@app.route("/")
def inicio():
    return jsonify({
        "mensagem": "API de notas escolares funcionando!"
    })


# Buscar todos os alunos
@app.route("/alunos", methods=["GET"])
def listar_alunos():
    return jsonify(alunos)


# Buscar um aluno específico
@app.route("/alunos/<int:id_aluno>", methods=["GET"])
def buscar_aluno(id_aluno):
    aluno = next(
        (a for a in alunos if a["id"] == id_aluno),
        None
    )

    if aluno is None:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    return jsonify(aluno)


# Atualizar as notas de um aluno
@app.route(
    "/alunos/<int:id_aluno>/notas",
    methods=["PATCH"]
)
def atualizar_notas(id_aluno):
    aluno = next(
        (a for a in alunos if a["id"] == id_aluno),
        None
    )

    if aluno is None:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Envie um JSON válido"}), 400

    try:
        nota1 = float(dados["primeiroBimestre"])
        nota2 = float(dados["segundoBimestre"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"erro": "Envie as duas notas"}), 400

    if not (0 <= nota1 <= 10 and 0 <= nota2 <= 10):
        return jsonify({
            "erro": "As notas devem estar entre 0 e 10"
        }), 400

    aluno["primeiroBimestre"] = nota1
    aluno["segundoBimestre"] = nota2

    return jsonify({
        "mensagem": "Notas atualizadas!",
        "aluno": aluno
    })


if __name__ == "__main__":
    app.run(debug=True)
