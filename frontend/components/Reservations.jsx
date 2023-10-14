const firstNames = ["Alice", "Bob", "Charlie", "David", "Eva", "Frank", "Grace", "Hannah", "Ivy", "Jack", "Karen", "Leo", "Megan", "Nathan", "Olivia", "Paul", "Quincy", "Rachel", "Steve", "Tina", "Ursula", "Victor", "Wendy", "Xander", "Yasmine", "Zach"];
const lastNames = ["Smith", "Johnson", "Brown", "Williams", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris", "Clark"];

const Reservation = (props) => {
  const { assetClicked } = props;
  const [reservations, setReservations] = React.useState([]);

  React.useEffect(() => {
    if (assetClicked !== null && assetClicked !== undefined) {
      const newReservations = generateRandomReservations();
      setReservations(newReservations);
    } else {
      setReservations([]);
    }
  }, [assetClicked]);
  

  return React.createElement('div', { id: 'reservation-container' },
  reservations.length === 0 ?
    React.createElement('div', { className: 'no-reservation' }, 'no current reservations') :
    [
      React.createElement('div', { className: 'reservation-title' }, 'Reservations'),
      reservations.map((res, index) => 
        React.createElement('div', { className: 'reservation-entry', key: index }, 
          [
            React.createElement('div', { className: 'user-name' }, res.user),
            React.createElement('div', { className: 'date-range' },
              [
                React.createElement('div', { className: 'start-date' },
                  [
                    React.createElement('div', { className: 'day' }, new Date(res.startDate).getDate()),
                    React.createElement('div', { className: 'month' }, new Date(res.startDate).toLocaleString('default', { month: 'short' }))
                  ]
                ),
                React.createElement('div', { className: 'separator' }, '~'),
                React.createElement('div', { className: 'end-date' },
                  [
                    React.createElement('div', { className: 'day' }, new Date(res.endDate).getDate()),
                    React.createElement('div', { className: 'month' }, new Date(res.endDate).toLocaleString('default', { month: 'short' }))
                  ]
                )
              ]
            )
          ]
        )
      )
    ]
  );
};

function generateRandomReservations() {
  const reservations = [];
  const hasReservations = Math.random() < 0.8;  // 80% chance to have reservations

  if (hasReservations) {
    const numReservations = Math.floor(Math.random() * 10) + 1;
    for (let i = 0; i < numReservations; i++) {
      const firstName = firstNames[Math.floor(Math.random() * firstNames.length)];  // Pick a random first name
      const lastName = lastNames[Math.floor(Math.random() * lastNames.length)];  // Pick a random last name
      const user = `${firstName} ${lastName}`;
      const startDate = new Date(Date.now() + Math.floor(Math.random() * 1000000000));
      const endDate = new Date(startDate.getTime() + Math.floor(Math.random() * 86400000)); // Add up to 1 day (86400000 ms)
      reservations.push({ user, startDate: startDate.toDateString(), endDate: endDate.toDateString() });
    }
  }

  return reservations;
}


window.Reservation = Reservation;