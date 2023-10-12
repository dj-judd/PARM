
const { React } = window;

const App = () => {
  return (
    React.createElement('div', { id: 'app-root' },
      [
        React.createElement(LeftPanel, null, null),
        React.createElement(RightPanel, null, null)
      ]
    )
  );
};

window.App = App;
