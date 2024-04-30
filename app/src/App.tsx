import React, { useState } from 'react';
import './App.css';
import SearchBar from './Components/SearchBar';
import WordResult from './Components/WordResult';

function App() {
  const [chosenWord, setChosenWord] = useState<string>("")

  return (
    <div className="App">
      <div className='headerSection'>
        <img style={{maxWidth: "80%"}} src="TDK12.png" alt="" />
      </div>
      <div className='searchBarSection'>
        <br />
        <br />
        <SearchBar setChosenWord={setChosenWord} />
        <br />
        <br />
      </div>
      <div className='definitionsSection'>
        {
          chosenWord &&
          <WordResult chosenWord={chosenWord} />
        }
      </div>
      <div className='footerSection'>

        <i className="pi pi-github"
          style={{ fontSize: '2rem', cursor: 'pointer' }}
          onClick={() => window.open('https://github.com/bora-7/tdk-12-kindle')}
        />
      </div>
      {/* https://github.com/bora-7/tdk-12-kindle */}


    </div>
  );
}

export default App;
