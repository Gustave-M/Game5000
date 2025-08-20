const socket = io({forceNew: true});
const gameAreaEl = document.getElementById('game-area');
const boardEl = document.getElementById('board');
const buttons = document.querySelectorAll('.button');

const dices = [];
const users = [];
const seats = [];

const mySeatIndex = 0;

const diceImages = [
  "assets/dice/dice-six-faces-one.png",
  "assets/dice/dice-six-faces-two.png",
  "assets/dice/dice-six-faces-three.png",
  "assets/dice/dice-six-faces-four.png",
  "assets/dice/dice-six-faces-five.png",
  "assets/dice/dice-six-faces-six.png"
];

const stateColorTable = {
  "waiting": "#00ffff",
  "selected": "#0000ff",
  "unselected": "#ff0000",
  "fixed": "#ff00ff"
};

const seatPositions = [
  { bottom: '0%', left: '50%', transform: 'translate(-50%, 0%)' },
  { top: '50%', left: '0%',    transform: 'translate(0%, -50%)' },
  { top: '25%', left: '0%',    transform: 'translate(0%, -50%)' },
  { top: '0%',  left: '33.3%', transform: 'translate(-50%, 0%)' },
  { top: '0%',  left: '66.7%', transform: 'translate(-50%, 0%)' },
  { top: '25%', right: '0%',   transform: 'translate(0%, -50%)' },
  { top: '50%', right: '0%',   transform: 'translate(0%, -50%)' }
];

// Dices creation and init
for (let i = 0; i < 6; i++) {
  const dice = document.createElement('div');
  dice.classList.add('dice');

  dice.addEventListener('click', () => {
    socket.emit('dice-click', { id: i });
  });

  boardEl.appendChild(dice);
  dices.push(dice);
}

// Seats creation and init
seatPositions.forEach((pos, index) => {

  const seat = document.createElement('div');
  seat.classList.add('seat');
  seat.id = `seat-${index}`;
  seat.classList.add('seat--empty');

  Object.assign(seat.style, pos);
  
  // Username
  const nameEl = document.createElement('div');
  nameEl.classList.add('username');
  nameEl.textContent = "Empty"; // default value

  if (index === mySeatIndex) {
    nameEl.classList.add('username--changeable');
    nameEl.addEventListener('click', () => {
      const newUsername = prompt("Enter your username (letters and numbers only):");
      if (newUsername && /^[a-zA-Z0-9 ]+$/.test(newUsername)) {
        socket.emit('change-username', {username: newUsername });
      } else if (newUsername) {
        alert("Username must contain only letters, numbers, and spaces.");
      }
      if (newUsername) {
        socket.emit('change-username', {username: newUsername });
      }
    });
  }

  // Score
  const scoreEl = document.createElement('div');
  scoreEl.classList.add('score');


  seat.append(nameEl, scoreEl);
  gameAreaEl.appendChild(seat);
});

// Buttons event listeners
buttons.forEach(button => {
  button.addEventListener('click', () => {
    socket.emit(button.dataset.action, {});
  });
});

/********** Updates functions **********/

// Mise à jour d’un siège (username + score)
socket.on('update-seat', (data) => {
  const { seatIndex, username, score, isActive, isEmpty } = data;
  const seat = document.getElementById(`seat-${seatIndex}`);
  if (!seat) return;

  const usernameEl = seat.querySelector('.username');
  const scoreEl = seat.querySelector('.score');

  if (isEmpty) {
    // 🪑 Cas siège vide → pas de username/score dans data
    usernameEl.textContent = "Empty2";
    scoreEl.textContent = "";
    seat.classList.add('seat--empty');
    seat.classList.remove('seat--active');
  } else {
    // 👤 Cas siège occupé → data contient username/score
    usernameEl.textContent = username ?? "Unknown";
    scoreEl.textContent = score ?? 0;

    seat.classList.remove('seat--empty');
    if (isActive) {
      seat.classList.add('seat--active');
    } else {
      seat.classList.remove('seat--active');
    }
  }
});


socket.on('update-dice', (data) => {
  const { id, value, state } = data;
  if (value < 1 || value > dices.length) {
    dices[id].style.backgroundColor = "#ffffff"
    dices[id].style.backgroundImage = "none";
  }else{
    dices[id].style.backgroundImage = `url(${diceImages[value - 1]})`;
    dices[id].style.backgroundColor = "transparent";
  }
  dices[id].style.backgroundSize = "cover";
  dices[id].style.backgroundPosition = "center";
  dices[id].style.borderColor = stateColorTable[state];
});

socket.on('show_alert', (data) => {
    alert(data.message);
});

socket.on('update-turn-info', (data) => {
  const { gain, unselectedGain, haveToPlay } = data;
  const turnInfoEl = document.getElementById('turn-info');
  
  turnInfoEl.innerHTML = `
    <div><strong>Gain :</strong> ${gain}</div>
    <div><strong>Unselected Gain :</strong> ${unselectedGain}</div>
    <div><strong>Can validate :</strong> ${!haveToPlay ? "✅ Yes" : "❌ No"}</div>
  `;
});


/*document.addEventListener("DOMContentLoaded", () => {
  const mySeatIndex = 0;  // ton siège attribué (par ex. 0)
  const myUsernameEl = document.querySelector(`#seat-${mySeatIndex} .username`);

  if (myUsernameEl) {
    myUsernameEl.addEventListener("click", () => {
      // Émission vers le backend Python
      socket.emit("username-clicked", { seatIndex: mySeatIndex });
    });
  }
});*/

