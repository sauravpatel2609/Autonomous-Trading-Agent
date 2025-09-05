import { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Play, Square, Settings, AlertCircle, CheckCircle, Shield, TrendingUp, AlertTriangle } from 'lucide-react';
import { api, AgentStatus } from '@/lib/api';
import { useAuth } from '@/components/Auth/AuthContext';

export function AgentControlComponent() {
  const { isAuthenticated } = useAuth();
  const [selectedStock, setSelectedStock] = useState('GOOGL');
  const [isStarting, setIsStarting] = useState(false);
  const [isStopping, setIsStopping] = useState(false);
  const [isSettingProtection, setIsSettingProtection] = useState(false);
  const [isEmergencySelling, setIsEmergencySelling] = useState(false);
  const [agentStatus, setAgentStatus] = useState<AgentStatus>({ running: false, ticker: null, task_id: null });
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [stopLossPercent, setStopLossPercent] = useState('5');
  const [takeProfitPercent, setTakeProfitPercent] = useState('10');

  const popularStocks = [
    'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 
    'META', 'NVDA', 'NFLX', 'AMD', 'INTC'
  ];

  const fetchAgentStatus = useCallback(async () => {
    try {
      const status = await api.getAgentStatus();
      setAgentStatus(status);
      if (status.ticker && status.ticker !== selectedStock) {
        setSelectedStock(status.ticker);
      }
    } catch (error) {
      console.error('Failed to fetch agent status:', error);
    }
  }, [selectedStock]);

  useEffect(() => {
    // Fetch initial agent status
    fetchAgentStatus();
    
    // Poll agent status every 5 seconds
    const interval = setInterval(fetchAgentStatus, 5000);
    return () => clearInterval(interval);
  }, [fetchAgentStatus]);

  const handleStartAgent = async () => {
    if (!isAuthenticated) {
      setError('Please log in to control the agent');
      return;
    }

    setIsStarting(true);
    setError(null);
    try {
      const response = await api.startAgent(selectedStock);
      if (response.status === 'success') {
        await fetchAgentStatus(); // Refresh status immediately
      } else {
        setError(response.message);
      }
    } catch (error) {
      console.error('Error starting agent:', error);
      setError(error instanceof Error ? error.message : 'Failed to start agent');
    } finally {
      setIsStarting(false);
    }
  };

  const handleStopAgent = async () => {
    if (!isAuthenticated) {
      setError('Please log in to control the agent');
      return;
    }

    setIsStopping(true);
    setError(null);
    setSuccess(null);
    try {
      const response = await api.stopAgent();
      if (response.status === 'success') {
        setSuccess('Agent stopped and protective orders placed automatically!');
        await fetchAgentStatus(); // Refresh status immediately
      } else {
        setError(response.message);
      }
    } catch (error) {
      console.error('Error stopping agent:', error);
      setError(error instanceof Error ? error.message : 'Failed to stop agent');
    } finally {
      setIsStopping(false);
    }
  };

  const handleSetupProtection = async () => {
    if (!isAuthenticated) {
      setError('Please log in to setup protective orders');
      return;
    }

    setIsSettingProtection(true);
    setError(null);
    setSuccess(null);
    try {
      const response = await api.setupProtectiveOrders(
        selectedStock, 
        parseFloat(stopLossPercent), 
        parseFloat(takeProfitPercent)
      );
      if (response.status === 'success') {
        setSuccess(`Protective orders placed: ${stopLossPercent}% stop-loss, ${takeProfitPercent}% take-profit`);
      } else {
        setError(response.message);
      }
    } catch (error) {
      console.error('Error setting up protection:', error);
      setError(error instanceof Error ? error.message : 'Failed to setup protective orders');
    } finally {
      setIsSettingProtection(false);
    }
  };

  const handleEmergencySell = async () => {
    if (!isAuthenticated) {
      setError('Please log in to execute emergency sell');
      return;
    }

    const confirmed = window.confirm(
      `Are you sure you want to IMMEDIATELY SELL ALL ${selectedStock} shares at market price? This action cannot be undone.`
    );
    
    if (!confirmed) return;

    setIsEmergencySelling(true);
    setError(null);
    setSuccess(null);
    try {
      const response = await api.emergencySell(selectedStock);
      if (response.status === 'success') {
        setSuccess(`Emergency sell order placed for ${selectedStock}!`);
      } else {
        setError(response.message);
      }
    } catch (error) {
      console.error('Error executing emergency sell:', error);
      setError(error instanceof Error ? error.message : 'Failed to execute emergency sell');
    } finally {
      setIsEmergencySelling(false);
    }
  };

  return (
    <Card className="card-trading">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Settings className="h-5 w-5 text-primary" />
            <span>Agent Control</span>
          </div>
          <div className="flex items-center space-x-2">
            {agentStatus.running ? (
              <>
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span className="text-xs px-2 py-1 bg-green-500/20 text-green-600 rounded-full font-medium">
                  RUNNING
                </span>
              </>
            ) : (
              <>
                <Square className="h-4 w-4 text-muted-foreground" />
                <span className="text-xs px-2 py-1 bg-muted text-muted-foreground rounded-full font-medium">
                  STOPPED
                </span>
              </>
            )}
          </div>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Error Display */}
        {error && (
          <div className="p-3 rounded-lg bg-destructive/10 border border-destructive/20 text-destructive flex items-center space-x-2">
            <AlertCircle className="h-4 w-4" />
            <p className="text-sm">{error}</p>
          </div>
        )}

        {/* Success Display */}
        {success && (
          <div className="p-3 rounded-lg bg-green-500/10 border border-green-500/20 text-green-600 flex items-center space-x-2">
            <CheckCircle className="h-4 w-4" />
            <p className="text-sm">{success}</p>
          </div>
        )}

        {/* Authentication Warning */}
        {!isAuthenticated && (
          <div className="p-3 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-600 flex items-center space-x-2">
            <AlertCircle className="h-4 w-4" />
            <p className="text-sm">Please log in to control the trading agent</p>
          </div>
        )}

        {/* Current Running Status */}
        {agentStatus.running && agentStatus.ticker && (
          <div className="p-3 rounded-lg bg-green-500/10 border border-green-500/20 text-green-600">
            <p className="text-sm font-medium">
              🚀 Auto-trading agent running for <span className="font-bold">{agentStatus.ticker}</span>
            </p>
            <p className="text-xs mt-1">Buying and selling automatically based on AI predictions</p>
          </div>
        )}

        <Tabs defaultValue="control" className="space-y-4">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="control">Agent Control</TabsTrigger>
            <TabsTrigger value="protection">Protection</TabsTrigger>
            <TabsTrigger value="emergency">Emergency</TabsTrigger>
          </TabsList>

          <TabsContent value="control" className="space-y-4">
            <div>
              <label className="text-sm font-medium text-foreground mb-2 block">
                Target Stock
              </label>
              <Select 
                value={selectedStock} 
                onValueChange={setSelectedStock}
                disabled={agentStatus.running}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select a stock" />
                </SelectTrigger>
                <SelectContent>
                  {popularStocks.map((stock) => (
                    <SelectItem key={stock} value={stock}>
                      {stock}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="grid grid-cols-2 gap-2">
              <Button
                onClick={handleStartAgent}
                disabled={isStarting || isStopping || agentStatus.running || !isAuthenticated}
                className="flex items-center space-x-2 transition-smooth bg-profit hover:bg-profit/90"
              >
                {isStarting ? (
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-primary-foreground border-t-transparent"></div>
                ) : (
                  <Play className="h-4 w-4" />
                )}
                <span>Start Auto-Trading</span>
              </Button>

              <Button
                onClick={handleStopAgent}
                disabled={isStopping || isStarting || !agentStatus.running || !isAuthenticated}
                variant="destructive"
                className="flex items-center space-x-2 transition-smooth"
              >
                {isStopping ? (
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-primary-foreground border-t-transparent"></div>
                ) : (
                  <Square className="h-4 w-4" />
                )}
                <span>Stop & Protect</span>
              </Button>
            </div>
          </TabsContent>

          <TabsContent value="protection" className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-sm font-medium text-foreground mb-2 block">
                  Stop-Loss %
                </label>
                <Input
                  type="number"
                  value={stopLossPercent}
                  onChange={(e) => setStopLossPercent(e.target.value)}
                  placeholder="5"
                  min="0.1"
                  max="50"
                  step="0.1"
                />
              </div>
              <div>
                <label className="text-sm font-medium text-foreground mb-2 block">
                  Take-Profit %
                </label>
                <Input
                  type="number"
                  value={takeProfitPercent}
                  onChange={(e) => setTakeProfitPercent(e.target.value)}
                  placeholder="10"
                  min="0.1"
                  max="100"
                  step="0.1"
                />
              </div>
            </div>

            <Button
              onClick={handleSetupProtection}
              disabled={isSettingProtection || !isAuthenticated}
              className="w-full flex items-center space-x-2 bg-blue-600 hover:bg-blue-700"
            >
              {isSettingProtection ? (
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-primary-foreground border-t-transparent"></div>
              ) : (
                <Shield className="h-4 w-4" />
              )}
              <span>Setup Protective Orders</span>
            </Button>

            <div className="rounded-lg bg-blue-500/10 p-3 text-xs text-blue-600">
              <p className="font-medium mb-1">🛡️ Protection Orders:</p>
              <p>• Stop-Loss: Sell if price drops {stopLossPercent}%</p>
              <p>• Take-Profit: Sell if price rises {takeProfitPercent}%</p>
              <p>• Orders work 24/7 even when agent is offline</p>
            </div>
          </TabsContent>

          <TabsContent value="emergency" className="space-y-4">
            <div className="rounded-lg bg-red-500/10 border border-red-500/20 p-3">
              <div className="flex items-center space-x-2 mb-2">
                <AlertTriangle className="h-4 w-4 text-red-500" />
                <span className="font-medium text-red-600">Emergency Controls</span>
              </div>
              <p className="text-sm text-red-600 mb-3">
                Use these controls only in urgent situations. Actions are immediate and cannot be undone.
              </p>
            </div>

            <Button
              onClick={handleEmergencySell}
              disabled={isEmergencySelling || !isAuthenticated}
              variant="destructive"
              className="w-full flex items-center space-x-2"
            >
              {isEmergencySelling ? (
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-primary-foreground border-t-transparent"></div>
              ) : (
                <TrendingUp className="h-4 w-4 rotate-180" />
              )}
              <span>EMERGENCY SELL ALL {selectedStock}</span>
            </Button>

            <div className="rounded-lg bg-amber-500/10 p-3 text-xs text-amber-600">
              <p className="font-medium mb-1">⚠️ Warning:</p>
              <p>Emergency sell will immediately sell ALL shares of {selectedStock} at current market price. This action cannot be undone.</p>
            </div>
          </TabsContent>
        </Tabs>

        <div className="rounded-lg bg-muted/20 p-3 text-xs text-muted-foreground">
          <p className="font-medium mb-1">🤖 Auto-Trading Features:</p>
          <p>• Analyzes market conditions every 5 minutes</p>
          <p>• Automatically buys on upward predictions</p>
          <p>• Aggressively sells on ANY downward prediction</p>
          <p>• Sets protective orders when stopped</p>
        </div>
      </CardContent>
    </Card>
  );
}