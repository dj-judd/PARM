const InfoPanel = (props) => {
  const { asset } = props;

  if (!asset) {
    return React.createElement('div', { id: 'info-panel'},
      [
        React.createElement(AssetBox, { asset: {}, className: 'info-panel-asset-box' }, null), // Render empty AssetBox
      ]
    );
  }

  return React.createElement('div', { id: 'info-panel'},
    [
      React.createElement(AssetBox, { asset, className: 'info-panel-asset-box' }, null), // Render full AssetBox
      React.createElement('div', { id: 'info-text' }, 
        [
          React.createElement('p', { id: 'model-name' }, `${asset.model_name}`),
          React.createElement('p', { id: 'manufacturer-name' }, `${asset.manufacturer_name}`),
        ]
      )
    ]
  );
};

window.InfoPanel = InfoPanel;
