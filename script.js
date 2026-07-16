const { useState } = React;

function App() {
    return (
        <div className="p-10">
            <h1 className="text-3xl font-bold text-emerald-400">
                Welcome to Atlas
            </h1>
            <p className="mt-4 text-slate-400">
                This app is running directly in the browser!
            </p>
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
