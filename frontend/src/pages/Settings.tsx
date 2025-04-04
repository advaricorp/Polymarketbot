import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Switch,
  FormControlLabel,
  Alert,
  Snackbar,
} from '@mui/material';
import '../styles/Settings.css';

interface BotSettings {
  apiKey: string;
  apiSecret: string;
  tradingEnabled: boolean;
  maxPositionSize: number;
  riskLevel: 'low' | 'medium' | 'high';
  notificationsEnabled: boolean;
  notificationEmail: string;
  autoRebalance: boolean;
  rebalanceThreshold: number;
}

const Settings: React.FC = () => {
  const [settings, setSettings] = useState<BotSettings>({
    apiKey: '',
    apiSecret: '',
    tradingEnabled: false,
    maxPositionSize: 1000,
    riskLevel: 'medium',
    notificationsEnabled: true,
    notificationEmail: '',
    autoRebalance: true,
    rebalanceThreshold: 5,
  });

  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success' as 'success' | 'error',
  });

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setSettings((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSwitchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, checked } = event.target;
    setSettings((prev) => ({
      ...prev,
      [name]: checked,
    }));
  };

  const handleSelectChange = (event: any) => {
    const { name, value } = event.target;
    setSettings((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSave = async () => {
    try {
      // TODO: Implement API call to save settings
      setSnackbar({
        open: true,
        message: 'Settings saved successfully',
        severity: 'success',
      });
    } catch (error) {
      setSnackbar({
        open: true,
        message: 'Failed to save settings',
        severity: 'error',
      });
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbar((prev) => ({
      ...prev,
      open: false,
    }));
  };

  return (
    <Box className="settings-container">
      <Typography variant="h4" gutterBottom>
        Bot Settings
      </Typography>

      <Paper className="settings-section">
        <Typography variant="h6" gutterBottom>
          API Configuration
        </Typography>
        <div className="settings-grid">
          <TextField
            name="apiKey"
            label="API Key"
            value={settings.apiKey}
            onChange={handleChange}
            fullWidth
            type="password"
          />
          <TextField
            name="apiSecret"
            label="API Secret"
            value={settings.apiSecret}
            onChange={handleChange}
            fullWidth
            type="password"
          />
        </div>
      </Paper>

      <Paper className="settings-section">
        <Typography variant="h6" gutterBottom>
          Trading Parameters
        </Typography>
        <div className="settings-grid">
          <FormControlLabel
            control={
              <Switch
                checked={settings.tradingEnabled}
                onChange={handleSwitchChange}
                name="tradingEnabled"
              />
            }
            label="Enable Trading"
          />
          <TextField
            name="maxPositionSize"
            label="Max Position Size (USD)"
            type="number"
            value={settings.maxPositionSize}
            onChange={handleChange}
            fullWidth
          />
          <FormControl fullWidth>
            <InputLabel>Risk Level</InputLabel>
            <Select
              name="riskLevel"
              value={settings.riskLevel}
              onChange={handleSelectChange}
              label="Risk Level"
            >
              <MenuItem value="low">Low</MenuItem>
              <MenuItem value="medium">Medium</MenuItem>
              <MenuItem value="high">High</MenuItem>
            </Select>
          </FormControl>
        </div>
      </Paper>

      <Paper className="settings-section">
        <Typography variant="h6" gutterBottom>
          Notifications
        </Typography>
        <div className="settings-grid">
          <FormControlLabel
            control={
              <Switch
                checked={settings.notificationsEnabled}
                onChange={handleSwitchChange}
                name="notificationsEnabled"
              />
            }
            label="Enable Notifications"
          />
          <TextField
            name="notificationEmail"
            label="Notification Email"
            type="email"
            value={settings.notificationEmail}
            onChange={handleChange}
            fullWidth
            disabled={!settings.notificationsEnabled}
          />
        </div>
      </Paper>

      <Paper className="settings-section">
        <Typography variant="h6" gutterBottom>
          Auto Rebalancing
        </Typography>
        <div className="settings-grid">
          <FormControlLabel
            control={
              <Switch
                checked={settings.autoRebalance}
                onChange={handleSwitchChange}
                name="autoRebalance"
              />
            }
            label="Enable Auto Rebalancing"
          />
          <TextField
            name="rebalanceThreshold"
            label="Rebalance Threshold (%)"
            type="number"
            value={settings.rebalanceThreshold}
            onChange={handleChange}
            fullWidth
            disabled={!settings.autoRebalance}
          />
        </div>
      </Paper>

      <Box className="settings-actions">
        <Button
          variant="contained"
          color="primary"
          onClick={handleSave}
          size="large"
        >
          Save Settings
        </Button>
      </Box>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
      >
        <Alert
          onClose={handleCloseSnackbar}
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default Settings; 