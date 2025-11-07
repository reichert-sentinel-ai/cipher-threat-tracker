import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ThreatTimeline from './components/ThreatTimeline.jsx';
import IOCSearch from './components/IOCSearch.jsx';
import MitreAttackMap from './components/MitreAttackMap.jsx';
import IRPlaybookGenerator from './components/IRPlaybookGenerator.jsx';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50 dark:bg-[#0f0f0f] transition-colors">
        <nav className="bg-white dark:bg-[#1a1a1a] shadow-sm border-b border-gray-200 dark:border-[#2a2a2a]">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex">
                <div className="flex-shrink-0 flex items-center">
                  <h1 className="text-xl font-bold text-gray-900 dark:text-[#e5e5e5]">
                    🛡️ Cipher Threat Intelligence
                  </h1>
                </div>
                <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                  <Link
                    to="/threat-timeline"
                    className="border-transparent text-gray-500 dark:text-[#a0a0a0] hover:border-gray-300 dark:hover:border-[#2a2a2a] hover:text-gray-700 dark:hover:text-[#e5e5e5] inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
                  >
                    Threat Timeline
                  </Link>
                  <Link
                    to="/ioc-search"
                    className="border-transparent text-gray-500 dark:text-[#a0a0a0] hover:border-gray-300 dark:hover:border-[#2a2a2a] hover:text-gray-700 dark:hover:text-[#e5e5e5] inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
                  >
                    IOC Search
                  </Link>
                  <Link
                    to="/mitre-attack"
                    className="border-transparent text-gray-500 dark:text-[#a0a0a0] hover:border-gray-300 dark:hover:border-[#2a2a2a] hover:text-gray-700 dark:hover:text-[#e5e5e5] inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
                  >
                    MITRE ATT&CK
                  </Link>
                  <Link
                    to="/ir-playbooks"
                    className="border-transparent text-gray-500 dark:text-[#a0a0a0] hover:border-gray-300 dark:hover:border-[#2a2a2a] hover:text-gray-700 dark:hover:text-[#e5e5e5] inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
                  >
                    IR Playbooks
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </nav>

        <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8 bg-transparent text-gray-900 dark:text-[#e5e5e5]">
          <Routes>
            <Route path="/" element={
              <div className="px-4 py-8">
                <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-[#e5e5e5]">Welcome to Cipher</h2>
                <p className="text-gray-600 dark:text-[#a0a0a0] mb-4">
                  Cyber threat detection, attribution, and incident response platform.
                </p>
                <Link
                  to="/threat-timeline"
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 transition-colors"
                >
                  View Threat Timeline
                </Link>
              </div>
            } />
            <Route path="/threat-timeline" element={<ThreatTimeline />} />
            <Route path="/ioc-search" element={<IOCSearch />} />
            <Route path="/mitre-attack" element={<MitreAttackMap />} />
            <Route path="/ir-playbooks" element={<IRPlaybookGenerator />} />
            <Route path="*" element={
              <div className="px-4 py-8">
                <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-[#e5e5e5]">Page Not Found</h2>
                <p className="text-gray-600 dark:text-[#a0a0a0] mb-4">
                  The page you're looking for doesn't exist.
                </p>
                <Link
                  to="/"
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700"
                >
                  Go Home
                </Link>
              </div>
            } />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;

