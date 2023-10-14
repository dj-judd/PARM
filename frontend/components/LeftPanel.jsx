const LeftPanel = () => {
  return (
    React.createElement('div', { id: 'left-panel'},
      [
        React.createElement(UpperNavigation, null, null),
        React.createElement(CategoryStrip, null, null),
        React.createElement(AssetBoxContainer, null, null)
      ]
    )
  );
};

window.LeftPanel = LeftPanel;
