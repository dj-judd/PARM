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
    
    return (
      <select className="form-control">
        <option>Select Category</option>
        {renderOptions(categories)}
      </select>
    );
  }
  