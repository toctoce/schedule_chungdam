// InputForm.js
import React, { useState } from "react";

const InputForm = ({ onExecute }) => {
  const [numRows, setNumRows] = useState("");
  const [numCols, setNumCols] = useState("");

  const handleExecute = () => {
    // 입력값이 유효한지 여부를 확인하고, 유효하다면 onExecute 함수 호출
    const isValid = validateInput(numRows, numCols);
    if (isValid) {
      onExecute({ numRows: parseInt(numRows), numCols: parseInt(numCols) });
    }
  };

  const validateInput = (rows, cols) => {
    const isValid = !isNaN(rows) && !isNaN(cols) && rows > 0 && cols > 0;
    if (!isValid) {
      alert(
        "Invalid input. Please enter positive integers for rows and columns."
      );
    }
    return isValid;
  };

  return (
    <div>
      <label>
        Rows:
        <input
          type="number"
          value={numRows}
          onChange={(e) => setNumRows(e.target.value)}
        />
      </label>
      <label>
        Columns:
        <input
          type="number"
          value={numCols}
          onChange={(e) => setNumCols(e.target.value)}
        />
      </label>
      <button onClick={handleExecute}>Execute</button>
    </div>
  );
};

export default InputForm;
