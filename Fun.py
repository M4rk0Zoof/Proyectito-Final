def infor(server_ip, server_port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((server_ip, server_port))
        
        active_connections = len(s.getsockname())
        print("Número de conexiones activas:",active_connections)
        
        process_count = len(psutil.pids())
        print("Número de procesos en ejecución:",process_count)
        
        s.close()
    
    except ConnectionRefusedError:
        print("No se pudo establecer la conexión con el servidor.")
    except Exception as e:
        print("Ocurrió un error:",e)

def borrado():
    entrada1.delete(0,'end')
    entrada2.delete(0,'end')