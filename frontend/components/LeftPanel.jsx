const LeftPanel = () => {
  return (
    React.createElement('div', { id: 'left-panel', style: { overflowY: 'auto' } },
      [
        React.createElement(SearchBar, null, null),
        React.createElement(CategoryStrip, null, null),
        React.createElement(AssetBoxContainer, null, null)
      ]
    )
  );
};

window.LeftPanel = LeftPanel;
