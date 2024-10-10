from tkinter import Tk, Label, Button, Entry, Text, Scrollbar
import psutil

ven = Tk()
ven.title("Conexiones del servidor")
ven.configure(bg="pale green")
ven.geometry("700x500")

def main():
    def infor():
        server_ip = entrada1.get()
        server_port = entrada2.get()

        # Verificar si el usuario ingresó un puerto, si no, usar puerto 80 como predeterminado.
        if server_port:
            server_port = int(server_port)
        else:
            server_port = 80  # Puerto predeterminado

        try:
            # Obtener todas las conexiones de red activas
            connections = psutil.net_connections(kind='inet')

            # Limpiar la salida antes de mostrar nueva información
            salida1.delete('1.0', 'end')

            connection_count = 0

            for conn in connections:
                laddr = f"{conn.laddr.ip}:{conn.laddr.port}"
                raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "Desconocido"
                status = conn.status
                pid = conn.pid
                if pid:
                    try:
                        process = psutil.Process(pid)
                        process_name = process.name()
                    except psutil.NoSuchProcess:
                        process_name = "Desconocido"
                else:
                    process_name = "Sin proceso"

                if conn.raddr and conn.raddr.ip == server_ip and conn.raddr.port == server_port:
                    salida1.insert('end', f"Local: {laddr} | Remoto: {raddr} | Estado: {status} | Proceso: {process_name} (PID: {pid})\n")
                    connection_count += 1

            # Actualizar el número total de conexiones activas con el servidor especificado
            texto_conexiones["text"] = f"Conexiones activas: {connection_count}"

            # Mostrar el número de procesos en ejecución
            process_count = len(psutil.pids())
            salida2.delete(0, 'end')
            salida2.insert(0, process_count)

        except Exception as e:
            print("Ocurrió un error:", e)

    def borrado():
        entrada1.delete(0, 'end')
        entrada2.delete(0, 'end')
        salida1.delete('1.0', 'end')
        salida2.delete(0, 'end')

    texto1 = Label(ven, text="Ingrese dirección IP: ", bg="yellow")
    texto1.place(relx=0.03, rely=0.03, relwidth=0.18, relheight=0.08)
    entrada1 = Entry(ven, bg="pink")
    entrada1.place(relx=0.23, rely=0.03, relwidth=0.13, relheight=0.08)

    texto2 = Label(ven, text="Ingrese puerto (opcional): ", bg="yellow")
    texto2.place(relx=0.03, rely=0.13, relwidth=0.18, relheight=0.08)
    entrada2 = Entry(ven, bg="pink")
    entrada2.place(relx=0.23, rely=0.13, relwidth=0.13, relheight=0.08)

    ingresar = Button(ven, text="Ingresar", command=infor)
    ingresar.place(relx=0.03, rely=0.23, relwidth=0.1, relheight=0.08)

    borrar = Button(ven, text="Borrar", command=borrado)
    borrar.place(relx=0.41, rely=0.08, relwidth=0.1, relheight=0.08)

    texto_conexiones = Label(ven, text="Conexiones activas: 0", bg="yellow")
    texto_conexiones.place(relx=0.32, rely=0.32, relwidth=0.26, relheight=0.08)

    # Añadir un cuadro de texto con scroll para las conexiones
    scroll_bar = Scrollbar(ven)
    scroll_bar.place(relx=0.63, rely=0.42, relheight=0.4)

    salida1 = Text(ven, bg="white", yscrollcommand=scroll_bar.set)
    salida1.place(relx=0.32, rely=0.42, relwidth=0.29, relheight=0.4)
    scroll_bar.config(command=salida1.yview)

    texto4 = Label(ven, text="Número de procesos en ejecución: ", bg="yellow")
    texto4.place(relx=0.32, rely=0.82, relwidth=0.29, relheight=0.08)
    salida2 = Entry(ven, bg="white")
    salida2.place(relx=0.32, rely=0.9, relwidth=0.29, relheight=0.08)

if __name__ == "__main__":
    main()

ven.mainloop()