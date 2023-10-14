const SearchBar = () => {
  return React.createElement('input', { 
    type: 'text', 
    className: 'search-bar',
    placeholder: 'Search...'
  }, null);
};


window.SearchBar = SearchBar;
