from tkinter import Tk, Label, Button, Entry
import socket
import psutil

ven = Tk()
ven.title("Conexiones del servidor")
ven.configure(bg="pale green")
ven.geometry("700x500")

def main():
    def infor():
        server_ip = entrada1.get()
        server_port = entrada2.get()
        server_port = int(server_port)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((server_ip, server_port))
            
            active_connections = len(s.getsockname())
            salida1.delete(0, 'end')
            salida1.insert(0, active_connections)
            
            process_count = len(psutil.pids())
            salida2.delete(0, 'end')
            salida2.insert(0, process_count)
            
            s.close()
            
        except ConnectionRefusedError:
            print("No se pudo establecer la conexión con el servidor.")
        except Exception as e:
            print("Ocurrió un error:",e)
        
        ven.after(5000, infor)
    
    def borrado():
        entrada1.delete(0, 'end')
        entrada2.delete(0, 'end')

    texto1 = Label(ven, text="Ingrese direccion IP: ", bg="yellow")
    texto1.place(relx=0.03, rely=0.03, relwidth=0.18, relheight=0.08)
    entrada1 = Entry(ven, bg="pink")
    entrada1.place(relx=0.23, rely=0.03, relwidth=0.13, relheight=0.08)

    texto2 = Label(ven, text="Ingrese puerto: ", bg="yellow")
    texto2.place(relx=0.03, rely=0.13, relwidth=0.13, relheight=0.08)
    entrada2 = Entry(ven, bg="pink")
    entrada2.place(relx=0.18, rely=0.13, relwidth=0.13, relheight=0.08)

    ingresar = Button(ven, text="Ingresar", command=infor)
    ingresar.place(relx=0.03, rely=0.23, relwidth=0.1, relheight=0.08)

    borrar = Button(ven, text="Borrar", command=borrado)
    borrar.place(relx=0.41, rely=0.08, relwidth=0.1, relheight=0.08)

    texto3 = Label(ven, text="Numero de conexiones activas: ", bg="yellow")
    texto3.place(relx=0.32, rely=0.32, relwidth=0.26, relheight=0.08)
    salida1 = Entry(ven, bg="white")
    salida1.place(relx=0.32, rely=0.42, relwidth=0.29, relheight=0.08)

    texto4 = Label(ven, text="Numero de procesos en ejecucion: ", bg="yellow")
    texto4.place(relx=0.32, rely=0.52, relwidth=0.29, relheight=0.08)
    salida2 = Entry(ven, bg="white")
    salida2.place(relx=0.32, rely=0.62, relwidth=0.29, relheight=0.08)

if __name__ == "__main__":
    main()

ven.mainloop()