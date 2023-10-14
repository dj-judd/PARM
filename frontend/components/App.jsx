const { React, ReactDOM } = window;
const assets = window.assets;
const categories = window.categories;

const App = () => {
  return (
    React.createElement('div', { id: 'app' },
      [
        React.createElement(LeftPanel, {assets, categories}, null),
        React.createElement(RightPanel, null, null)
      ]
    )
  );
};

window.App = App;


ReactDOM.render(
  React.createElement(App, null, null),
  document.getElementById('root')
);