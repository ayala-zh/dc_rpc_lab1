import socket
import json
import time

print("=== Starting RPC Server ===")

def add_numbers(params):
    return params.get('a', 0) + params.get('b', 0)

def get_time(params):
    return time.time()

def reverse_string(params):
    return params.get('text', '')[::-1]

# Available functions
FUNCTIONS = {
    'add': add_numbers,
    'get_time': get_time,
    'reverse': reverse_string
}

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind to all interfaces on port 5000
server_socket.bind(('0.0.0.0', 5000))
server_socket.listen(5)

print(f"✅ Server listening on 0.0.0.0:5000")
print(f"📋 Available methods: {list(FUNCTIONS.keys())}")

try:
    while True:
        print("\n⏳ Waiting for connection...")
        client_socket, address = server_socket.accept()
        print(f"🔗 Connection from {address}")
        
        # Receive request
        data = client_socket.recv(1024).decode('utf-8')
        print(f"📥 Received: {data}")
        
        try:
            # Parse JSON request
            request = json.loads(data)
            method = request.get('method')
            params = request.get('params', {})
            request_id = request.get('request_id', 'unknown')
            
            # Execute function
            if method in FUNCTIONS:
                result = FUNCTIONS[method](params)
                response = {
                    'request_id': request_id,
                    'result': result,
                    'status': 'OK'
                }
                print(f"✅ Executed {method}() = {result}")
            else:
                response = {
                    'request_id': request_id,
                    'error': f'Unknown method: {method}',
                    'status': 'ERROR'
                }
                print(f"❌ Unknown method: {method}")
                
        except Exception as e:
            response = {
                'request_id': request_id if 'request_id' in locals() else 'unknown',
                'error': str(e),
                'status': 'ERROR'
            }
            print(f"⚠️ Error processing request: {e}")
        
        # Send response
        response_json = json.dumps(response)
        client_socket.send(response_json.encode('utf-8'))
        print(f"📤 Sent: {response_json}")
        
        client_socket.close()
        
except KeyboardInterrupt:
    print("\n\n🛑 Server shutting down...")
    server_socket.close()
