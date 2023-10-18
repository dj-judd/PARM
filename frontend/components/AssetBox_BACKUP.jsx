const AssetBox = (props) => {
  const { asset, selected, onClick } = props;
  const manufacturerName = asset.manufacturer_name || 'Unknown';

  const assetBoxClass = selected ? 'asset-box selected' : 'asset-box';
  
  const handleClick = () => {
    if (typeof onClick === 'function') {
      onClick(asset);
    }
  };

  return React.createElement('div', { className: assetBoxClass, onClick: handleClick, style: {backgroundImage: `url(${asset.online_item_page})`}}, [
    React.createElement('p', null, asset.model_name),
    // React.createElement('p', null, manufacturerName)
  ]);
};

window.AssetBox = AssetBox;
