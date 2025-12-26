import socket
import json
import time
import uuid

class RPCClient:
    def __init__(self, server_ip, port=5000, timeout=2):
        self.server_ip = server_ip
        self.port = port
        self.timeout = timeout
    
    def call(self, method, params, max_retries=2):
        request_id = str(uuid.uuid4())[:8]
        request = {
            'request_id': request_id,
            'method': method,
            'params': params
        }
        
        print(f"\n📞 RPC Call #{request_id}")
        print(f"   Method: {method}")
        print(f"   Params: {params}")
        
        for attempt in range(max_retries):
            print(f"   Attempt {attempt + 1}/{max_retries}...")
            
            try:
                # Create socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self.timeout)
                
                # Connect
                start_time = time.time()
                sock.connect((self.server_ip, self.port))
                
                # Send request
                sock.send(json.dumps(request).encode('utf-8'))
                
                # Receive response
                response_data = sock.recv(1024).decode('utf-8')
                response_time = time.time() - start_time
                
                # Parse response
                response = json.loads(response_data)
                
                print(f"   ⏱️ Response time: {response_time:.2f}s")
                
                if response.get('status') == 'OK':
                    print(f"   ✅ Success! Result: {response.get('result')}")
                    sock.close()
                    return response.get('result')
                else:
                    print(f"   ❌ Error: {response.get('error')}")
                    
            except socket.timeout:
                print(f"   ⏰ Timeout after {self.timeout}s")
            except ConnectionRefusedError:
                print(f"   🔌 Connection refused - server not running")
            except Exception as e:
                print(f"   ⚠️ Error: {e}")
            
            # Wait before retry
            if attempt < max_retries - 1:
                wait = 1  # 1 second between retries
                print(f"   Waiting {wait}s before retry...")
                time.sleep(wait)
        
        print(f"   🚨 All retries failed")
        return None

# Test the client
if __name__ == "__main__":
    SERVER_IP = "172.31.19.11" 
    
    print("🚀 Starting RPC Client Tests")
    print(f"🔗 Connecting to server at {SERVER_IP}:5000")
    
    client = RPCClient(SERVER_IP, timeout=3)
    
    # Test 1: Add numbers
    print("\n" + "="*50)
    print("TEST 1: Add numbers")
    client.call('add', {'a': 5, 'b': 7})
    
    # Test 2: Get server time
    print("\n" + "="*50)
    print("TEST 2: Get server time")
    client.call('get_time', {})
    
    # Test 3: Reverse string
    print("\n" + "="*50)
    print("TEST 3: Reverse string")
    client.call('reverse', {'text': 'Hello RPC'})
    
    print("\n" + "="*50)
    print("✅ All tests completed")
