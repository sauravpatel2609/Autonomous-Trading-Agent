import { TradingHeader } from '@/components/trading/TradingHeader';
import { PortfolioComponent } from '@/components/trading/PortfolioComponent';
import { TradeHistoryComponent } from '@/components/trading/TradeHistoryComponent';
import { StockChartComponent } from '@/components/trading/StockChartComponent';
import { PredictionToolComponent } from '@/components/trading/PredictionToolComponent';
import { AgentStatusComponent } from '@/components/trading/AgentStatusComponent';
import { AgentControlComponent } from '@/components/trading/AgentControlComponent';
import { AuthPage, useAuth } from '@/components/Auth';

export default function TradingDashboard() {
  const { isAuthenticated, loading } = useAuth();

  // Show loading spinner while checking authentication
  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="flex flex-col items-center space-y-4">
          <div className="h-12 w-12 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  // Show authentication page if not logged in
  if (!isAuthenticated) {
    return (
      <AuthPage 
        onAuthSuccess={() => {
          // The auth context will handle the state update
          console.log('User authenticated successfully');
        }}
        defaultMode="login"
      />
    );
  }

  // Show the trading dashboard for authenticated users
  return (
    <div className="min-h-screen bg-background">
      <TradingHeader />
      
      <main className="container mx-auto p-6">
        <div className="grid grid-cols-12 gap-6 h-[calc(100vh-140px)]">
          {/* Left Column - Portfolio & Trades (30% width) */}
          <div className="col-span-12 lg:col-span-4 xl:col-span-3 space-y-6">
            <PortfolioComponent />
            <TradeHistoryComponent />
          </div>

          {/* Center Column - Market Analysis (45% width) */}
          <div className="col-span-12 lg:col-span-8 xl:col-span-6">
            <StockChartComponent />
          </div>

          {/* Right Column - Agent Command & Control (25% width) */}
          <div className="col-span-12 xl:col-span-3 space-y-6">
            <PredictionToolComponent />
            <AgentStatusComponent />
            <AgentControlComponent />
          </div>
        </div>
      </main>
    </div>
  );
}