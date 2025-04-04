import React, { useEffect, useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Card,
  CardContent,
  CircularProgress,
} from '@mui/material';
import { getStats } from '../services/api';
import '../styles/Dashboard.css';

interface DashboardStats {
  totalMarkets: number;
  activeMarkets: number;
  totalVolume: number;
  totalTrades: number;
}

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await getStats();
        setStats(data);
      } catch (err) {
        setError('Failed to load dashboard stats');
        console.error('Error fetching stats:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
    const interval = setInterval(fetchStats, 30000); // Refresh every 30 seconds

    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <Box className="dashboard-loading">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box className="dashboard-error">
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  if (!stats) {
    return (
      <Box className="dashboard-error">
        <Typography color="error">No data available</Typography>
      </Box>
    );
  }

  return (
    <Box className="dashboard-container">
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>

      <div className="stats-grid">
        <Card className="stat-card">
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              Total Markets
            </Typography>
            <Typography variant="h4">
              {stats.totalMarkets.toLocaleString()}
            </Typography>
          </CardContent>
        </Card>

        <Card className="stat-card">
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              Active Markets
            </Typography>
            <Typography variant="h4">
              {stats.activeMarkets.toLocaleString()}
            </Typography>
          </CardContent>
        </Card>

        <Card className="stat-card">
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              Total Volume
            </Typography>
            <Typography variant="h4">
              ${stats.totalVolume.toLocaleString()}
            </Typography>
          </CardContent>
        </Card>

        <Card className="stat-card">
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              Total Trades
            </Typography>
            <Typography variant="h4">
              {stats.totalTrades.toLocaleString()}
            </Typography>
          </CardContent>
        </Card>
      </div>

      <Paper className="chart-section">
        <Typography variant="h6" gutterBottom>
          Trading Activity
        </Typography>
        <Box className="chart-container">
          {/* Chart component will be added here */}
        </Box>
      </Paper>
    </Box>
  );
};

export default Dashboard; 