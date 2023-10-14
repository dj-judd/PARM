const UpperNavigation = (props) => {
    return (
      React.createElement(
        'div',
        { id: 'upper-navigation' },
        [React.createElement(
            'a',
            {
                href: '/',
                style: {
                textDecoration: 'none',
                fontSize: '30px',
                marginLeft: '10px',
                }
            },
            '🧀'
          ),
          React.createElement(SearchBar, null, null),
          React.createElement(CategoryDropdown, { setSelectedCategory: props.setSelectedCategory, categories: props.categories }, null),
        ]
      )
    );
  };
  
  window.UpperNavigation = UpperNavigation;
  