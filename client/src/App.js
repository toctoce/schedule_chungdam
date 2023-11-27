// App.js

import "./App.css";
import React, { useState } from "react";
import ScheduleCd from "./ScheduleCd";
import AudioRecord from "./audioRecode";

function App() {
  const [isPaused, setPaused] = useState(false);

  const handleResume = () => {
    setPaused(false);
  };

  return (
    <div>
      <ScheduleCd isPaused={isPaused} />
      <AudioRecord setPause={setPaused} />
      <button onClick={handleResume}>재개</button>
    </div>
  );
}

export default App;
