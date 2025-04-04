import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import {
  Box,
  Typography,
  Paper,
  Card,
  CardContent,
  CircularProgress,
  Divider,
} from '@mui/material';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { getMarketDetails, getMarketEvents } from '../services/api';
import '../styles/MarketDetail.css';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface MarketDetails {
  id: string;
  title: string;
  description: string;
  currentPrice: number;
  volume24h: number;
  trades24h: number;
  openInterest: number;
  resolutionDate: string;
  status: string;
}

interface MarketEvent {
  id: string;
  type: string;
  price: number;
  amount: number;
  timestamp: string;
}

const MarketDetail: React.FC = () => {
  const { marketId } = useParams<{ marketId: string }>();
  const [market, setMarket] = useState<MarketDetails | null>(null);
  const [events, setEvents] = useState<MarketEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      if (!marketId) {
        setError('Market ID is required');
        setLoading(false);
        return;
      }

      try {
        const [marketData, eventsData] = await Promise.all([
          getMarketDetails(marketId),
          getMarketEvents(marketId),
        ]);
        setMarket(marketData);
        setEvents(eventsData);
      } catch (err) {
        setError('Failed to load market data');
        console.error('Error fetching market data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 30000); // Refresh every 30 seconds

    return () => clearInterval(interval);
  }, [marketId]);

  // Sample data for the price chart
  const chartData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Yes Price',
        data: [0.6, 0.65, 0.7, 0.75, 0.8, 0.85],
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
      {
        label: 'No Price',
        data: [0.4, 0.35, 0.3, 0.25, 0.2, 0.15],
        borderColor: 'rgb(255, 99, 132)',
        tension: 0.1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Price History',
      },
    },
    scales: {
      y: {
        min: 0,
        max: 1,
      },
    },
  };

  if (loading) {
    return (
      <Box className="market-detail-loading">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box className="market-detail-error">
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  if (!market) {
    return (
      <Box className="market-detail-error">
        <Typography color="error">Market not found</Typography>
      </Box>
    );
  }

  return (
    <Box className="market-detail-container">
      <Typography variant="h4" gutterBottom className="market-detail-title">
        {market.title}
      </Typography>

      <div className="market-detail-grid">
        <Paper className="market-detail-overview">
          <Typography variant="h6" gutterBottom>
            Market Overview
          </Typography>
          <Typography variant="body1" paragraph>
            {market.description}
          </Typography>
          <Divider />
          <div className="market-stats">
            <div className="market-stat">
              <Typography color="textSecondary">Current Price</Typography>
              <Typography variant="h5">${market.currentPrice.toFixed(2)}</Typography>
            </div>
            <div className="market-stat">
              <Typography color="textSecondary">24h Volume</Typography>
              <Typography variant="h5">${market.volume24h.toLocaleString()}</Typography>
            </div>
            <div className="market-stat">
              <Typography color="textSecondary">24h Trades</Typography>
              <Typography variant="h5">{market.trades24h}</Typography>
            </div>
            <div className="market-stat">
              <Typography color="textSecondary">Open Interest</Typography>
              <Typography variant="h5">${market.openInterest.toLocaleString()}</Typography>
            </div>
          </div>
        </Paper>

        <Paper className="market-detail-chart">
          <Typography variant="h6" gutterBottom>
            Price Chart
          </Typography>
          <Box className="chart-container">
            <Line data={chartData} options={chartOptions} />
          </Box>
        </Paper>
      </div>

      <Paper className="market-events">
        <Typography variant="h6" gutterBottom>
          Recent Events
        </Typography>
        <div className="events-list">
          {events.map((event) => (
            <Card key={event.id} className="event-card">
              <CardContent>
                <Typography variant="subtitle1">
                  {event.type} - ${event.price.toFixed(2)}
                </Typography>
                <Typography color="textSecondary">
                  Amount: {event.amount} | {new Date(event.timestamp).toLocaleString()}
                </Typography>
              </CardContent>
            </Card>
          ))}
        </div>
      </Paper>
    </Box>
  );
};

export default MarketDetail;