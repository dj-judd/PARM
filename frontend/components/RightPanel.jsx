const RightPanel = (props) => {
  const { selectedAsset } = props;
  
  return (
    React.createElement('div', { id: 'right-panel'},
      [
        React.createElement(InfoPanel, { asset: selectedAsset }, null),
        React.createElement(Flags, null, null),
        React.createElement(Reservations, null, null)
      ]
    )
  );
};

window.RightPanel = RightPanel;
