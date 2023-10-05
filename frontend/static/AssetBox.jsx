import React from 'react';
import './AssetBox.css';

const AssetBox = ({ title }) => {
  return (
    <div className="asset-box">
      <h3>{title}</h3>
      {/* Additional content here */}
    </div>
  );
};

export default AssetBox;
