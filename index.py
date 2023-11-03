from tkinter import ttk
from tkinter import *

import sqlite3  #es una base de dades que funciona a partir d'arxiu db. No necessita estar a un port com una db de red com Mysql

class Product: #classe que té tots els mètodes de les finestres (per posar, treure obj etc), i per crear la finestra (titol, botons etc)
    
    db_path = 'database.db' #guardem el fitxer de la base de dades en sqlite3
    
    def __init__(self, window): #definim la nostre finestra. li anirem afegint variables amb self.aaa   (sekf es el this de java) 
        self.wind = window
        self.wind.title('Aplicacó de productes')
        
        #frame
        frame = LabelFrame(self.wind, text = 'registrar un nou producte')  #creem un frame on hi posarem coses. (self.wind: a la nostra finestra, text: que s'hi mostra)
        frame.grid(row= 0, column=0, columnspan= 3, pady= 20)  #per colocar el frame on volguem. (files, columnes, cols vuides al inici, relleno vertical en pixels pk els seguents elements no es veiguin tant junts ) 
    
        #name input
        Label(frame, text = 'Nom : ').grid(row= 1, column= 0) #fem una etiqueta perque l'usuari entri dades
        self.nom = Entry(frame) #fem que l'usuari entri dades i ho guardem a la variable name per poder manipular-la
        self.nom.focus() #fa que el cursos comenci ya colocat per escriure a nom
        self.nom.grid(row= 1, column= 1)
        
        #price input
        Label(frame, text = 'Preu : ').grid(row= 2, column= 2)
        self.preu = Entry(frame) 
        self.preu.grid(row= 2, column= 3)
        
        
        #Taula
        self.tree = ttk.Treeview(height= 10, columns= 2) #es una taula de dades de 10 pixels d'altura i 2 columnes guardada a la variable tree
        self.tree.grid(row= 4, column=0 , columnspan= 2)
        self.tree.heading('#0', text = 'Nom', anchor= CENTER) #capçalera de la primera columna de caselles (indicata primera en #0). anchor = center vol dir que la capçalera esta centrada
        self.tree.heading('#1', text= 'Preu', anchor= CENTER) #una altra per la segona columna de caselles
        
        
        #Botó afegir producte:  command serveix per dir-li que ha de fer cada cop que es clica, ha d'estar en forma de funció
        ttk.Button(frame, text = 'Guardar producte', command= self.agregar_productes).grid(row= 3, columnspan= 2, sticky= W + E) #fem que al clicar-se cridi agreagar producte, per fer aquesta funció al clicar-se
                                                                                                                                 #sticky: desde on fins a on ocupa el botó, de oest (W) fins a est (E)
        
        #botons extres
        ttk.Button(frame, text = 'Esborrar', command= self.esborrar_productes).grid(row= 5, column= 0, sticky= W + E)
        ttk.Button(frame, text = 'Editar', command= self.editar_productes).grid(row= 5, column= 1, sticky= W + E)
        
        #output msg:    volem fer un missatge que sols es mostri quan volem
        self.missatge = Label(text= '', fg = 'red') #inicialment el missatge està buit. fg és per canviar el color del text
        self.missatge.grid(row = 3, column= 0 , columnspan= 2, sticky= W + E)
        
        
        self.rebre_productes()
        
    
    def executar_consulta(self, query, parameters = ()): #ens definim una funció que ens permet accedir a la base de dades. Per insterar dades: executem la funció amb (self, conulta d'insertar, dades a insertar)
        with sqlite3.connect(self.db_path) as conn: #metode per conenctar-te a la base de dades. li posem el nom conn
            cursor = conn.cursor() #permet obtenir la posició on estas de la base de dades
            result = cursor.execute(query, parameters) #permet executar una consulta sql
            conn.commit() #per executar la consulta
        return result
    
    def rebre_productes(self):
       #netejar la taula
       records = self.tree.get_children() #serveix per obtenir totes les dades de la taula 
       for element in records: 
           self.tree.delete(element) #eliminel cada element de la taula
       
       #consultar les dades
       query = 'SELECT * FROM product ORDER BY nom DESC' #agafem les dades de productes ordenades pel nom de forma descendent
       db_rows = self.executar_consulta(query)  #l'executem i ens torna les files de la base de dades
       
       for row in db_rows: #per cada fila en db_rows els intentarem insertar a la taula
           print(row)
           self.tree.insert('', 0, text = row[1], values= row[2]) #(tipus 1a dada, tipus 2a dada, 1a dada, 2a dada)(1a dada res,2a dada un numero, row[1] és on esta el nom del producte a la base de dades, igual pel preu)
    
    def validar(self): #mirem que els valors de les dades no son nuls per saber que hi ha dada
        return (len(self.nom.get()) != 0 and len(self.preu.get()) != 0) #el .get és per aconseguir el valor del que ha entrat l'usuari com a tal i no tot l'objecte sencer
    
    def agregar_productes(self): 
        if self.validar(): #si la validació és correcte:
            query = 'INSERT INTO product VALUES(NULL, ?, ?)' #creem una consulta d'insertar dades a producte amb (null "la id va per defecte", nom que s'ha escrit, preu que s'ha escrit)
            parameters = (self.nom.get(), self.preu.get())  #indiquem que son els interrogants de dalt
            self.executar_consulta(query, parameters)   #marquem que s'ha d'executar una consulta amb la creada anteriorment i els parametres que hem especificat
            self.missatge['text'] = 'El producte {} ha estat actualitzat satisfactoriament'.format(self.nom.get()) #actualitzem el valor missatge perque aparegui al agreagar el producte
            
            self.nom.delete(0, END) #netegem els inputs per poder tornar a entrar productes
            self.preu.delete(0, END)
        
        else:   #en cas que no s'insertin dades correctament
            self.missatge['text'] = 'no s"ha insertat cap producte, revisa els camps nom i preu'
        self.rebre_productes()
    
    def esborrar_productes(self): #volem que al apretar el botó esborrar esborri el producte seleccionat
        self.missatge['text'] = '' #el vuidem per actualitzar-lo despres
        try:    #fem servir l'equivalent a un try-catch per si passa que no hi ha cap producte seleccionat
            self.tree.item(self.tree.selection())['text'][0]   #ens quedem el 'text' del producte seleccionat (metode selection), el index 0
        except IndexError as e:
            self.missatge['text'] = 'Selecciona un producte'    #si no hi ha cap producte seleccionat ho indiquem al missatge vermell i acabem l'acció
            return
        self.missatge['text'] = ''
        nom = self.tree.item(self.tree.selection())['text'] #ens guardem el nom del producte seleccionat
        query = 'DELETE FROM product WHERE nom = ?' #fem la consulta d'esborrar el producte amb el nom especificat.
        self.executar_consulta(query, (nom, ))    #executem la consulta amb el nom guardat
        self.missatge['text'] = 'El producte {} ha estat eliminat satisfactoriament'.format(nom)
        self.rebre_productes()
    
    def editar_productes(self): #s'apren a fer finestres sobre finestres
        self.missatge['text'] = ''  #exactament igual que a esvorrar_productes. Mirem si s'ha seleccionat o no cap producte
        try:    
            self.tree.item(self.tree.selection())['text'][0]   
        except IndexError as e:
            self.missatge['text'] = 'Selecciona un producte'
            return
        
        nom_vell = self.tree.item(self.tree.selection())['text']    #guardem el nom i el preu del producte
        preu_vell = self.tree.item(self.tree.selection())['values'][0]
        self.finestra_editar = Toplevel()   #Toplvel ens permet crear una nova finestra secondària que es mostra sobre l'anterior
        self.finestra_editar.title = 'Editar producte'
        
        Label(self.finestra_editar, text = 'Nom antic: ').grid(row= 0, column= 1)
        Label(self.finestra_editar, text = 'Preu antic: ').grid(row= 1, column= 1)
        Label(self.finestra_editar, text= nom_vell).grid(row= 0, column= 2)
        Label(self.finestra_editar, text= preu_vell).grid(row= 1, column= 2)
        #Entry(self.finestra_editar, tetxtvariable = StringVar(self.finestra_editar, value = nom_vell), state = 'readonly').grid(row= 0, column= 2)   #posem que es pugui entrar text dins la finestra_editar. Mostrarà un string amb el nom antic que nomes es pot llegir (readonly)
                                                                                                                                                    #StringVar és un string ubicat a la finestra_editar que mostra el nom vell i nomes es pot llegir, no editar
        #Entry(self.finestra_editar, tetxtvariable = StringVar(self.finestra_editar, value = preu_vell), state = 'readonly').grid(row= 1, column= 2)
        
        Label(self.finestra_editar, text = 'Nom nou: ').grid(row= 0, column= 3)
        nom_nou = Entry(self.finestra_editar).grid(row= 0, column= 4)  
        Label(self.finestra_editar, text = 'Preu nou: ').grid(row= 1, column= 3)
        preu_nou = Entry(self.finestra_editar).grid(row= 1, column= 4)
        
        #fem un botó que ens permeti canviar el nom i el preu cridant a una altra funció
        ttk.Button(self.finestra_editar, text = 'Canviar nom/preu', command= lambda: self.editar_nom_productes(nom_nou.get(), nom_vell, preu_nou.get(), preu_vell)).grid(row= 4, column= 0, sticky= W)
   
    def editar_nom_productes(self, nom_nou, nom_vell, preu_nou, preu_vell): 
        query = 'UPDATE product SET nom = ?, preu = ? WHERE nom = ? AND preu = ?' #fem la consulta d'actualitzar nom i preu
        parameters = (nom_nou, preu_nou, nom_vell, preu_vell)
        self.executar_consulta(query, parameters)
        self.finestra_editar.destroy()
        self.missatge['text'] = 'El producte {} ha estat actualitzat correctament'.format(nom_vell)
        self.rebre_productes()
        
                
if __name__ == '__main__':  #basicament si s'executa com a main, ens desplega la finestra
    window = Tk() #crea una finestra
    application = Product(window)  #es guarda la finestra
    window.mainloop()  #la desplega
