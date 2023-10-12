
const { React } = window;

const SearchBar = () => {
  return React.createElement('input', { type: 'text', placeholder: 'Search...' }, null);
};

window.SearchBar = SearchBar;
