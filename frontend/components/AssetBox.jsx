const AssetBox = (props) => {
  const { asset } = props;
  const manufacturerName = asset.manufacturer_name || 'Unknown'; // Use the manufacturer_name from the asset object

  return React.createElement('div', { className: 'asset-box', style: {backgroundImage: `url(${asset.online_item_page})`}}, [
    React.createElement('p', null, asset.model_name),
    // React.createElement('p', null, manufacturerName)
  ]);
};

window.AssetBox = AssetBox;
