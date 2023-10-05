import React from 'react';
import './App.css';
import AssetBox from './AssetBox';

const App = () => {
  // Sample asset data; you can replace this with actual data later
  const assets = ['Asset 1', 'Asset 2', 'Asset 3'];

  return (
    <div className="App">
      <header className="App-header">
        {/* Header Content */}
      </header>
      <div className="App-main">
        <div className="App-window" id="left-window">
          {assets.map((asset, index) => (
            <AssetBox key={index} title={asset} />
          ))}
        </div>
        <div className="App-window" id="right-window">
          {/* Right Window Content */}
        </div>
      </div>
    </div>
  );
};

export default App;
