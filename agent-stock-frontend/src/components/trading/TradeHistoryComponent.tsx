import { useEffect, useState, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Clock, ArrowUpCircle, ArrowDownCircle, AlertCircle, RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { api, Trade } from '@/lib/api';

export function TradeHistoryComponent() {
  const [trades, setTrades] = useState<Trade[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);
  const [refreshing, setRefreshing] = useState(false);

  const fetchTrades = useCallback(async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      setError('Please log in to view your trade history');
      setLoading(false);
      return;
    }

    try {
      setError(null);
      const data = await api.getTrades();
      setTrades(data.slice(0, 20)); // Get latest 20 trades
      setLastUpdate(new Date());
    } catch (error) {
      console.error('Failed to fetch trades:', error);
      setError(error instanceof Error ? error.message : 'Failed to fetch trades');
      
      // Fallback to mock data for demo purposes
      const mockTrades: Trade[] = [
        {
          timestamp: new Date(Date.now() - 3600000).toISOString(),
          ticker: 'AAPL',
          side: 'BUY',
          quantity: 10,
          price: 150.25
        },
        {
          timestamp: new Date(Date.now() - 7200000).toISOString(),
          ticker: 'GOOGL',
          side: 'SELL',
          quantity: 5,
          price: 2750.50
        },
        {
          timestamp: new Date(Date.now() - 10800000).toISOString(),
          ticker: 'MSFT',
          side: 'BUY',
          quantity: 15,
          price: 300.75
        }
      ];
      setTrades(mockTrades);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('token');
    setIsAuthenticated(!!token);
    
    fetchTrades();
    
    // Refresh every 30 seconds if authenticated
    if (token) {
      const interval = setInterval(fetchTrades, 30000);
      return () => clearInterval(interval);
    }
  }, [fetchTrades]);

  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchTrades();
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
    }).format(value);
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getTotalValue = (trade: Trade) => {
    return trade.quantity * trade.price;
  };

  const getSideBadge = (side: 'BUY' | 'SELL') => {
    const isBuy = side === 'BUY';
    return (
      <Badge 
        variant={isBuy ? 'default' : 'destructive'}
        className={`${isBuy ? 'buy-order' : 'sell-order'} flex items-center space-x-1`}
      >
        {isBuy ? (
          <ArrowUpCircle className="h-3 w-3" />
        ) : (
          <ArrowDownCircle className="h-3 w-3" />
        )}
        <span>{side}</span>
      </Badge>
    );
  };

  return (
    <Card className="card-trading">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Clock className="h-5 w-5 text-primary" />
            <span>Recent Trades</span>
          </div>
          <div className="flex items-center space-x-2">
            {lastUpdate && (
              <span className="text-xs text-muted-foreground">
                Updated {lastUpdate.toLocaleTimeString()}
              </span>
            )}
            <Button
              variant="outline"
              size="sm"
              onClick={handleRefresh}
              disabled={refreshing || !isAuthenticated}
              className="transition-smooth"
            >
              <RefreshCw className={`h-4 w-4 ${refreshing ? 'animate-spin' : ''}`} />
            </Button>
          </div>
        </CardTitle>
      </CardHeader>
      <CardContent>
        {/* Error Display */}
        {error && (
          <div className="mb-4 p-3 rounded-lg bg-destructive/10 border border-destructive/20 text-destructive flex items-center space-x-2">
            <AlertCircle className="h-4 w-4" />
            <p className="text-sm">{error}</p>
          </div>
        )}

        {/* Authentication Warning */}
        {!isAuthenticated && (
          <div className="p-4 rounded-lg bg-muted/50 border border-border text-center">
            <AlertCircle className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
            <p className="text-muted-foreground">Please log in to view your trade history</p>
          </div>
        )}

        {loading && isAuthenticated ? (
          <div className="space-y-3">
            {[...Array(8)].map((_, i) => (
              <div key={i} className="flex justify-between">
                <div className="h-4 w-20 animate-pulse rounded bg-muted"></div>
                <div className="h-4 w-16 animate-pulse rounded bg-muted"></div>
                <div className="h-4 w-12 animate-pulse rounded bg-muted"></div>
                <div className="h-4 w-16 animate-pulse rounded bg-muted"></div>
                <div className="h-4 w-20 animate-pulse rounded bg-muted"></div>
                <div className="h-4 w-24 animate-pulse rounded bg-muted"></div>
              </div>
            ))}
          </div>
        ) : isAuthenticated ? (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Time</TableHead>
                <TableHead>Ticker</TableHead>
                <TableHead>Side</TableHead>
                <TableHead className="text-right">Qty</TableHead>
                <TableHead className="text-right">Price</TableHead>
                <TableHead className="text-right">Total</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {trades.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} className="text-center text-muted-foreground">
                    No trades found
                  </TableCell>
                </TableRow>
              ) : (
                trades.map((trade, index) => (
                  <TableRow key={trade._id || index} className="transition-smooth hover:bg-muted/50">
                    <TableCell className="text-sm text-muted-foreground">
                      {formatTimestamp(trade.timestamp)}
                    </TableCell>
                    <TableCell className="font-medium">{trade.ticker}</TableCell>
                    <TableCell>{getSideBadge(trade.side)}</TableCell>
                    <TableCell className="text-right">{trade.quantity}</TableCell>
                    <TableCell className="text-right">{formatCurrency(trade.price)}</TableCell>
                    <TableCell className="text-right font-medium">
                      {formatCurrency(getTotalValue(trade))}
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        ) : null}

        {/* Trade Summary */}
        {isAuthenticated && trades.length > 0 && (
          <div className="mt-4 pt-4 border-t border-border">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
              <div className="text-center">
                <p className="text-muted-foreground">Total Trades</p>
                <p className="text-lg font-bold">{trades.length}</p>
              </div>
              <div className="text-center">
                <p className="text-muted-foreground">Buy Orders</p>
                <p className="text-lg font-bold text-green-600">
                  {trades.filter(t => t.side === 'BUY').length}
                </p>
              </div>
              <div className="text-center">
                <p className="text-muted-foreground">Sell Orders</p>
                <p className="text-lg font-bold text-red-600">
                  {trades.filter(t => t.side === 'SELL').length}
                </p>
              </div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}