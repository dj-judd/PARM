const RightPanel = (props) => {
  const { assetClicked, selectedAsset } = props;
  
  return (
    React.createElement('div', { id: 'right-panel'},
      [
        React.createElement(InfoPanel, { asset: selectedAsset }, null),
        React.createElement(Reservation, { assetClicked }, null),
      ]
    )
  );
};

window.RightPanel = RightPanel;
