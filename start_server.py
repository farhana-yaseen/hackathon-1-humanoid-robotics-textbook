import os
import sys
import subprocess
import time

def kill_port_process(port):
    """Kill process using the specified port on Windows"""
    try:
        # Find the process using the port
        result = subprocess.run(
            f'netstat -ano | findstr :{port}',
            shell=True,
            capture_output=True,
            text=True
        )

        if result.stdout:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'LISTENING' in line:
                    # Extract PID (last column)
                    pid = line.split()[-1]
                    print(f"Killing process {pid} using port {port}")
                    subprocess.run(f'taskkill /F /PID {pid}', shell=True)
                    time.sleep(1)
    except Exception as e:
        print(f"Error killing process on port {port}: {e}")

def start_server():
    """Start the backend server on port 8000"""
    try:
        # Kill any existing process on port 8000
        kill_port_process(8000)

        # Change to backend directory
        os.chdir('backend')

        # Import and start the FastAPI app
        sys.path.insert(0, '.')
        from main import app
        import uvicorn

        print("Starting backend server on port 8000...")
        uvicorn.run(app, host='127.0.0.1', port=8000)

    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    start_server()