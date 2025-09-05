import { useEffect, useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { TrendingUp, Activity, LogOut, User } from 'lucide-react';
import { useAuth } from '@/components/Auth/AuthContext';
import { api, AccountData } from '@/lib/api';

export function TradingHeader() {
  const { username, logout } = useAuth();
  const [accountData, setAccountData] = useState<AccountData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAccountData = async () => {
      try {
        setError(null);
        const data = await api.getAccount();
        setAccountData(data);
      } catch (error) {
        console.error('Failed to fetch account data:', error);
        setError(error instanceof Error ? error.message : 'Failed to load account data');
      } finally {
        setLoading(false);
      }
    };

    // Only fetch if user is authenticated
    if (username) {
      fetchAccountData();
      // Refresh every 30 seconds
      const interval = setInterval(fetchAccountData, 30000);
      return () => clearInterval(interval);
    } else {
      setLoading(false);
    }
  }, [username]);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
    }).format(value);
  };

  return (
    <header className="border-b border-border bg-gradient-to-r from-card to-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex h-16 items-center justify-between px-6">
        {/* Logo and Title */}
        <div className="flex items-center space-x-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/20 text-primary">
            <Activity className="h-6 w-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight">Autonomous Trading Agent</h1>
            <p className="text-sm text-muted-foreground">Real-time portfolio management</p>
          </div>
        </div>

        {/* Account Summary and User Info */}
        <div className="flex items-center space-x-4">
          {/* User Info */}
          <div className="flex items-center space-x-2">
            <User className="h-4 w-4 text-muted-foreground" />
            <span className="text-sm font-medium">{username}</span>
            <Button
              variant="outline"
              size="sm"
              onClick={logout}
              className="h-8"
            >
              <LogOut className="h-4 w-4 mr-1" />
              Logout
            </Button>
          </div>

          {/* Account Summary */}
          {loading ? (
            <div className="flex items-center space-x-4">
              <div className="h-12 w-32 animate-pulse rounded-lg bg-muted"></div>
              <div className="h-12 w-32 animate-pulse rounded-lg bg-muted"></div>
            </div>
          ) : accountData ? (
            <div className="flex items-center space-x-4">
              <Card className="card-trading px-4 py-2">
                <div className="flex items-center space-x-2">
                  <TrendingUp className="h-4 w-4 text-primary" />
                  <div>
                    <p className="text-xs text-muted-foreground">Cash Balance</p>
                    <p className="font-semibold">{formatCurrency(accountData.cash)}</p>
                  </div>
                </div>
              </Card>
              <Card className="card-trading px-4 py-2">
                <div className="flex items-center space-x-2">
                  <Activity className="h-4 w-4 text-primary" />
                  <div>
                    <p className="text-xs text-muted-foreground">Portfolio Value</p>
                    <p className="font-semibold">{formatCurrency(accountData.portfolio_value)}</p>
                  </div>
                </div>
              </Card>
            </div>
          ) : (
            <div className="text-sm text-destructive">
              {error || 'Failed to load account data'}
            </div>
          )}
        </div>
      </div>
    </header>
  );
}