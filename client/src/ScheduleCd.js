import React, { useState, useEffect } from "react";
import "./ScheduleCd.css";

const numRows = 7;
const numCols = 10;
const stringArray = [
  ".HHHHCCCCCHHHHHCCCCCHHHHHCCCCCHHHHHCCCCCHHHHHCCCCCHHHHHCCCCCHHHHHCCCCC",
  ".HHHHCCCCCHHHHHCCCCCHHHHHCCCCCHHHHHCCCCCHHHHHCCCCCHHHHHCCCCCHHHHHRRRRR",
  "HHHHHCCCCCHHHHHCCCCCHHHHHCCCCCHHHHHCCCCCHHHHHCCCCCHHHHHCCCCCHHHHHPPPPP",
  "HHHHHCCCCCHHHHHCCCCCHHHHHCCCCCHHHHHCCCCCHHHHHCCCCCHHHHHCCCCCHHHHHHHHHH",
  // ... (원하는 문자열을 추가해주세요)
];

const generateEmptyBoard = () => {
  const board = [];
  for (let i = 0; i < numRows; i++) {
    board.push(Array(numCols).fill(undefined));
  }
  return board;
};

const ScheduleCd = ({ isPaused }) => {
  const [board, setBoard] = useState(generateEmptyBoard());
  const [errorMessage, setErrorMessage] = useState("");
  const [stringIndex, setStringIndex] = useState(0);

  const getImagePath = (value) => {
    switch (value) {
      case "H":
        return process.env.PUBLIC_URL + "/hazard.png";
      case "C":
        return process.env.PUBLIC_URL + "/colorblob.png";
      case "R":
        return process.env.PUBLIC_URL + "/robot.png";
      case "P":
        return process.env.PUBLIC_URL + "/point.png";
      case "c":
      case "h":
        return undefined;
      default:
        return "";
    }
  };

  useEffect(() => {
    const intervalId = setInterval(() => {
      if (!isPaused && stringIndex < stringArray.length) {
        // 배열에서 다음 문자열을 가져와서 보드를 업데이트합니다.
        const nextString = stringArray[stringIndex];
        const newBoard = generateEmptyBoard();
        for (let i = 0; i < nextString.length; i++) {
          const inputValue = nextString[i];
          const [row, col] = getRowColFromIndex(i);
          newBoard[row][col] = inputValue;
        }
        setBoard(newBoard);

        // 다음 문자열로 넘어갑니다.
        setStringIndex((prevIndex) => prevIndex + 1);
      } else {
        // 모든 문자열을 돌았을 때, interval을 정리하고 종료 메시지를 표시합니다.
        clearInterval(intervalId);
        //setErrorMessage("정상적으로 종료되었음. 영규 보쌈 언제 먹을래?");
        console.log("Recording stopped at index:", stringIndex - 1);
        console.log("Corresponding stringArray:", stringArray[stringIndex - 1]);
      }
    }, 1000);

    return () => {
      // 컴포넌트가 언마운트되면 interval을 정리합니다.
      clearInterval(intervalId);
    };
  }, [stringIndex, isPaused]);

  const getRowColFromIndex = (index) => {
    const row = Math.floor(index / numCols);
    const col = index % numCols;
    return [row, col];
  };

  return (
    <div>
      <h1>ScheduleCd</h1>
      <table className="mapBoard">
        <tbody>
          {board.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {row.map((cell, colIndex) => (
                <td key={colIndex}>
                  {colIndex < numCols && <div className="vertical-line" />}
                  {rowIndex < numRows && <div className="horizontal-line" />}
                  <td style={{ position: "relative" }}>
                    {cell && (
                      <React.Fragment>
                        {getImagePath(cell) && (
                          <img
                            src={getImagePath(cell)}
                            alt={`Cell at (${rowIndex}, ${colIndex})`}
                            className={`cell-image cell-image-${cell}`}
                          />
                        )}
                      </React.Fragment>
                    )}
                  </td>
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>

      {errorMessage && <div className="error">{errorMessage}</div>}
    </div>
  );
};

export default ScheduleCd;
