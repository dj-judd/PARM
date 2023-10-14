const UpperNavigation = () => {
  return (
    React.createElement(
        'div',
        { id: 'upper-navigation', style: { width: '100%' } },
        [
        React.createElement(SearchBar, null, null),
        React.createElement(
            'select',
            { id: 'dropdown-1' },
            [
            React.createElement('option', { value: 'option1' }, 'Option 1'),
            React.createElement('option', { value: 'option2' }, 'Option 2'),
            // ...other options
            ]
        ),
        // Add more dropdowns here
        ]
    )
  );
};

window.UpperNavigation = UpperNavigation;