const LeftPanel = (props) => {
  const [selectedCategory, setSelectedCategory] = React.useState(null);
  return (
    React.createElement('div', { id: 'left-panel'},
      [
        React.createElement(UpperNavigation, { setSelectedCategory, categories: props.categories }, null),
        React.createElement(AssetGridContainer, { selectedCategory, assets: props.assets }, null)
      ]
    )
  );
};

window.LeftPanel = LeftPanel;
