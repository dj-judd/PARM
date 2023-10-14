const { React, ReactDOM } = window;
const assets = window.assets;
const categories = window.categories;

const App = () => {
  const [selectedAsset, setSelectedAsset] = React.useState(null);
  const [selectedCategory, setSelectedCategory] = React.useState(null);
  const [assetClicked, setAssetClicked] = React.useState(null);

  const handleAssetClick = (asset) => {
    setSelectedAsset(asset);
    setAssetClicked(Math.random());  // set assetClicked to a random number
  };

  return (
    React.createElement('div', { id: 'app' },
      [
        React.createElement(LeftPanel, { assets, categories, onAssetClick: handleAssetClick, selectedAsset, selectedCategory, setSelectedCategory }, null),
        React.createElement(RightPanel, { selectedAsset, assetClicked }, null)

      ]
    )
  );
};

window.App = App;

ReactDOM.render(
  React.createElement(App, null, null),
  document.getElementById('root')
);