# RPC Lab #1 - Distributed Computing

## Overview
Implementation of a Remote Procedure Call (RPC) system deployed on AWS EC2 instances. Demonstrates client-server communication, timeout/retry logic, and failure handling.

## Features
- TCP socket communication on port 5000
- JSON request/response format
- Request IDs using UUID
- Timeout (3 seconds) and retry logic (2 retries)
- Three remote functions: `add`, `get_time`, `reverse`

## Deployment on AWS EC2
1. Launch two Ubuntu 22.04 instances
2. Configure security group to allow:
   - SSH (port 22)
   - RPC (port 5000)
3. Install Python: `sudo apt install python3 python3-pip`
4. Copy files to instances

## Usage
### Server Instance:
`python3 server.py`

### Client Instance:
`python3 client.py`

## Files
- server.py - RPC server implementation
- client.py - RPC client with retry logic

## Failure Demonstration
To demonstrate timeout and retry behavior:

1. Add time.sleep(5) in server.py add_numbers() function
2. Restart server
3. Run client - observe timeout and retries

## RPC Semantics
This implementation demonstrates at-least-once semantics:

- Client retries ensure request delivery
- Server may execute duplicate requests
- Suitable for idempotent operations

## Author
Ayala Zholdybayeva
Group IT-2307
