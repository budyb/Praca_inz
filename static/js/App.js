// import React from "react";

// const App = () => {
//   return <div>dupa!</div>;
// };

// export default App;


import React, { Component } from "react";
import { render } from "react-dom";
//import HomePage from "./HomePage";

export default class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <h1>REACT</h1>
      </div>
    );
  }
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);