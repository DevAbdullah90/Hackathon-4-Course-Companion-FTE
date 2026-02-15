import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Lesson from './pages/Lesson';
import Login from './pages/Login';
import Register from './pages/Register';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-background font-sans antialiased">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<Dashboard />} />
          <Route path="/course/:slug" element={<Dashboard />} /> {/* Simplified for now */}
          <Route path="/lesson/:slug" element={<Lesson />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
