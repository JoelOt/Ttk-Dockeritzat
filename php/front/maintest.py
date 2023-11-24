from tkinter import ttk
from tkinter import *
import requests
import json

class Product:
    def __init__(self, window): #definim la nostre finestra. li anirem afegint variables amb self.aaa   (sekf es el this de java) 
        self.wind = window
        self.wind.title('Aplicacó de productes')
        
        #frame
        frame = LabelFrame(self.wind, text = 'registrar un nou producte')  #creem un frame on hi posarem coses. (self.wind: a la nostra finestra, text: que s'hi mostra)
        frame.grid(row= 0, column=0, columnspan= 3, pady= 20)  #per colocar el frame on volguem. (files, columnes, cols vuides al inici, relleno vertical en pixels pk els seguents elements no es veiguin tant junts ) 
    
        #name input
        Label(frame, text = 'request : ').grid(row= 1, column= 0) #fem una etiqueta perque l'usuari entri dades
        self.request = Entry(frame) #fem que l'usuari entri dades i ho guardem a la variable name per poder manipular-la
        self.request.focus() #fa que el cursos comenci ya colocat per escriure a nom
        self.request.grid(row= 1, column= 1)
        
        
        #Taula
        self.tree = ttk.Treeview(height= 10, columns= 2) #es una taula de dades de 10 pixels d'altura i 2 columnes guardada a la variable tree
        self.tree.grid(row= 4, column=0 , columnspan= 2)
        self.tree.heading('#0', text = 'Nom', anchor= CENTER) #capçalera de la primera columna de caselles (indicata primera en #0). anchor = center vol dir que la capçalera esta centrada
        self.tree.heading('#1', text= 'Preu', anchor= CENTER) #una altra per la segona columna de caselles
        
        
        #Botó afegir producte:  command serveix per dir-li que ha de fer cada cop que es clica, ha d'estar en forma de funció
        ttk.Button(frame, text = 'Seleccionar', command=self.seleccionar).grid(row= 3, columnspan= 2, sticky= W + E) #fem que al clicar-se cridi agreagar producte, per fer aquesta funció al clicar-se
                                                                                                                                 #sticky: desde on fins a on ocupa el botó, de oest (W) fins a est (E)
        #output msg:    volem fer un missatge que sols es mostri quan volem
        self.missatge = Label(text= '', fg = 'red') #inicialment el missatge està buit. fg és per canviar el color del text
        self.missatge.grid(row = 3, column= 0 , columnspan= 2, sticky= W + E)
        
    def seleccionar(self):  #consulta http
        
        request = self.request.get().split("?")
        if len(request) < 2:
            request.append('')
        url = "http://localhost:8080/CriticalDesignPBE/back/index.php?request={}&{}".format(request[0], request[1])  #url de l'arxiu index.php on s'envia la request per que el processi
        response = requests.get(url)  #fem una request post a l'url enviant les data
        print("STATUS: {}, url: {}".format(response.status_code, url))
        # verificar si la request és exitosa
        if response.status_code == 200: #200 exitosa, 404 url no trobat, 500 error en el php...
            producto = response.json()
            array_of_strings = [json.dumps(entry) for entry in producto]
            for entry_str in array_of_strings:
                entry_dict = json.loads(entry_str)
                day = entry_dict['day']
                print(day)
            
            hour = entry_dict['hour']
            subject = entry_dict['subject']
            room = entry_dict['room']
            
        else:
            self.missatge.config(text='Error al añadir el producto: {}'.format(response.status_code), fg='red')



if __name__ == '__main__':  #basicament si s'executa com a main, ens desplega la finestra
    window = Tk() #crea una finestra
    application = Product(window)  #es guarda la finestra
    window.mainloop()  #la desplega
