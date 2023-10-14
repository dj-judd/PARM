const AssetGridContainer = (props) => {
  const filteredAssets = (!props.selectedCategory || props.selectedCategory === "") 
    ? props.assets 
    : props.assets.filter(asset => asset.category_id === Number(props.selectedCategory));



  console.log('Selected Category: ', props.selectedCategory)
  console.log('Selected Category: ',filteredAssets)

  return React.createElement('div', { className: 'grid-container' },
    filteredAssets.map((asset, index) => 
      React.createElement(AssetBox, { key: index, asset }, null)
    )
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
