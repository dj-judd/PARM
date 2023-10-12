
const { React } = window;

const RightPanel = () => {
  return (
    React.createElement('div', { id: 'right-panel', style: { overflowY: 'auto' } },
      [
        React.createElement(Navigation, null, null),
        React.createElement(CategoryName, null, null),
        React.createElement(InfoPanel, null, null),
        React.createElement(Flags, null, null),
        React.createElement(Reservations, null, null)
      ]
    )
  );
};

window.RightPanel = RightPanel;
