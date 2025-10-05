import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Utensils, 
  TrendingUp, 
  Settings, 
  Menu, 
  X,
  Heart,
  Brain
} from 'lucide-react';

const Layout = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();

  const navigation = [
    { name: 'Dashboard', href: '/', icon: LayoutDashboard },
    { name: 'Diet Plans', href: '/plans', icon: Utensils },
    { name: 'Progress', href: '/progress', icon: TrendingUp },
    { name: 'Predictions', href: '/predictions', icon: Brain },
    { name: 'Settings', href: '/settings', icon: Settings },
  ];

  const isActive = (path) => {
    if (path === '/' && location.pathname === '/') return true;
    if (path !== '/' && location.pathname.startsWith(path)) return true;
    return false;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile Header */}
      <div className="lg:hidden fixed top-0 left-0 right-0 bg-white border-b border-gray-200 z-30">
        <div className="flex items-center justify-between px-4 py-3">
          <div className="flex items-center gap-2">
            <Heart className="h-6 w-6 text-primary-500" />
            <span className="text-xl font-bold text-gray-800">FitPlanner</span>
          </div>
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
          >
            {sidebarOpen ? (
              <X className="h-6 w-6 text-gray-600" />
            ) : (
              <Menu className="h-6 w-6 text-gray-600" />
            )}
          </button>
        </div>
      </div>

      {/* Sidebar Overlay (Mobile) */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed top-0 left-0 z-50 h-screen w-64 bg-white border-r border-gray-200 transition-transform duration-300 ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        } lg:translate-x-0`}
      >
        {/* Logo */}
        <div className="flex items-center gap-2 px-6 py-5 border-b border-gray-200">
          <Heart className="h-7 w-7 text-primary-500" />
          <span className="text-2xl font-bold text-gray-800">FitPlanner</span>
        </div>

        {/* Navigation */}
        <nav className="px-3 py-6 space-y-1">
          {navigation.map((item) => {
            const Icon = item.icon;
            const active = isActive(item.href);
            
            return (
              <Link
                key={item.name}
                to={item.href}
                onClick={() => setSidebarOpen(false)}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg font-medium transition-all duration-200 ${
                  active
                    ? 'bg-primary-50 text-primary-600'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                <Icon className={`h-5 w-5 ${active ? 'text-primary-600' : 'text-gray-500'}`} />
                <span>{item.name}</span>
              </Link>
            );
          })}
        </nav>

        {/* Footer */}
        <div className="absolute bottom-0 left-0 right-0 p-6 border-t border-gray-200">
          <div className="bg-gradient-to-br from-primary-50 to-secondary-50 rounded-lg p-4">
            <p className="text-sm font-semibold text-gray-800 mb-1">
              Your Health Journey
            </p>
            <p className="text-xs text-gray-600">
              Track your progress and stay motivated!
            </p>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="lg:ml-64 min-h-screen pt-16 lg:pt-0">
        <div className="p-6 lg:p-8">
          {children}
        </div>
      </main>
    </div>
  );
};

export default Layout;
