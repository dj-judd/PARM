const AssetBoxContainer = () => {
  return (
    React.createElement('div', { id: 'asset-box-container' },
      [
        React.createElement(AssetBox, null, null),
        React.createElement(AssetBox, null, null)
      ]
    )
  );
};

window.AssetBoxContainer = AssetBoxContainer;
