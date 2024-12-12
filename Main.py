from tkinter import Tk, Label, Button, Entry
import socket
import psutil
import sqlite3
import configparser
from datetime import datetime

config = configparser.ConfigParser()
config.read('config.ini')
bg_texto = config.get('colores','bg_texto')
bg_ventana = config.get('colores','bg_ventana')
bg_label = config.get('colores','bg_label')
bg_boton = config.get('colores','bg_boton')

conn = sqlite3.connect('conexiones.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS registros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip TEXT,
    conexiones INTEGER,
    procesos INTEGER,
    fecha_hora TEXT
)
''')
conn.commit()

ven = Tk()
ven.title("Conexiones del servidor")
ven.configure(bg=bg_ventana)
ven.geometry("700x500")

def main():
    def infor(): 
        ip = entrada.get()
        conex = obtener_conexiones(ip)
        proc = obtener_procesos_activos()
        insertar_en_base_datos(ip, conex, proc)
        
        ven.after(5000, infor)
    
    def obtener_conexiones(ip):
        conexiones = []
        for conn in psutil.net_connections(kind='inet'):
            if conn.raddr and conn.raddr.ip == ip:
                conexiones.append(conn)
        can_conexiones = len(conexiones)
        salida.delete(0, 'end')
        salida.insert(0, can_conexiones)
        return len(conexiones)

    def obtener_procesos_activos():
        procesos = []
        for proc in psutil.process_iter(['pid', 'name']):
            procesos.append(proc.info)
        can_procesos = len(procesos)
        salida2.delete(0, 'end')
        salida2.insert(0, can_procesos)
        return len(procesos)
    
    def insertar_en_base_datos(ip, conexiones, procesos):
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
        INSERT INTO registros (ip, conexiones, procesos, fecha_hora)
        VALUES (?, ?, ?, ?)
        ''', (ip, conexiones, procesos, fecha_hora))
        conn.commit()
    
    def borrado():
        entrada.delete(0, 'end')
    
    def imprimido():
        cursor.execute('SELECT * FROM registros')
        registros = cursor.fetchall()
        for registro in registros:
            print(registro)

    texto = Label(ven, text="Ingrese direccion IP: ", bg=bg_texto)
    texto.place(relx=0.03, rely=0.03, relwidth=0.18, relheight=0.08)
    entrada = Entry(ven, bg="pink")
    entrada.place(relx=0.23, rely=0.03, relwidth=0.13, relheight=0.08)

    ingresar = Button(ven, text="Ingresar", command=infor)
    ingresar.place(relx=0.03, rely=0.23, relwidth=0.1, relheight=0.08)

    borrar = Button(ven, text="Borrar", command=borrado)
    borrar.place(relx=0.41, rely=0.08, relwidth=0.1, relheight=0.08)

    imprimir = Button(ven, text="Imprimir", command=imprimido)
    imprimir.place(relx=0.61, rely=0.08, relwidth=0.1, relheight=0.08)

    texto2 = Label(ven, text="Numero de conexiones activas: ", bg=bg_texto)
    texto2.place(relx=0.32, rely=0.32, relwidth=0.26, relheight=0.08)
    salida = Entry(ven, bg="white")
    salida.place(relx=0.32, rely=0.42, relwidth=0.29, relheight=0.08)

    texto3 = Label(ven, text="Numero de procesos en ejecucion: ", bg=bg_texto)
    texto3.place(relx=0.32, rely=0.52, relwidth=0.29, relheight=0.08)
    salida2 = Entry(ven, bg="white")
    salida2.place(relx=0.32, rely=0.62, relwidth=0.29, relheight=0.08)

if __name__ == "__main__":
    main()

ven.mainloop()

conn.close()