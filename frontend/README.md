# Polymarketbot Frontend

This is the frontend application for the Polymarketbot, a trading bot for Polymarket prediction markets.

## Features

- Dashboard with real-time statistics and charts
- Market listing and detailed market views
- Bot configuration and settings
- Real-time event monitoring

## Technologies Used

- React with TypeScript
- Material-UI for components
- Chart.js for data visualization
- React Router for navigation

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Clone the repository
2. Navigate to the frontend directory:
   ```
   cd Polymarketbot/frontend
   ```
3. Install dependencies:
   ```
   npm install
   ```
   or
   ```
   yarn install
   ```

### Development

To start the development server:

```
npm start
```

or

```
yarn start
```

This will start the development server at [http://localhost:3000](http://localhost:3000).

### Building for Production

To build the application for production:

```
npm run build
```

or

```
yarn build
```

This will create a production build in the `build` directory.

## Project Structure

- `src/components`: Reusable UI components
- `src/pages`: Page components
- `src/services`: API services and utilities
- `src/utils`: Helper functions and utilities
- `src/types`: TypeScript type definitions

## API Integration

The frontend communicates with the backend API at `http://localhost:8001`. Make sure the backend server is running before starting the frontend application.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
