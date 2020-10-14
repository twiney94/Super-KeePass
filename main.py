from bottle import route, get, run, template, static_file, post, request
import os.path
from pykeepass import PyKeePass
from pykeepass.exceptions import CredentialsError # password error management


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')


################################################################
#Routage de tout ce qui référencé dans le dossier "ressources" vers le tout ce qui dans le dossier local "ressources"
@route('/ressources/<path:path>')
def callback(path):
    return static_file(path, root="./ressources/")
################################################################


################################################################
#Routage de /login vers la page de connexion
@route('/login')
def login():
    return template('login', loginError = '')
################################################################


################################################################
#Routage de /login vers la page de connexion AVEC LA METHODE POST
@post('/login')
def do_login():
    nameDB = request.forms.get('nameDB') #recuperation du nameDB depuis login.html
    inputPassword = request.forms.get('inputPassword') #recuperation du inputPassword depuis login.html
    if not os.path.exists('./ressources/' + str(nameDB)): #cherche si le chemin n'existe pas
        return template('login', loginError='<div class="alert alert-danger" role="alert">Please enter a correct filename (with extension)</div>') #retour au login.html avec erreur si chemin n'existe pas
    else:
        try:
            kp = PyKeePass('./ressources/' + str(nameDB), password=inputPassword) #identification au keepass
            entries=""
            for entry in kp.entries: #pour chaque element (entry) de kp.entries faire:
                x = str(entry).split('"', 1)
                x = str(x[1]).split('(', 1)
                title = str(x[0]) #split pour récupérer le Title
                username = str(x[1]).split(')', 1) #split pour récupérer le Username
                entries+="<tr><td>" + str(title) + "</td><td>" + str(username[0]) + "</td></tr>" #concaténer ligne à chaque itération
            return template('index', welcomeMsg='<div class="alert alert-success" id="success-alert" role="alert">Welcome to the Datadabase editing interface!<button type="button" class="close" data-dismiss="alert">x</button></div>', dbEntries=entries)
        except (RuntimeError, TypeError, NameError, CredentialsError): #Si erreur lors de l'identification faire:
            return template('login', loginError='<div class="alert alert-danger" role="alert">Please enter a correct password</div>') #retour au login.html avec erreur si password pas bon
################################################################


run(host='localhost', port=8088, reloader=True, debug=True)