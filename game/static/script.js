const board = document.getElementById("board");
const { boardWidth, boardHeight } = board.getBoundingClientRect();
const centerX = board.offsetWidth / 2; // Center of the board
const centerY = board.offsetHeight / 2; // Center of the board
const diameterCircle = 30; // diameter of each circle
const diameterPiece = 30;
const distCC = 40; // center-center Distance
const middleLayer = 4; // Number of middleLayer to create, outside of it will be the corners
let selectedPiece = null;
let validPos1 = [];
let validPos2 = [];

let seconds = 0;
let timerInterval;
let nrMoves = 0;
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, "0")}`;
}

function startTimer() {
    if (timerInterval) return; // Prevent multiple timers from starting
    timerInterval = setInterval(() => {
        seconds++;
        document.getElementById("timer").textContent = formatTime(seconds);
    }, 1000);
}
function stopTimer() {
    clearInterval(timerInterval); // Stop the timer
    timerInterval = null;
}
function resetTimer() {
    clearInterval(timerInterval); // Stop the timer
    timerInterval = null;
    seconds = 0;
    document.getElementById("timer").textContent = "0:00";
}
document.getElementById("startButton").addEventListener("click", startTimer);
document.getElementById("stopButton").addEventListener("click", stopTimer);
document.getElementById("resetButton").addEventListener("click", resetTimer);

function createCircle(x, y, colorIndex) {
    // used in createBoard, create single circle-formed field
    const circle = document.createElement("div");
    const xr = Math.round(x);
    const yr = Math.round(y);
    if (colorIndex === 0) {
        circle.classList.add("circle");
    } else if (colorIndex === 1) {
        circle.classList.add("piece");
    }
    circle.style.left = `${x - diameterPiece / 2}px`; // Center the circle
    circle.style.top = `${y - diameterPiece / 2}px`; // Center the circle
    circle.id = `${xr}-${yr}-${colorIndex}`;
    circle.addEventListener("click", () => klicken(xr, yr, colorIndex));
    board.appendChild(circle);
}
function removePiece(x, y, colorIndex) {
    const piece = document.getElementById(`${x}-${y}-${colorIndex}`);
    piece.remove();
}
function resetValid() {
    // remove all valid class from circles
    const circles = document.querySelectorAll(".circle");
    circles.forEach((circle) => {
        circle.classList.remove("valid");
    });
    const pieces = document.querySelectorAll(".piece");
    pieces.forEach((piece) => {
        piece.classList.remove("selected");
    });
}
function movePiece(xrFrom, yrFrom, colorIndex, xrTo, yrTo) {
    removePiece(xrFrom, yrFrom, colorIndex);
    createCircle(xrTo, yrTo, colorIndex);
    selectedPiece = null;
    nrMoves++;
    // start timer
    if (!timerInterval) {
        timerInterval = setInterval(() => {
            seconds++; // Increment the seconds count
            document.getElementById("timer").textContent = formatTime(seconds); // Update the timer on the page
        }, 1000);
    }
    // update number of move
    const pNrMoves = document.getElementById("nrMoves");
    pNrMoves.textContent = nrMoves;
    // check winning, stop timer
}

// work with python
function initBoard1() {
    fetch("/return_board")
        .then((response) => response.json())
        .then((lstBoard) => {
            lstBoard.forEach(([x, y]) => {
                createCircle(x, y, 0);
            });
        })
        .catch((err) => console.error("Error fetching board data:", err));
}
function initPieces1() {
    fetch("/return_pieces")
        .then((response) => response.json())
        .then((lstPiece) => {
            lstPiece.forEach(([x, y]) => {
                createCircle(x, y, 1);
            });
        })
        .catch((err) => console.error("Error fetching pieces:", err));
}

async function klicken(xr, yr, colorIndex) {
    fetch("/klicken/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
        },
        body: JSON.stringify({ xr: xr, yr: yr }),
    })
        .then((response) => response.json())
        .then((result) => {
            console.log(xr, yr);
            resetValid();
            if (result.selected) {
                // get the piece by id xr-yr, add selected to class
                const piece = document.getElementById(
                    `${xr}-${yr}-${colorIndex}`
                );
                if (piece) piece.classList.add("selected");
            }
            result.validPos.forEach(([xr, yr]) => {
                const circle = document.getElementById(`${xr}-${yr}-0`);
                if (circle) circle.classList.add("valid");
            });
            if (result.coordTo) {
                movePiece(
                    result.coordFrom[0],
                    result.coordFrom[1],
                    1,
                    result.coordTo[0],
                    result.coordTo[1]
                );
            }
        });
}
document.addEventListener("DOMContentLoaded", () => {
    initBoard1();
    initPieces1();
});
