const AssetGridContainer = (props) => {
  const { selectedCategory, assets, onAssetClick, selectedAsset } = props;

    console.log('Assets:', props.assets);
    console.group("Category Selection");
    console.log("%cSelected Category ID: " + props.selectedCategory, "color: green; font-size: 16px;");
    console.groupEnd();
    console.log(filteredAssets)

    console.log('Type of selectedCategory:', typeof props.selectedCategory);
    console.log('Type of first asset\'s category_id:', typeof props.assets[0].category_id);

    // console.log('Assets:', assets);

    console.log('Assets in AssetGridContainer:', assets);


  
  const filteredAssets = (!selectedCategory || selectedCategory === "") 
    ? assets 
    : assets.filter(asset => asset.category_id === Number(selectedCategory));

  return (
    <div className="asset-grid-container">
      {assets.map((asset) => (
        <AssetBox 
          key={asset.id} 
          asset={asset} 
          smallImagePath={asset.small_image_path}  // Pass down the small image path
          onClick={() => onAssetClick(asset)}
          selected={selectedAsset && selectedAsset.id === asset.id}
        />
      ))}
      {/* <InfoPanel asset={selectedAsset} largeImagePath={selectedAsset ? selectedAsset.large_image_path : null} /> */}
    </div>
  );
};

window.AssetGridContainer = AssetGridContainer;



// Debuggin VERSION
// const AssetGridContainer = (props) => {
//   console.log('Assets:', props.assets);
//   console.group("Category Selection");
//   console.log("%cSelected Category ID: " + props.selectedCategory, "color: green; font-size: 16px;");
//   console.groupEnd();
//   console.log(filteredAssets)

//   console.log('Type of selectedCategory:', typeof props.selectedCategory);
//   console.log('Type of first asset\'s category_id:', typeof props.assets[0].category_id);

//   const filteredAssets = props.assets.filter(asset => asset.category_id === props.selectedCategory);
//   console.log('Filtered Assets:', filteredAssets);

//   return React.createElement('div', { className: 'grid-container' },
//     filteredAssets.map((asset, index) => 
//       React.createElement(AssetBox, { key: index, asset }, null)
//     )
//   );
// };

// window.AssetGridContainer = AssetGridContainer;
