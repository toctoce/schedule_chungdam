// ScheduleCd.js

import React, { useState, useEffect } from "react";
import "./ScheduleCd.css";

const generateEmptyBoard = (numRows, numCols) => {
  const board = [];
  for (let i = 0; i < numRows; i++) {
    board.push(Array(numCols).fill(undefined));
  }
  return board;
};

const ScheduleCd = ({
  isPaused,
  numRows,
  numCols,
  receivedData,
  setNewData,
  setError,
}) => {
  const [board, setBoard] = useState(generateEmptyBoard(numRows, numCols));
  const [dummyData, setDummyData] = useState(null);

  const getRowColFromIndex = (index) => {
    const row = Math.floor(index / numCols);
    const col = index % numCols;

    return [row, col];
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        // const response = await fetch("./dummy.json");
        // const response = receivedData;
        // const data = await response.json();

        setDummyData(receivedData);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [isPaused]);

  useEffect(() => {
    if (!dummyData || isPaused) return;

    let stringIndex = 0;
    const intervalId = setInterval(() => {
      if (stringIndex < dummyData.data.length) {
        const nextData = dummyData.data[stringIndex];
        setNewData(nextData);
        console.log({ nextData });
        const newBoard = mapInfoToBoard(nextData.map_info, nextData.robot);
        setBoard(newBoard);
        stringIndex++;
        console.log(nextData.status);
        if (nextData.status === 1) {
          setError("오작동이 발생했습니다");
        } else if (nextData.status === -1) {
          setError(nextData.err);
        } else {
          setError(" ");
        }
      } else {
        clearInterval(intervalId);
        console.log("Recording stopped at index:", stringIndex - 1);
        console.log(
          "Corresponding map_info:",
          dummyData.data[stringIndex - 1].map_info
        );
      }
    }, 1000);

    return () => {
      clearInterval(intervalId);
    };
  }, [dummyData, isPaused]);

  const mapInfoToBoard = (mapInfo, robot) => {
    const lines = (mapInfo || "").split("\n");

    const newBoard = generateEmptyBoard(numRows, numCols);

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];

      for (let j = 0; j < line.length; j++) {
        const inputValue = line[j];
        const [row, col] = getRowColFromIndex(i * numCols + j);
        let cellType = "";

        switch (inputValue) {
          case "H":
            cellType = "hazard";
            break;
          case "C":
            cellType = "colorblob";
            break;
          case "P":
            cellType = "point";
            break;
          case "c":
            cellType = "colorblobB";
            break;
          case "h":
            cellType = "hazardB";
            break;
          default:
            cellType = "empty";
            break;
        }
        if (row === robot.row && col === robot.col) {
          console.log(robot.direction);
          switch (robot.direction) {
            case 0:
              cellType = "robotN";
              break;
            case 1:
              cellType = "robotE";
              break;
            case 2:
              cellType = "robotS";
              break;
            case 3:
              cellType = "robotW";
              break;
            default:
              cellType = "empty";
              break;
          }
        }

        if (!newBoard[row]) {
          newBoard[row] = [];
        }
        newBoard[row][col] = { type: cellType };
      }
    }

    return newBoard;
  };

  const getImagePath = (cell) => {
    const { type } = cell;

    switch (type) {
      case "empty":
        return "";
      case "hazard":
        //console.log(1);
        return process.env.PUBLIC_URL + "/hazard.png";
      case "colorblob":
        return process.env.PUBLIC_URL + "/colorblob.png";

      case "point":
        return process.env.PUBLIC_URL + "/point.png";

      case "hazardB":
        return process.env.PUBLIC_URL + "/hazardB.png";

      case "colorblobB":
        return process.env.PUBLIC_URL + "/colorblobB.png";

      default:
        return "";
    }
  };

  const getRobotPath = (cell) => {
    const { type } = cell;

    switch (type) {
      case "robotE":
        return process.env.PUBLIC_URL + "/robotE.png";
      case "robotS":
        return process.env.PUBLIC_URL + "/robotS.png";
      case "robotW":
        return process.env.PUBLIC_URL + "/robotW.png";
      case "robotN":
        return process.env.PUBLIC_URL + "/robotN.png";
      default:
        return "";
    }
  };

  return (
    <div>
      <h1>Mapboard⬇️</h1>
      <table className="mapBoard">
        <tbody>
          {board.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {row.map((cell, colIndex) => (
                <td key={colIndex}>
                  {colIndex < numCols && <div className="vertical-line" />}
                  {rowIndex < numRows && <div className="horizontal-line" />}
                  <td>
                    <div
                      style={{
                        position: "relative",
                        width: "50px",
                        height: "50px",
                      }}
                    >
                      {cell && (
                        <React.Fragment>
                          {getImagePath(cell) && (
                            <img
                              src={getImagePath(cell)}
                              alt={`Cell at (${rowIndex}, ${colIndex})`}
                              className={`cell-image cell-image-${cell.type}`}
                            />
                          )}
                          {getRobotPath(cell) && (
                            <img
                              src={getRobotPath(cell)}
                              alt={`Cell at (${rowIndex}, ${colIndex})`}
                              className={`robot-image robot-image-${cell.type}`}
                            />
                          )}
                        </React.Fragment>
                      )}
                    </div>
                  </td>
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ScheduleCd;
