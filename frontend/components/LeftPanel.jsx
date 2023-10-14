const LeftPanel = (props) => {
  const { assets, categories, onAssetClick, selectedAsset, selectedCategory, setSelectedCategory } = props;
  
  return (
    React.createElement('div', { id: 'left-panel'},
      [
        React.createElement(UpperNavigation, { setSelectedCategory, categories }, null),
        React.createElement(AssetGridContainer, { selectedCategory, assets, onAssetClick, selectedAsset }, null)
      ]
    )
  );
};

window.LeftPanel = LeftPanel;
