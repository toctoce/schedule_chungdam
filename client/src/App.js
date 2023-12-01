// App.js

import "./App.css";
import React, { useState } from "react";
import ScheduleCd from "./ScheduleCd";
import AudioRecord from "./audioRecode";

function App() {
  const [isPaused, setPaused] = useState(true);
  // const [initialBoardSize, setInitialBoardSize] = useState(null);
  const [numRows, setNumRows] = useState();
  const [numCols, setNumCols] = useState();
  const [startInput, setStartInput] = useState("");
  const [spotInput, setSpotInput] = useState("");
  const [hazardInput, setHazardInput] = useState("");
  const [colorInput, setColorInput] = useState("");
  const [error, setError] = useState(null); // 추가
  const [receivedData, setReceivedData] = useState(null);
  const [newData, setNewData] = useState(null);

  console.log(numRows, numCols);
  const mapdata = `(${numRows} ${numCols})`;
  console.log(mapdata);
  const handleResume = () => {
    setPaused(false);
  };

  const parseDimensions = (input) => {
    const matches = input.match(/\((\d+)\s+(\d+)\)/);
    if (matches && matches.length === 3) {
      setError(null);
      return { rows: parseInt(matches[1]), cols: parseInt(matches[2]) };
    } else {
      setError("Invalid input format. Please use the format (rows cols).");
      return null;
    }
  };

  const handlePostData = () => {
    const dataToSend = {
      map_input: mapdata,
      start_input: startInput,
      spot_input: spotInput,
      hazard_input: hazardInput,
      color_input: colorInput,
    };

    // 서버로 데이터 전송 예시
    fetch("http://127.0.0.1:5000/operator-input", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(dataToSend),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Data sent successfully:", data);
        setReceivedData({ data });
        console.log({ receivedData });
        // 이거 받고 동작하게끔 하는거 이제 추가하면 됨.
      })

      .catch((error) => {
        console.error("Error sending data:", error);
      });
  };

  const handleExecute = () => {
    const isValidFormat = (input) => /^\((\(\d+\s+\d+\))+\)$/.test(input);
    const isValidFormatMap = (input) => /^\(\d+\s+\d+\)$/.test(input);
    if (
      !isValidFormatMap(startInput) ||
      !isValidFormat(spotInput) ||
      !isValidFormat(hazardInput) ||
      !isValidFormat(colorInput)
    ) {
      setError("Invalid data format. Please use the format (x y)");
      return;
    }
    console.log("start");
    setError(null);
    setPaused(false);

    const handleNextDataReceived = (nextData) => {
      // nextData를 필요한 변수에 저장하는 작업 수행
      console.log("다음 데이터:", nextData);
    };
  };

  return (
    <div>
      <h1>Robot Schedule App</h1>

      <div>
        <label>
          Map:
          <input
            type="text"
            placeholder="ex.(4 5)"
            onChange={(e) => {
              const dimensions = parseDimensions(e.target.value);
              if (dimensions) {
                setNumRows(dimensions.rows);
                setNumCols(dimensions.cols);
              }
            }}
          />
        </label>
      </div>
      <div>
        <label>
          Start:
          <input
            type="text"
            placeholder="ex.(2 3)"
            value={startInput}
            onChange={(e) => setStartInput(e.target.value)}
          />
        </label>
      </div>
      <div>
        <label>
          Spot:
          <input
            type="text"
            placeholder="ex.((1 2)(3 4))"
            value={spotInput}
            onChange={(e) => setSpotInput(e.target.value)}
          />
        </label>
      </div>
      <div>
        <label>
          Color:
          <input
            type="text"
            value={colorInput}
            placeholder="ex.((1 2)(3 4))"
            onChange={(e) => setColorInput(e.target.value)}
          />
        </label>
      </div>
      <div>
        <label>
          Hazard:
          <input
            type="text"
            value={hazardInput}
            placeholder="ex.((1 2)(3 4))"
            onChange={(e) => setHazardInput(e.target.value)}
          />
        </label>
      </div>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <button onClick={handleExecute}>Execute</button>
      <button onClick={handlePostData}>Post Data</button>
      <ScheduleCd
        isPaused={isPaused}
        numRows={numCols + 1}
        numCols={numRows + 1}
        receivedData={receivedData} // 함수를 전달
        setNewData={setNewData}
        setError={setError}
      />
      <AudioRecord
        setPause={setPaused}
        setReceivedData={setReceivedData}
        newData={newData}
      />
      <button onClick={handleResume}>재개</button>
    </div>
  );
}

export default App;
