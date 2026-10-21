"""
Application Web Flask pour une calculatrice simple. 

Ce module gère les requêtes HTTP, analyse les expressions mathématiques, 
appelle l'opération appropriée et renvoie le résultat à l'utilisateur via une interface web.

"""
from flask import Flask, request, render_template
from operators import add, subtract, multiply, divide

app = Flask(__name__)
# Associe les symboles d'opération aux fonctions correspondantes.
OPS = {
    '+': add,
    '-': subtract,
    '*': multiply,
    '/': divide,
}

def calculate(expr: str):
    """
    Évalue une expression mathématique contenant deux opérandes et un seul opérateur (+, -, *, /).
    
    Paramètres: 
        expr (str): L'expression mathématique à évaluer, par exemple "3 + 4".

    Return:
        float: Le résultat de l'opération.

    Raises:
        ValueError: Si l'expression est vide, mal formée, ou si les opérandes ne sont pas des nombres.

    """
    if not expr or not isinstance(expr, str):
        raise ValueError("empty expression")
    # Retire les espaces avant d'analyser l'expression
    s = expr.replace(" ", "")

    op_pos = -1
    op_char = None
    # Cette boucle parcourt chaque caractère de l'expression pour trouver 
    # l'opérateur et qu'il y en a un seul.
    for i, ch in enumerate(s):
        if ch in OPS:
            if op_pos != -1:
                raise ValueError("only one operator is allowed")
            op_pos = i
            op_char = ch

    if op_pos <= 0 or op_pos >= len(s) - 1:
        # operator at start/end or not found
        raise ValueError("invalid expression format")

    left = s[:op_pos]
    right = s[op_pos+1:]

    # Convertit les deux opérandes en float et gère les erreurs de conversion.
    try:
        a = float(left)
        b = float(right)
    except ValueError:
        raise ValueError("operands must be numbers")

    return OPS[op_char](a, b)

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Affiche la page de la calculatrice et traite les expressions soumises par l'utilisateur via le formulaire HTML.

    Return: 
        str: Le rendu HTML de la page avec le résultat du calcul ou un message d'erreur.
    """
    result = ""
    if request.method == 'POST':
        expression = request.form.get('display', '')
        try:
            result = calculate(expression)
        except Exception as e:
            result = f"Error: {e}"
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)