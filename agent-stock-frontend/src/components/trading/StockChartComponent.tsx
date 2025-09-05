import { useEffect, useRef, useState, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { TrendingUp, Search, BarChart3 } from 'lucide-react';
import { api, StockDataPoint } from '@/lib/api';

interface StockData {
  time: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume?: number;
}

export function StockChartComponent() {
  const [ticker, setTicker] = useState('AAPL');
  const [inputTicker, setInputTicker] = useState('AAPL');
  const [timeframe, setTimeframe] = useState('1D');
  const [loading, setLoading] = useState(false);
  const [stockData, setStockData] = useState<StockData[]>([]);
  const [currentPrice, setCurrentPrice] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fetchStockData = useCallback(async (symbol: string, tf: string) => {
    setLoading(true);
    setError(null);
    try {
      const data: StockDataPoint[] = await api.getStockData(symbol);
      
      // Convert API data to StockData format
      const convertedData: StockData[] = data.map((point, index) => {
        const close = point.Close;
        // For simplification, we'll use close price for all OHLC values
        // In a real implementation, you'd get full OHLC data from the API
        const variance = close * 0.01; // 1% variance for mock OHLC
        return {
          time: point.Date,
          open: close + (Math.random() - 0.5) * variance,
          high: close + Math.random() * variance,
          low: close - Math.random() * variance,
          close: close,
          volume: Math.floor(Math.random() * 1000000),
        };
      });
      
      setStockData(convertedData);
      if (convertedData.length > 0) {
        setCurrentPrice(convertedData[convertedData.length - 1].close);
      }
    } catch (error) {
      console.error('Failed to fetch stock data:', error);
      setError(error instanceof Error ? error.message : 'Failed to fetch stock data');
      
      // Fallback to mock data if API fails
      const mockData = generateMockData();
      setStockData(mockData);
      setCurrentPrice(mockData[mockData.length - 1].close);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchStockData(ticker, timeframe);
  }, [ticker, timeframe, fetchStockData]);

  const generateMockData = (): StockData[] => {
    const data: StockData[] = [];
    let price = 150;
    const now = new Date();
    
    for (let i = 30; i >= 0; i--) {
      const date = new Date(now.getTime() - i * 24 * 60 * 60 * 1000);
      const open = price + (Math.random() - 0.5) * 10;
      const close = open + (Math.random() - 0.5) * 15;
      const high = Math.max(open, close) + Math.random() * 5;
      const low = Math.min(open, close) - Math.random() * 5;
      
      data.push({
        time: date.toISOString().split('T')[0],
        open: Number(open.toFixed(2)),
        high: Number(high.toFixed(2)),
        low: Number(low.toFixed(2)),
        close: Number(close.toFixed(2)),
        volume: Math.floor(Math.random() * 1000000),
      });
      
      price = close;
    }
    
    return data;
  };

  const handleTickerChange = () => {
    if (inputTicker && inputTicker !== ticker) {
      setTicker(inputTicker.toUpperCase());
    }
  };

  const handleTimeframeChange = (tf: string) => {
    setTimeframe(tf);
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
    }).format(value);
  };

  const getRecentData = () => {
    if (stockData.length === 0) return [];
    return stockData.slice(-10); // Get last 10 data points
  };

  const getPriceChange = () => {
    if (stockData.length < 2) return { change: 0, percentage: 0 };
    const latest = stockData[stockData.length - 1];
    const previous = stockData[stockData.length - 2];
    const change = latest.close - previous.close;
    const percentage = (change / previous.close) * 100;
    return { change, percentage };
  };

  const priceChange = getPriceChange();

  return (
    <Card className="card-trading h-full">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <TrendingUp className="h-5 w-5 text-primary" />
            <span>Market Analysis</span>
          </div>
          <div className="flex items-center space-x-2">
            <Input
              placeholder="Enter ticker..."
              value={inputTicker}
              onChange={(e) => setInputTicker(e.target.value.toUpperCase())}
              onKeyPress={(e) => e.key === 'Enter' && handleTickerChange()}
              className="w-32"
            />
            <Button 
              size="sm" 
              onClick={handleTickerChange}
              disabled={loading}
              className="transition-smooth"
            >
              <Search className="h-4 w-4" />
            </Button>
          </div>
        </CardTitle>
        <div className="flex items-center space-x-2">
          <span className="text-lg font-bold">{ticker}</span>
          <div className="flex space-x-1">
            {['1D', '5D', '1M', '3M', '1Y'].map((tf) => (
              <Button
                key={tf}
                variant={timeframe === tf ? 'default' : 'outline'}
                size="sm"
                onClick={() => handleTimeframeChange(tf)}
                className="transition-smooth"
              >
                {tf}
              </Button>
            ))}
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {/* Error Display */}
          {error && (
            <div className="p-3 rounded-lg bg-destructive/10 border border-destructive/20 text-destructive">
              <p className="text-sm">{error}</p>
            </div>
          )}

          {/* Price Display */}
          {currentPrice && (
            <div className="flex items-center justify-between border-b border-border pb-3">
              <div>
                <p className="text-2xl font-bold">{formatCurrency(currentPrice)}</p>
                <div className={`flex items-center space-x-1 ${priceChange.change >= 0 ? 'profit' : 'loss'}`}>
                  <span className="font-medium">
                    {priceChange.change >= 0 ? '+' : ''}{formatCurrency(priceChange.change)}
                  </span>
                  <span className="text-sm">
                    ({priceChange.change >= 0 ? '+' : ''}{priceChange.percentage.toFixed(2)}%)
                  </span>
                </div>
              </div>
              <BarChart3 className="h-8 w-8 text-primary" />
            </div>
          )}

          {/* Chart Area */}
          <div className="relative">
            {loading && (
              <div className="absolute inset-0 z-10 flex items-center justify-center bg-background/50 rounded-lg">
                <div className="h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent"></div>
              </div>
            )}
            
            {/* Simple Chart Visualization */}
            <div className="h-[350px] w-full rounded-lg bg-muted/20 border border-border">
              <div className="p-4 h-full">
                <div className="h-full flex items-end space-x-1">
                  {getRecentData().map((data, index) => {
                    const height = ((data.close - Math.min(...getRecentData().map(d => d.low))) / 
                      (Math.max(...getRecentData().map(d => d.high)) - Math.min(...getRecentData().map(d => d.low)))) * 300;
                    const isUp = data.close >= data.open;
                    
                    return (
                      <div key={index} className="flex-1 flex flex-col justify-end">
                        <div className="text-xs text-center mb-1 text-muted-foreground">
                          {formatCurrency(data.close)}
                        </div>
                        <div 
                          className={`w-full rounded-t transition-all duration-300 ${
                            isUp ? 'bg-profit' : 'bg-loss'
                          }`}
                          style={{ height: `${Math.max(height, 10)}px` }}
                        ></div>
                        <div className="text-xs text-center mt-1 text-muted-foreground">
                          {new Date(data.time).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>

            {/* Chart Info */}
            <div className="mt-3 grid grid-cols-4 gap-3 text-sm">
              {stockData.length > 0 && (
                <>
                  <div className="text-center">
                    <p className="text-muted-foreground">Open</p>
                    <p className="font-medium">{formatCurrency(stockData[stockData.length - 1].open)}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-muted-foreground">High</p>
                    <p className="font-medium profit">{formatCurrency(stockData[stockData.length - 1].high)}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-muted-foreground">Low</p>
                    <p className="font-medium loss">{formatCurrency(stockData[stockData.length - 1].low)}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-muted-foreground">Volume</p>
                    <p className="font-medium">{stockData[stockData.length - 1].volume?.toLocaleString() || 'N/A'}</p>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}