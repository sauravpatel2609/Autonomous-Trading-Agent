import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { TrendingUp, TrendingDown, AlertCircle } from 'lucide-react';
import { api, PortfolioPosition } from '@/lib/api';

interface Position extends PortfolioPosition {
  unrealized_pl?: number;
}

export function PortfolioComponent() {
  const [positions, setPositions] = useState<Position[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('token');
    setIsAuthenticated(!!token);
    
    const fetchPortfolio = async () => {
      if (!token) {
        setError('Please log in to view your portfolio');
        setLoading(false);
        return;
      }

      setLoading(true);
      setError(null);
      try {
        const data = await api.getPortfolio();
        setPositions(data);
      } catch (error) {
        console.error('Failed to fetch portfolio:', error);
        setError(error instanceof Error ? error.message : 'Failed to fetch portfolio');
        
        // Fallback to mock data for demo purposes
        const mockPositions: Position[] = [
          { symbol: 'AAPL', quantity: 10, market_value: 1500.50, unrealized_pl: 150.25 },
          { symbol: 'GOOGL', quantity: 5, market_value: 2750.75, unrealized_pl: -25.50 },
          { symbol: 'MSFT', quantity: 8, market_value: 2400.00, unrealized_pl: 75.00 },
        ];
        setPositions(mockPositions);
      } finally {
        setLoading(false);
      }
    };

    fetchPortfolio();
    
    // Refresh every 30 seconds if authenticated
    if (token) {
      const interval = setInterval(fetchPortfolio, 30000);
      return () => clearInterval(interval);
    }
  }, []);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
    }).format(value);
  };

  const formatPL = (value?: number) => {
    if (value === undefined) {
      return <span className="text-muted-foreground">N/A</span>;
    }
    
    const isProfit = value >= 0;
    return (
      <div className={`flex items-center space-x-1 ${isProfit ? 'profit' : 'loss'}`}>
        {isProfit ? (
          <TrendingUp className="h-3 w-3" />
        ) : (
          <TrendingDown className="h-3 w-3" />
        )}
        <span className="font-medium">{formatCurrency(Math.abs(value))}</span>
      </div>
    );
  };

  const getTotalValue = () => {
    return positions.reduce((sum, pos) => sum + pos.market_value, 0);
  };

  const getTotalPL = () => {
    return positions.reduce((sum, pos) => sum + (pos.unrealized_pl || 0), 0);
  };

  return (
    <Card className="card-trading">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <TrendingUp className="h-5 w-5 text-primary" />
            <span>Portfolio Positions</span>
          </div>
          {isAuthenticated && positions.length > 0 && (
            <div className="text-sm text-muted-foreground">
              Total: {formatCurrency(getTotalValue())}
            </div>
          )}
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
            <p className="text-muted-foreground">Please log in to view your portfolio positions</p>
          </div>
        )}

        {loading && isAuthenticated ? (
          <div className="space-y-3">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="flex justify-between">
                <div className="h-4 w-16 animate-pulse rounded bg-muted"></div>
                <div className="h-4 w-20 animate-pulse rounded bg-muted"></div>
                <div className="h-4 w-24 animate-pulse rounded bg-muted"></div>
                <div className="h-4 w-20 animate-pulse rounded bg-muted"></div>
              </div>
            ))}
          </div>
        ) : isAuthenticated ? (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Symbol</TableHead>
                <TableHead className="text-right">Quantity</TableHead>
                <TableHead className="text-right">Market Value</TableHead>
                <TableHead className="text-right">Unrealized P/L</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {positions.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={4} className="text-center text-muted-foreground">
                    No positions found
                  </TableCell>
                </TableRow>
              ) : (
                positions.map((position) => (
                  <TableRow key={position.symbol} className="transition-smooth hover:bg-muted/50">
                    <TableCell className="font-medium">{position.symbol}</TableCell>
                    <TableCell className="text-right">{position.quantity}</TableCell>
                    <TableCell className="text-right">{formatCurrency(position.market_value)}</TableCell>
                    <TableCell className="text-right">{formatPL(position.unrealized_pl)}</TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        ) : null}

        {/* Portfolio Summary */}
        {isAuthenticated && positions.length > 0 && (
          <div className="mt-4 pt-4 border-t border-border">
            <div className="flex justify-between items-center">
              <span className="font-medium">Total Portfolio Value:</span>
              <span className="text-lg font-bold">{formatCurrency(getTotalValue())}</span>
            </div>
            <div className="flex justify-between items-center mt-2">
              <span className="font-medium">Total P/L:</span>
              <div>{formatPL(getTotalPL())}</div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}