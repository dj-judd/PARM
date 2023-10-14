function CategoryDropdown(props) {
    const categories = props.categories;
      
    // Indenting the sub-categories for the dropdown list.
    function renderOptions(tree, indent = 0) {
      const nbsp = "\u00A0".repeat(indent * 5);  // 4 spaces per indentation level
      
      return Object.keys(tree).map((id) => (
        <React.Fragment key={id}>
          <option value={id}>
            {nbsp}{tree[id].name}
          </option>
          {tree[id].children.length > 0 && renderOptions(tree[id].children, indent + 1)}
        </React.Fragment>
      ));
    }

    function handleCategoryChange(event) {
      const selectedCategoryId = event.target.value;
      // console.log('Type of selectedCategoryId:', typeof selectedCategoryId);
      // console.log('Value of selectedCategoryId:', selectedCategoryId);
      props.setSelectedCategory(selectedCategoryId);
    }
  
    return (
      <select className="custom-dropdown" onChange={handleCategoryChange}>
        <option value="">Select Category</option>  {/* Set value to an empty string */}
        {renderOptions(categories)}
      </select>
    );
    
  }
  



// DEBUGGING VERSION

// function CategoryDropdown(props) {
//   const categories = props.categories;

//   // Indenting the sub-categories for the dropdown list.
//   function renderOptions(tree, indent = 0) {
//     const nbsp = "\u00A0".repeat(indent * 5);  // 4 spaces per indentation level

//     return Object.keys(tree).map((id) => (
//       <React.Fragment key={id}>
//         <option value={id}>
//           {nbsp}{tree[id].name}
//         </option>
//         {tree[id].children.length > 0 && renderOptions(tree[id].children, indent + 1)}
//       </React.Fragment>
//     ));
//   }

//   function handleCategoryChange(event) {
//     const selectedCategoryId = event.target.value;
//     console.group("Category Selection");
//     console.log("%cSelected Category ID: " + selectedCategoryId, "color: green; font-size: 16px;");
//     console.groupEnd();
//     props.setSelectedCategory(selectedCategoryId);
//   }
  

//   return (
//     <select className="form-control" onChange={handleCategoryChange}>
//       <option>Select Category</option>
//       {renderOptions(categories)}
//     </select>
//   );
// }