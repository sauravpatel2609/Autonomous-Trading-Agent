import { useEffect, useState, useRef, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Activity, Circle, TrendingUp, Clock } from 'lucide-react';
import { api, AgentStatus as ApiAgentStatus } from '@/lib/api';

interface LogMessage {
  timestamp: string;
  message: string;
  level: 'INFO' | 'WARNING' | 'ERROR' | 'DEBUG';
}

type DisplayStatus = 'RUNNING' | 'SLEEPING' | 'ERROR' | 'DISCONNECTED' | 'STOPPED';

export function AgentStatusComponent() {
  const [status, setStatus] = useState<DisplayStatus>('DISCONNECTED');
  const [agentInfo, setAgentInfo] = useState<ApiAgentStatus>({ running: false, ticker: null, task_id: null });
  const [logs, setLogs] = useState<LogMessage[]>([]);
  const [connectionError, setConnectionError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const scrollAreaRef = useRef<HTMLDivElement>(null);

  const fetchAgentStatus = useCallback(async () => {
    try {
      const agentStatus = await api.getAgentStatus();
      setAgentInfo(agentStatus);
      setLastUpdate(new Date());
      
      // Update display status based on agent running state
      if (agentStatus.running) {
        setStatus('RUNNING');
      } else {
        setStatus('STOPPED');
      }
    } catch (error) {
      console.error('Failed to fetch agent status:', error);
    }
  }, []);

  useEffect(() => {
    // Fetch initial agent status
    fetchAgentStatus();
    
    // Poll agent status every 10 seconds
    const statusInterval = setInterval(fetchAgentStatus, 10000);

    const connectWebSocket = () => {
      try {
        const ws = new WebSocket('ws://localhost:8000/ws/agent-logs');
        wsRef.current = ws;

        ws.onopen = () => {
          console.log('WebSocket connected');
          setConnectionError(null);
        };

        ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            const newLog: LogMessage = {
              timestamp: new Date().toISOString(),
              message: data.message || event.data,
              level: data.level || 'INFO',
            };
            
            setLogs(prevLogs => [newLog, ...prevLogs.slice(0, 99)]); // Keep last 100 logs
            
            // Update status based on log content
            if (data.status) {
              setStatus(data.status);
            }
          } catch (error) {
            // If not JSON, treat as plain text log
            const newLog: LogMessage = {
              timestamp: new Date().toISOString(),
              message: event.data,
              level: 'INFO',
            };
            setLogs(prevLogs => [newLog, ...prevLogs.slice(0, 99)]);
          }
        };

        ws.onclose = () => {
          console.log('WebSocket disconnected');
          setStatus('DISCONNECTED');
          setConnectionError('Connection lost. Attempting to reconnect...');
          
          // Attempt to reconnect after 3 seconds
          setTimeout(connectWebSocket, 3000);
        };

        ws.onerror = (error) => {
          console.error('WebSocket error:', error);
          setConnectionError('Failed to connect to agent logs');
          setStatus('ERROR');
        };
      } catch (error) {
        console.error('Failed to create WebSocket connection:', error);
        setConnectionError('Unable to establish WebSocket connection');
        setStatus('ERROR');
      }
    };

    connectWebSocket();

    return () => {
      clearInterval(statusInterval);
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [fetchAgentStatus]);

  const getStatusColor = (status: DisplayStatus) => {
    switch (status) {
      case 'RUNNING':
        return 'status-running';
      case 'SLEEPING':
        return 'status-sleeping';
      case 'ERROR':
        return 'status-error';
      case 'STOPPED':
        return 'text-muted-foreground';
      case 'DISCONNECTED':
        return 'text-muted-foreground';
      default:
        return 'text-muted-foreground';
    }
  };

  const getStatusBadge = (status: DisplayStatus) => {
    const variant = status === 'RUNNING' ? 'default' : 
                   status === 'SLEEPING' ? 'secondary' : 
                   status === 'STOPPED' ? 'outline' : 'destructive';
    
    return (
      <Badge variant={variant} className="flex items-center space-x-1">
        <Circle className={`h-2 w-2 fill-current ${getStatusColor(status)}`} />
        <span>{status}</span>
      </Badge>
    );
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString('en-US', {
      hour12: false,
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    });
  };

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'ERROR':
        return 'text-loss';
      case 'WARNING':
        return 'text-status-sleeping';
      case 'INFO':
        return 'text-foreground';
      case 'DEBUG':
        return 'text-muted-foreground';
      default:
        return 'text-foreground';
    }
  };

  return (
    <Card className="card-trading">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Activity className="h-5 w-5 text-primary" />
            <span>Agent Status & Logs</span>
          </div>
          {getStatusBadge(status)}
        </CardTitle>
      </CardHeader>
      <CardContent>
        {/* Agent Information Panel */}
        <div className="mb-4 grid grid-cols-1 md:grid-cols-3 gap-3">
          <div className="p-3 rounded-lg bg-muted/20 border border-border">
            <div className="flex items-center space-x-2 mb-1">
              <TrendingUp className="h-4 w-4 text-primary" />
              <span className="text-sm font-medium">Target Stock</span>
            </div>
            <p className="text-lg font-bold">
              {agentInfo.ticker || 'None'}
            </p>
          </div>
          
          <div className="p-3 rounded-lg bg-muted/20 border border-border">
            <div className="flex items-center space-x-2 mb-1">
              <Circle className={`h-4 w-4 ${agentInfo.running ? 'text-green-500' : 'text-muted-foreground'}`} />
              <span className="text-sm font-medium">Status</span>
            </div>
            <p className="text-lg font-bold">
              {agentInfo.running ? 'Running' : 'Stopped'}
            </p>
          </div>
          
          <div className="p-3 rounded-lg bg-muted/20 border border-border">
            <div className="flex items-center space-x-2 mb-1">
              <Clock className="h-4 w-4 text-primary" />
              <span className="text-sm font-medium">Last Update</span>
            </div>
            <p className="text-sm text-muted-foreground">
              {lastUpdate ? lastUpdate.toLocaleTimeString() : 'Never'}
            </p>
          </div>
        </div>

        {connectionError && (
          <div className="mb-3 rounded-lg border border-destructive/20 bg-destructive/10 p-2 text-sm text-destructive">
            {connectionError}
          </div>
        )}
        
        <div className="mb-2">
          <h4 className="text-sm font-medium text-foreground">Live Logs</h4>
          <p className="text-xs text-muted-foreground">Real-time agent activity logs</p>
        </div>
        
        <ScrollArea ref={scrollAreaRef} className="h-[300px] w-full">
          <div className="space-y-2 text-sm">
            {logs.length === 0 ? (
              <div className="text-center text-muted-foreground py-8">
                {status === 'DISCONNECTED' ? 'Connecting to agent logs...' : 'No logs available'}
              </div>
            ) : (
              logs.map((log, index) => (
                <div 
                  key={index} 
                  className="flex items-start space-x-2 rounded border-l-2 border-l-muted bg-muted/20 p-2 transition-smooth hover:bg-muted/40"
                >
                  <span className="text-xs text-muted-foreground font-mono">
                    {formatTimestamp(log.timestamp)}
                  </span>
                  <span className={`text-xs font-medium ${getLevelColor(log.level)}`}>
                    [{log.level}]
                  </span>
                  <span className="flex-1 text-sm">{log.message}</span>
                </div>
              ))
            )}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
}