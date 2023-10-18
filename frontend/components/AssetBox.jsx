
// Function to remove unnecessary prefix from image paths
const removePrefix = (path) => {
  const prefix = '/home/dj/src/PARM-Production_Asset_Reservation_Manager/backend/database/data/file_attachments/';
  return path ? path.replace(prefix, '/images/') : null;
};

const AssetBox = (props) => {
  const { asset, selected, onClick, smallImagePath } = props;
  // console.log('Small Image Path:', smallImagePath);
  const manufacturerName = asset.manufacturer_name || 'Unknown';

  const assetBoxClass = selected ? 'asset-box selected' : 'asset-box';
  
  const handleClick = () => {
    if (typeof onClick === 'function') {
      onClick(asset);
    }
  };

  return (
    <div className={assetBoxClass} onClick={handleClick}>
      {smallImagePath ? (
        <img src={removePrefix(smallImagePath)} alt={manufacturerName} />
      ) : (
        <p>{manufacturerName}</p>
      )}
    </div>
  );
};

window.AssetBox = AssetBox;