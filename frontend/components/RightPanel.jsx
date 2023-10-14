const RightPanel = () => {
  return (
    React.createElement('div', { id: 'right-panel'},
      [
        React.createElement(InfoPanel, null, null),
        React.createElement(Flags, null, null),
        React.createElement(Reservations, null, null)
      ]
    )
  );
};

window.RightPanel = RightPanel;
