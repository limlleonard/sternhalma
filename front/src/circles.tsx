
const diameterPiece = 30;
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
