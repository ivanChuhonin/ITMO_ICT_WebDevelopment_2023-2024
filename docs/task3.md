# Упражнение 3

## Код

### Клиента
```python
def run_tcp_client(port: int, buffer_size: int) -> None:
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', port, ))
    except OSError as msg:
        print(msg)
        sys.exit(1)

    if client is None:
        print('could not open client socket')
        sys.exit(1)

    with client:
        hi = 'hi'.encode('utf-8')
        data = client.recv(buffer_size)
        print(data.decode('utf-8'))
        time.sleep(1.0)
        # get html again
        client.sendall(hi)
        data = client.recv(buffer_size)
        print(data.decode('utf-8'))
        time.sleep(1.0)
        # stop it
        stop = 'stop'.encode('utf-8')
        client.sendall(stop)
```

### Сервер 
```python
def create_server() -> socket:
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('127.0.0.1', 0, ))
        server.listen(1)
    except OSError as msg:
        print(msg)
        sys.exit(1)

    if server is None:
        print('could not open server socket')
        sys.exit(1)

    return server

def run_server_connection(server: socket) -> None:
    print('Wait...')
    conn, addr = server.accept()
    with conn:
        print('Connected by', addr)
        file = open("hello.html", "r")
        hello = file.read()
        data = hello.encode('utf-8')
        conn.send(data)
        while True:
            r = conn.recv(1024)
            if r.decode('utf-8') == 'stop':
                break
            conn.send(data)
```
### index.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>3-socket</title>
</head>
<body>
    <p>
        Today is a beautiful day. We go swimming and fishing.
    </p>
</body>
</html>
```