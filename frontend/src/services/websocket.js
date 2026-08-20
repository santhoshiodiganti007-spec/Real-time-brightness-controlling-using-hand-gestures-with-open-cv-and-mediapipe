/**
 * WebSocket Connection Service with automatic reconnect and event listener dispatching.
 */
class WebSocketService {
  constructor() {
    this.ws = null;
    this.listeners = new Set();
    const getWsUrl = () => {
      if (import.meta.env.VITE_WS_URL) {
        return import.meta.env.VITE_WS_URL;
      }
      if (typeof window !== 'undefined' && (window.location.port === '8000' || window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')) {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        return `${protocol}//${window.location.hostname}:8000/ws/brightness`;
      }
      return 'ws://127.0.0.1:8000/ws/brightness';
    };
    this.url = getWsUrl();
  }

  connect() {
    if (this.ws && (this.ws.readyState === WebSocket.CONNECTING || this.ws.readyState === WebSocket.OPEN)) {
      return;
    }

    try {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        this.isConnected = true;
        console.log('[WS] Connected to Touchless Brightness Stream');
        if (this.reconnectTimer) clearTimeout(this.reconnectTimer);
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.listeners.forEach((callback) => callback(data));
        } catch (e) {
          console.error('[WS] Error parsing message payload:', e);
        }
      };

      this.ws.onclose = () => {
        this.isConnected = false;
        console.log('[WS] Connection closed. Attempting reconnect in 2s...');
        this.reconnectTimer = setTimeout(() => this.connect(), 2000);
      };

      this.ws.onerror = (err) => {
        console.error('[WS] Error:', err);
        this.ws.close();
      };
    } catch (e) {
      console.error('[WS] Initialization failed:', e);
      this.reconnectTimer = setTimeout(() => this.connect(), 2000);
    }
  }

  subscribe(callback) {
    this.listeners.add(callback);
    if (!this.isConnected) {
      this.connect();
    }
    return () => this.listeners.delete(callback);
  }

  disconnect() {
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer);
    if (this.ws) {
      this.ws.close();
    }
    this.listeners.clear();
  }
}

export const wsService = new WebSocketService();
export default wsService;
