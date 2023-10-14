const React = window.React;
const Component = React.Component;
const ReactDOM = window.ReactDOM;

class CategoryDropdown extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selected: {
        label: 'Select Category...',
        value: ''
      },
      isOpen: false
    };
    this.handleDocumentClick = this.handleDocumentClick.bind(this);
  }

  componentDidMount() {
    document.addEventListener('click', this.handleDocumentClick, false);
  }

  componentWillUnmount() {
    document.removeEventListener('click', this.handleDocumentClick, false);
  }

  handleDocumentClick(event) {
    if (!ReactDOM.findDOMNode(this).contains(event.target)) {
      this.setState({ isOpen: false });
    }
  }

  handleMouseDown() {
    this.setState({ isOpen: !this.state.isOpen });
  }

  setValue(value, label) {
    const newState = {
      selected: {
        value,
        label
      },
      isOpen: false
    };
    if (this.props.setSelectedCategory) {
      this.props.setSelectedCategory(value);
    }
    this.setState(newState);
  }

  renderOptions(tree, indent = 0) {
    const lines = [];
    for (let i = 0; i < indent; i++) {
      lines.push(<span key={`line-${i}`} className="line" />);
    }

    if (!Array.isArray(tree)) return null;

    return tree.map((category) => (
      <li key={category.id}
          onClick={() => this.setValue(category.id, category.name)}
          onMouseDown={() => this.setValue(category.id, category.name)}>
        {lines}{category.name}
        {category.children.length > 0 && this.renderOptions(category.children, indent + 1)}
      </li>
    ));
  }

  render() {
    const { categories } = this.props;
    const { isOpen, selected } = this.state;

    return (
      <div className={`dropdown ${isOpen ? 'is-open' : ''}`}>
        <div className="dropdown-current"
             onMouseDown={() => this.handleMouseDown()}
             onTouchEnd={() => this.handleMouseDown()}>
          <div className="dropdown-option">
            {selected.label}
          </div>
        </div>
        {isOpen && (
          <div className="dropdown-select">
            <ul>
              {this.renderOptions(categories)}
            </ul>
          </div>
        )}
      </div>
    );
  }
}

window.CategoryDropdown = CategoryDropdown;