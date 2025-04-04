import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Chip,
  CircularProgress,
} from '@mui/material';

interface Market {
  id: string;
  title: string;
  volume: number;
  status: string;
  resolution: string | null;
  endDate: string;
}

const Markets: React.FC = () => {
  const navigate = useNavigate();
  const [markets, setMarkets] = useState<Market[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  useEffect(() => {
    const fetchMarkets = async () => {
      try {
        const response = await fetch('http://localhost:8001/api/markets');
        const data = await response.json();
        setMarkets(data.markets || []);
      } catch (error) {
        console.error('Error fetching markets:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchMarkets();
    const interval = setInterval(fetchMarkets, 60000); // Update every minute

    return () => clearInterval(interval);
  }, []);

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleRowClick = (marketId: string) => {
    navigate(`/markets/${marketId}`);
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active':
        return 'success';
      case 'resolved':
        return 'info';
      case 'cancelled':
        return 'error';
      default:
        return 'default';
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Markets
      </Typography>

      <Paper sx={{ width: '100%', mb: 2 }}>
        <TableContainer>
          <Table sx={{ minWidth: 750 }} aria-labelledby="tableTitle">
            <TableHead>
              <TableRow>
                <TableCell>Title</TableCell>
                <TableCell align="right">Volume</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Resolution</TableCell>
                <TableCell>End Date</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {markets
                .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                .map((market) => (
                  <TableRow
                    hover
                    onClick={() => handleRowClick(market.id)}
                    key={market.id}
                    sx={{ cursor: 'pointer' }}
                  >
                    <TableCell component="th" scope="row">
                      {market.title}
                    </TableCell>
                    <TableCell align="right">
                      ${market.volume.toLocaleString()}
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={market.status}
                        color={getStatusColor(market.status) as any}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>{market.resolution || 'Pending'}</TableCell>
                    <TableCell>{new Date(market.endDate).toLocaleDateString()}</TableCell>
                  </TableRow>
                ))}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={markets.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </Paper>
    </Box>
  );
};

export default Markets; 