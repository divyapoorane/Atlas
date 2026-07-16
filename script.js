import React, { useState } from 'react';
import { LayoutDashboard, Wallet, TrendingUp, ShieldCheck, Landmark, Receipt, FileText, Settings, Bot, ArrowUpRight, ArrowDownRight, Bell, Search, ChevronRight } from 'lucide-react';

const AtlasApp = () => {
  const [activeView, setActiveView] = useState('dashboard');

  const menuItems = [
    { id: 'dashboard', icon: LayoutDashboard, label: 'Dashboard' },
    { id: 'profile', icon: Wallet, label: 'Financial Profile' },
    { id: 'budget', icon: Receipt, label: 'Budget Planner' },
    { id: 'investments', icon: TrendingUp, label: 'Investment Planner' },
    { id: 'loans', icon: Landmark, label: 'Loan Analyzer' },
    { id: 'insurance', icon: ShieldCheck, label: 'Insurance' },
    { id: 'finn', icon: Bot, label: 'Finn AI Advisor' },
    { id: 'settings', icon: Settings, label: 'Settings' },
  ];

  const renderContent = () => {
    switch (activeView) {
      case 'dashboard': return <DashboardView />;
      case 'loans': return <LoanAnalyzerView />;
      default: return <div className="p-10 text-slate-400">Section: {activeView.toUpperCase()} - Enterprise Module Loading...</div>;
    }
  };

  return (
    <div className="flex h-screen bg-[#0A0A0A] text-slate-200 font-sans overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 border-r border-slate-800 bg-[#0A0A0A]/50 backdrop-blur-xl flex flex-col">
        <div className="p-6 text-xl font-bold tracking-tighter text-white flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-emerald-500/20 flex items-center justify-center text-emerald-400">A</div>
          ATLAS
        </div>
        <nav className="flex-1 px-4 space-y-1">
          {menuItems.map((item) => (
            <button 
              key={item.id}
              onClick={() => setActiveView(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${activeView === item.id ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'hover:bg-slate-900 text-slate-400'}`}
            >
              <item.icon size={18} />
              <span className="text-sm font-medium">{item.label}</span>
            </button>
          ))}
        </nav>
      </aside>

      {/* Main Panel */}
      <main className="flex-1 overflow-y-auto">
        <header className="h-16 border-b border-slate-800 flex items-center justify-between px-8 bg-[#0A0A0A]/80 backdrop-blur">
          <h2 className="text-lg font-semibold">{activeView.charAt(0).toUpperCase() + activeView.slice(1)}</h2>
          <div className="flex items-center gap-4">
            <Search className="text-slate-500" size={18} />
            <Bell className="text-slate-500" size={18} />
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-emerald-500 to-blue-500"></div>
          </div>
        </header>
        <div className="p-8">
          {renderContent()}
        </div>
      </main>
    </div>
  );
};

const DashboardView = () => (
  <div className="space-y-6">
    <div className="grid grid-cols-4 gap-6">
      {[ { label: 'Net Worth', val: '₹1,24,50,000', change: '+2.4%' }, { label: 'Monthly Income', val: '₹8,50,000', change: '+5.1%' }, { label: 'Total Debt', val: '₹42,00,000', change: '-1.2%' }, { label: 'Health Score', val: '88/100', change: '+2' } ].map((card, i) => (
        <div key={i} className="p-6 rounded-2xl bg-[#121212] border border-slate-800 shadow-xl">
          <p className="text-slate-500 text-xs uppercase tracking-widest mb-2">{card.label}</p>
          <h3 className="text-2xl font-semibold text-white">{card.val}</h3>
          <p className="text-emerald-400 text-xs mt-1">{card.change} vs last month</p>
        </div>
      ))}
    </div>
    <div className="h-64 rounded-2xl bg-[#121212] border border-slate-800 p-6 flex items-center justify-center border-dashed border-slate-700">
        <p className="text-slate-600 italic">Advanced Analytics Chart Integration Point</p>
    </div>
  </div>
);

const LoanAnalyzerView = () => (
    <div className="p-8 bg-[#121212] rounded-2xl border border-slate-800">
        <h3 className="text-xl font-semibold text-white mb-6">Loan Intelligence</h3>
        <div className="border-2 border-dashed border-slate-700 rounded-xl p-12 text-center hover:border-emerald-500/50 transition-colors">
            <p className="text-slate-400">Drag & Drop your Loan Agreement (PDF)</p>
        </div>
    </div>
);

export default AtlasApp;
