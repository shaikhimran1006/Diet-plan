import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Plans from './pages/Plans';
import Progress from './pages/Progress';
import Predictions from './pages/Predictions';
import Settings from './pages/Settings';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/plans" element={<Plans />} />
          <Route path="/progress" element={<Progress />} />
          <Route path="/predictions" element={<Predictions />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
