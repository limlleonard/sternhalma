import { useEffect, useRef, useState } from "react";
import './App.css'
import {Circle, Piece, Valid, Selected} from "./circles"
// const url0='http://127.0.0.1:8000/';
const url0=`${window.location.origin}:80/`

interface ModelScore {
    id: number;
    score: number | string;
    name: string;
}
function App() {
	// const [count, setCount] = useState(0)
	const timerRef = useRef<HTMLDivElement>(null);
	const [nrMoves, setNrMoves] = useState(0);
	const [seconds, setSeconds] = useState(0);
	const [timerInterval, setTimerInterval] = useState<number | null>(null);
	const [selected, setSelected] = useState<[number, number] | null>(null);
	const [arrCircle, setArrCircle] = useState<[number,number][]>([]);
	const [aaFigur, setAAFigur] = useState<[number,number][][]>([]); // array of array of figur
	const [arrValid, setArrValid] = useState<[number,number][]>([]);
	const [order, setOrder] = useState<number>(0);
	const [nrPlayer, setNrPlayer] = useState<number>(1);
    const [bestList, setBestList] = useState<ModelScore[]>([]);
	const [aktiv, setAktiv] = useState(false);

	const formatTime = (seconds: number) => {
		const minutes = Math.floor(seconds / 60);
		const remainingSeconds = seconds % 60;
		return `${minutes}:${remainingSeconds.toString().padStart(2, "0")}`;
	};

	const starten = async () => {
		if (timerInterval) return;
		const interval = setInterval(() => {
			setSeconds((prev) => prev + 1);
		}, 1000);
		setTimerInterval(interval);
		try {
			const response = await fetch(`${url0}starten/`, {
				method: "POST",
				headers: {"Content-Type": "application/json",},
				body: JSON.stringify({ nrPlayer }),
			});
			const llPiece: [number, number][][] = await response.json();
			setAAFigur(llPiece);
			setAktiv(true)
		} catch (err) {
			console.error("Error fetching pieces:", err);
		}
	};

	const reset = async () => {
		if (timerInterval) clearInterval(timerInterval);
		setTimerInterval(null);
		setSeconds(0);
		setNrMoves(0);
		setOrder(0);

		initBoard1();
		setSelected(null);
		setAAFigur([]);
		setArrValid([]);
		setAktiv(false)
		// Wenn man auf reset klickt, das Spiel läuft immer noch im Backend, aber der Frontend ist deaktiviert
	};

	const initBoard1 = async () => {
		try {
			const response = await fetch(`${url0}return_board/`);
			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}
			const contentType = response.headers.get("content-type");
			if (!contentType || !contentType.includes("application/json")) {
				throw new Error("Received non-JSON response");
			}
			const lstBoard: [number, number][] = await response.json();
			const lstBoardRound:[number, number][]= lstBoard.map(([x, y]:[number, number]) => [Math.round(x), Math.round(y)]);
			setArrCircle(lstBoardRound);
		} catch (err) {
			console.error("Error fetching board data:", err);
		}
	};

    const fetchScores = () => {
        fetch(`${url0}api/score/`)
            .then((response) => response.json())
            .then((apiData: ModelScore[]) => {
                const filledData = [
                    ...apiData,
                    ...Array.from({ length: Math.max(0, 5 - apiData.length) }, () => ({
                        id: Math.random(),
                        score: '---',
                        name: '----------',
                    })),
                ];
                setBestList(filledData);
            })
            .catch((error) => console.error('Error fetching data:', error));
    };

    const handleNewScore = (newScore: number) => {
        // Find the highest score in the array
        const scores = bestList
            .map((item) => (typeof item.score === 'number' ? item.score : -Infinity))
            .filter((score) => score !== -Infinity);
        const highestScore = scores.length > 0 ? Math.max(...scores) : -Infinity;

        if (newScore < highestScore || scores.length<5 ) {
            const name = prompt('Congratulations! Would you like to leave your name on the ranking:')?.trim();
            if (name && name.length <= 20) {
                fetch(`${url0}api/add_score/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ score: newScore, name }),
                })
                    .then((response) => {
                        if (!response.ok) {
                            throw new Error('Failed to add score');
                        }
                        return response.json();
                    })
                    .then(() => {
                        alert('Score added successfully!');
                        fetchScores(); // Refresh the scores
                    })
                    .catch((error) => {
                        console.error('Error adding score:', error);
                        alert('Error adding score. Please try again.');
                    });
            }
        }
    };

	const test1 = async () => {
		// const score = parseInt(prompt('Enter a new score:') || '', 10);
		// if (!isNaN(score)) {
		// 	handleNewScore(score);
		// }
		alert('Du bist aber neugierig...')
	}
	const klicken1 = async (coords: { x: number; y: number }) => {
		if (!aktiv) return 
		const xr=coords.x;
		const yr=coords.y;
		try {
			const response = await fetch(`${url0}klicken/`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ xr, yr }),
			});
			const result = await response.json();
			setSelected(null);
			if (result.selected) {
				setSelected([coords.x, coords.y]);
			}
			setArrValid(result.validPos);
			if (result.neueFiguren) {
				setAAFigur(result.neueFiguren)
				setNrMoves((prev) => prev+1);
				setOrder(result.order)
				if (result.gewonnen) {
					handleNewScore(nrMoves)
					setAktiv(false)
				};
			}
		} catch (err) {
			console.error("Error during klicken:", err);
		}
	}
	const handleSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
		setNrPlayer(parseInt(e.target.value))
	}
	useEffect(() => {
		initBoard1();
		fetchScores();
	}, []);

	// useEffect(() => {
		// if (timerRef.current) {
		// 	timerRef.current.textContent = formatTime(seconds);
		// }
	// }, [seconds]);

	return (
		<>
		<div className="ctn0">
			<section className="side-bar">
				<h1>Sternhalma</h1>
				<div className="ctn-select">
					<label htmlFor="nrPlayer">Nr of players: </label>
					<select name="nrPlayer" id="nrPlayer" onChange={handleSelect} value={nrPlayer}>
						<option value="1">1</option>
						<option value="2">2</option>
						<option value="3">3</option>
					</select>
				</div>
				<div id="ctn-btn">
					<button onClick={starten}>Start</button>
					<button onClick={reset}>Reset</button>
				</div>
				<p>Timer: <span id="timer" ref={timerRef}>{formatTime(seconds)}</span></p>
				<p>Number of moves: <span id="nrMoves">{nrMoves}</span></p>
				<p>Player in turn: <span className={`circleSmall farbe${order}`}></span></p>
				<p>High score list:</p>
				<table>
					<tbody>
						{bestList.map((item) => (
							<tr key={item.id}>
								<td>{item.score}</td>
								<td>{item.name}</td>
							</tr>
						))}
					</tbody>
					{/* <tr>
						<td>100</td>
						<td>Anna</td>
					</tr>
					<tr>
						<td>120</td>
						<td>Lena</td>
					</tr>
					<tr>
						<td>---</td>
						<td>----------</td>
					</tr> */}
				</table>
				<button onClick={test1}>Test1</button>
			</section>
			<div className="board" id="board" >
				{arrCircle.map(([x, y]) => (
					<Circle key={`${x}-${y}`} x={x} y={y} onKlicken={klicken1}/>
				))}
				{aaFigur.map((arrFigur, nrSpieler) => (
					arrFigur.map(([x, y]) => (
						<Piece key={`${x}-${y}`} x={x} y={y} colorInd={nrSpieler} onKlicken={klicken1} />
					))
				))}
				{arrValid.map(([x, y]) => (
					<Valid key={`${x}-${y}`} x={x} y={y} onKlicken={klicken1} />
				))}
				{selected ? (<Selected x={selected[0]} y={selected[1]} colorInd={order} onKlicken={klicken1} /> ) : null}
			</div>
		</div>
		</>
	)
}

export default App

// farben auswählen, feld farbe
// Dynamic Refs Storage: useRef<{ [key: string]: CircleRef | null }> creates an object to hold references to all Circle components.
// Assigning Refs: The ref prop is set using an inline function to dynamically store each Circle component by its key (x-y).
// Accessing Specific Circle: The handleSetValid function takes coordinates and calls setValid(true) on the correct circle.

// score list, one should not be able to click on the circles unless the game is started
// 1 server - 1 room / player. let the other wait.
// 1 server - multi rooms, create a instance for each room and direct the gamer to the room, python-socketio
// save those instance to a dict and ...
// ogs