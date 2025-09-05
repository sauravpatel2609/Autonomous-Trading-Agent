import { useAuth, AuthPage, UserProfile } from '@/components/Auth';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { User, UserPlus } from 'lucide-react';

export function AuthDemo() {
  const { isAuthenticated, username, logout, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-center">Authentication Required</CardTitle>
          </CardHeader>
          <CardContent className="text-center space-y-4">
            <p className="text-muted-foreground">
              Please sign in or create an account to access the trading platform.
            </p>
            <div className="flex justify-center space-x-4">
              <Button variant="outline" className="flex items-center space-x-2">
                <User className="h-4 w-4" />
                <span>Sign In</span>
              </Button>
              <Button className="flex items-center space-x-2">
                <UserPlus className="h-4 w-4" />
                <span>Sign Up</span>
              </Button>
            </div>
          </CardContent>
        </Card>
        
        <AuthPage 
          onAuthSuccess={() => {
            // Handle successful authentication
            console.log('Authentication successful!');
          }}
          defaultMode="login"
        />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="text-center text-green-600">Welcome to the Trading Platform!</CardTitle>
        </CardHeader>
        <CardContent className="text-center">
          <p className="text-muted-foreground">
            You are successfully logged in as <strong>{username}</strong>. 
            You now have access to all trading features.
          </p>
        </CardContent>
      </Card>

      <div className="flex justify-center">
        <UserProfile 
          username={username || 'User'}
          onLogout={logout}
        />
      </div>
    </div>
  );
}
