const InfoPanel = (props) => {
  const { asset } = props;

  if (!asset) {
    return React.createElement('div', { id: 'info-panel' },
      React.createElement(AssetBox, { asset: {}, className: 'info-panel-asset-box' }, null)
    );
  }

  return React.createElement('div', { id: 'info-panel' },
    [
      asset.large_image_path ? (
        React.createElement('div', { className: 'info-panel-asset-box' },
          React.createElement('img', { src: removePrefix(asset.large_image_path), alt: asset.manufacturer_name || 'Unknown' }, null)
        )
      ) : (
        React.createElement(AssetBox, { asset, className: 'info-panel-asset-box' }, null)
      ),
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
