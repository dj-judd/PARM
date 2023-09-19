function CategoryDropdown(props) {
    const categories = props.categories;
  
    function renderOptions(tree, indent = 0) {
      return Object.keys(tree).map((id) => (
        <React.Fragment key={id}>
          <option value={id} style={{ paddingLeft: `${indent * 20}px` }}>
            {tree[id].name}
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
  