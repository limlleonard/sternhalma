import { useEffect, useRef, useState } from "react";
import './App.css'

const diameterPiece = 30;
const url0='http://127.0.0.1:8000/';
interface BaseProps {
	x: number;
	y: number;
	colorInd?: number;
	className?: string;
	onKlicken: (coords: { x: number; y: number }) => void;
}
const Base: React.FC<BaseProps> = ({ x, y, className, onKlicken }) => {
	const klicken = () => {
		onKlicken({ x, y });
	};

	return (
	<div
		className={className}
		onClick={klicken}
		style={{
		position: 'absolute',
		width: `${diameterPiece}px`,
		height: `${diameterPiece}px`,
		left: `${x - diameterPiece / 2}px`,
		top: `${y - diameterPiece / 2}px`,
		}}
	></div>
	);
};
export const Circle: React.FC<BaseProps> = (props) => (
	<Base {...props} className="circle" />
);
export const Piece: React.FC<BaseProps> = (props) => (
	<Base {...props} className={`circle piece farbe${props.colorInd} `} />
);
export const Valid: React.FC<BaseProps> = (props) => (
	<Base {...props} className="circle valid" />
);
export const Selected: React.FC<BaseProps> = (props) => (
	<Base {...props} className={`circle piece selected farbe${props.colorInd}`} />
);

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
			const response = await fetch(`${url0}return_pieces/`, {
				method: "POST",
				headers: {"Content-Type": "application/json",},
				body: JSON.stringify({ nrPlayer }),
			});
			const llPiece: [number, number][][] = await response.json();
			setAAFigur(llPiece);
		} catch (err) {
			console.error("Error fetching pieces:", err);
		}
	};

	const stoppen = () => {
		if (timerInterval) clearInterval(timerInterval);
		setTimerInterval(null);
	};

	const reset = async () => {
		stoppen();
		setSeconds(0);
		setNrMoves(0);
		setOrder(0);
		try {
			const response = await fetch(`${url0}reset/`);
			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			} else {
				initBoard1();
				setSelected(null);
				setAAFigur([]);
				setArrValid([]);
			}
		} catch (err) {
			console.error("Error by resetting:", err);
		}
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

	const test1 = () => {
	}
	const klicken1 = async (coords: { x: number; y: number }) => {
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
				if (result.gewonnen) alert('Gewonnen!!!');
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
		// return () => stopTimer();
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
					<button onClick={stoppen}>Stop</button>
					<button onClick={reset}>Reset</button>
				</div>
				<p>Timer: <span id="timer" ref={timerRef}>{formatTime(seconds)}</span></p>
				<p>Number of moves: <span id="nrMoves">{nrMoves}</span></p>
				<p>Player in turn: <span className={`circleSmall farbe${order}`}></span></p>
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
