import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Brain, TrendingUp, TrendingDown } from 'lucide-react';
import { api, type PredictionResponse } from '@/lib/api';

interface PredictionData {
  ticker: string;
  last_close: number;
  predicted_next_close: number;
  confidence?: number;
}

export function PredictionToolComponent() {
  const [ticker, setTicker] = useState('');
  const [prediction, setPrediction] = useState<PredictionData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handlePredict = async () => {
    if (!ticker.trim()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const data = await api.predictStock(ticker);
      setPrediction(data);
    } catch (error) {
      console.error('Failed to fetch prediction:', error);
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError('Failed to get prediction');
      }
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
    }).format(value);
  };

  const getPredictionChange = () => {
    if (!prediction) return null;
    
    const change = prediction.predicted_next_close - prediction.last_close;
    const changePercent = (change / prediction.last_close) * 100;
    const isPositive = change >= 0;
    
    return {
      change,
      changePercent,
      isPositive,
    };
  };

  const predictionChange = getPredictionChange();

  return (
    <Card className="card-trading">
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Brain className="h-5 w-5 text-primary" />
          <span>ML Prediction Tool</span>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex space-x-2">
          <Input
            placeholder="Enter ticker symbol..."
            value={ticker}
            onChange={(e) => setTicker(e.target.value.toUpperCase())}
            onKeyPress={(e) => e.key === 'Enter' && handlePredict()}
          />
          <Button 
            onClick={handlePredict} 
            disabled={loading || !ticker.trim()}
            className="transition-smooth"
          >
            {loading ? (
              <div className="h-4 w-4 animate-spin rounded-full border-2 border-primary-foreground border-t-transparent"></div>
            ) : (
              'Predict'
            )}
          </Button>
        </div>

        {error && (
          <div className="rounded-lg border border-destructive/20 bg-destructive/10 p-3 text-sm text-destructive">
            {error}
          </div>
        )}

        {prediction && (
          <div className="space-y-3">
            <div className="text-center">
              <h3 className="text-lg font-semibold text-primary">{prediction.ticker}</h3>
              <p className="text-sm text-muted-foreground">Stock Prediction</p>
            </div>
            
            <div className="grid grid-cols-2 gap-3">
              <div className="rounded-lg bg-muted/50 p-3">
                <p className="text-xs font-medium text-muted-foreground">Last Close</p>
                <p className="text-lg font-bold">{formatCurrency(prediction.last_close)}</p>
              </div>
              <div className="rounded-lg bg-muted/50 p-3">
                <p className="text-xs font-medium text-muted-foreground">Predicted Close</p>
                <p className="text-lg font-bold">{formatCurrency(prediction.predicted_next_close)}</p>
              </div>
            </div>

            {predictionChange && (
              <div className={`flex items-center justify-center space-x-2 rounded-lg p-3 ${
                predictionChange.isPositive ? 'bg-profit/10 text-profit' : 'bg-loss/10 text-loss'
              }`}>
                {predictionChange.isPositive ? (
                  <TrendingUp className="h-4 w-4" />
                ) : (
                  <TrendingDown className="h-4 w-4" />
                )}
                <span className="font-medium">
                  {predictionChange.isPositive ? '+' : ''}{formatCurrency(predictionChange.change)}
                </span>
                <span className="text-sm">
                  ({predictionChange.isPositive ? '+' : ''}{predictionChange.changePercent.toFixed(2)}%)
                </span>
              </div>
            )}

            {prediction.confidence && (
              <div className="text-center">
                <p className="text-xs text-muted-foreground">Confidence</p>
                <div className="mt-1 h-2 w-full rounded-full bg-muted">
                  <div 
                    className="h-2 rounded-full bg-primary transition-all duration-500"
                    style={{ width: `${prediction.confidence * 100}%` }}
                  ></div>
                </div>
                <p className="mt-1 text-sm font-medium">{(prediction.confidence * 100).toFixed(1)}%</p>
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}