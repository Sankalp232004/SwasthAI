"""
Server-Sent Events (SSE) Routes
Realtime updates for doctor dashboard.

Implements push mechanism (NO POLLING).
Updates on:
- New patient
- Status change
- Priority override
"""

from flask import Blueprint, Response, stream_with_context
import json
import queue
import threading
from datetime import datetime

sse_bp = Blueprint('sse', __name__)

# Thread-safe message queues for each connected client
_clients = []
_clients_lock = threading.Lock()


class SSEClient:
    """Represents a connected SSE client."""
    
    def __init__(self):
        self.queue = queue.Queue()
        self.active = True
    
    def send(self, event_type: str, data: dict):
        """Queue a message to send to this client."""
        if self.active:
            self.queue.put({
                'event': event_type,
                'data': data,
                'timestamp': datetime.utcnow().isoformat()
            })
    
    def close(self):
        """Mark client as inactive."""
        self.active = False


def broadcast_queue_update(event_type: str, data: dict):
    """
    Broadcast an update to all connected clients.
    Called from API routes when changes occur.
    """
    with _clients_lock:
        inactive_clients = []
        for client in _clients:
            try:
                client.send(event_type, data)
            except Exception:
                inactive_clients.append(client)
        
        # Remove inactive clients
        for client in inactive_clients:
            _clients.remove(client)


@sse_bp.route('/queue')
def queue_stream():
    """
    SSE endpoint for realtime queue updates.
    Doctor dashboard connects here.
    Requires gevent worker class so this long-lived connection doesn't block
    Gunicorn threads for regular API requests.
    """
    def generate():
        client = SSEClient()

        with _clients_lock:
            _clients.append(client)

        try:
            # Send a padded initial event so Railway/Fastly CDN flushes immediately.
            # Some CDNs only flush once they see >= 1 kB; padding ensures that.
            padding = ':' + ' ' * 1024 + '\n'
            yield padding
            yield f"event: connected\ndata: {json.dumps({'message': 'Connected to queue updates'})}\n\n"

            while client.active:
                try:
                    # Wait for message with timeout (keep-alive interval)
                    message = client.queue.get(timeout=25)

                    event_type = message['event']
                    data = json.dumps({
                        'data': message['data'],
                        'timestamp': message['timestamp']
                    })

                    yield f"event: {event_type}\ndata: {data}\n\n"

                except queue.Empty:
                    # Send keepalive comment every 25 seconds to prevent proxy timeouts
                    yield f": keepalive {datetime.utcnow().isoformat()}\n\n"

        except GeneratorExit:
            pass
        finally:
            client.close()
            with _clients_lock:
                if client in _clients:
                    _clients.remove(client)
    
    response = Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no'
        }
    )
    
    return response


@sse_bp.route('/status')
def sse_status():
    """Check SSE service status."""
    with _clients_lock:
        client_count = len(_clients)
    
    return {
        'status': 'active',
        'connected_clients': client_count
    }
