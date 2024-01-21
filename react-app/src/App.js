// App.js

import React, { useEffect, useState, useRef } from 'react';
import io from 'socket.io-client';

const ENDPOINT = 'http://localhost:5000';  

function base64ToImage(base64String) {
  const binaryString = atob(base64String);
  const bytes = new Uint8Array(binaryString.length);

  for (let i = 0; i < binaryString.length; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }

  const blob = new Blob([bytes], { type: 'image/jpg' });
  const imageUrl = URL.createObjectURL(blob);

  const image = new Image();
  image.src = imageUrl;

  return image;
}

const App = () => {
  const [socket, setSocket] = useState(null);
  const [playerScore, setPlayerScore] = useState(0);
  const [computerScore, setComputerScore] = useState(0);
  const [consecutiveWins, setConsecutiveWins] = useState(0);
  const imageRef = useRef(new Image());
  const [username, setUsername] = useState('');
  const [usernameEntered, setUsernameEntered] = useState(false);
  // Variable for list of top 5 scores
  const [topScores, setTopScores] = useState([]);

  useEffect(() => {
    const socket = io(ENDPOINT);
    setSocket(socket);

    return () => {
      socket.disconnect();
    };
  }, []);

  const handleUsernameSubmit = () => {
    setUsername(username);
    setUsernameEntered(true);
    socket.emit('username', username);
  };

  // useEffect(() => {
  //   if (!socket) return;

  //   socket.on('username', (data) => {
  //     setUsername(data.username);
  //   });

  //   return () => {
  //     socket.off('username');
  //   };
  // }, [socket]);

  useEffect(() => {
    if (!socket) return;

    socket.on('top_scores', (data) => {
      const decoder = new TextDecoder('utf-8');
      setTopScores(data.map((item) => ({ username: decoder.decode(item.username), score: item.score })));
    });

    return () => {
      socket.off('top_scores');
    }
  }, [socket]);

  useEffect(() => {
    if (!socket) return;

    socket.on('video_feed', (frame) => {
      const image = base64ToImage(frame);
      
      if (!imageRef.current) return;
      imageRef.current.src = image.src;
      // console.log("Frame received")
    });
    
    return () => {  
      socket.off('video_feed');
    } 
    
  }, [socket]);

  // Get scores from server {score, player_score, computer_score}
  useEffect(() => {
    if (!socket) return;

    socket.on('score', (data) => {
      setPlayerScore(data.player_score);
      setComputerScore(data.computer_score);
      setConsecutiveWins(data.consecutive_wins);
    });

    return () => {
      socket.off('score');
    };
  }, [socket]);

  // Styles 
  const containerStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    // Set height to match the the height of all the content
    height: '130vh',
    background: 'linear-gradient(to bottom, #3498db, #2ecc71)', // Gradient from blue to green
    color: '#fff', // Text color to ensure contrast
  };

  const scoreBoxStyle = {
    backgroundColor: '#f1f1f1',
    padding: '20px',
    borderRadius: '8px',
    textAlign: 'center',
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
    height: '100px', // Set a fixed height for the score boxes
    width: '80px', // Set a fixed width for the score boxes
  };
  
  const scoreLabelStyle = {
    fontSize: '1.2rem',
    color: '#3498db',
    marginBottom: '10px',
    fontFamily: 'Roboto',
  };
  
  const scoreValueStyle = {
    fontSize: '2rem',
    color: '#2ecc71',
    margin: '0',
    fontFamily: 'Roboto',
  };

  const textBoxContainerStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    // Set height to match the the height of all the content
    height: '100vh',
  };
  
  const textBoxStyle = {
    padding: '10px',
    fontSize: '1rem',
    border: '1px solid #ccc',
    borderRadius: '5px',
    marginBottom: '10px',
    width: '300px',
  };
  
  const tableCellStyle = {
    border: '1px solid #ddd',  // Border color
    padding: '8px',  // Padding for cells
    textAlign: 'left',  // Align text to the left within cells
  };

  
  return (
  <div style={containerStyle}>
    {/* <img ref={testImg} alt="TEST" style={{ width: '100px', height: '100px' }} /> */}
    
    {usernameEntered && (<h1 style={{ fontFamily: 'Roboto', fontSize: '3rem', color: '#2f4f4f', marginBottom: '20px' }}>Rock Paper Scissors</h1>) }

    {usernameEntered && (<img
      ref={imageRef}
      alt="STREAM"
      style={{
        border: '6px solid #1b1b1b', // You can adjust the color and thickness
        borderRadius: '8px', // Optional: adds rounded corners
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)', // Optional: adds shadow
      }}
    />
    )}

    {/* Username input box */}
    {!usernameEntered && (
      <div style={textBoxContainerStyle}>
        <h1 style={{ fontFamily: 'Roboto', fontSize: '3rem', color: '#2f4f4f' }}>Rock Paper Scissors</h1>
        <input
          type="text"
          placeholder="Enter your username"
          style={textBoxStyle}
          onChange={(e) => setUsername(e.target.value)}
        />
        <button
          style={{
            backgroundColor: '#2ecc71',
            color: '#fff',
            padding: '10px 20px',
            fontSize: '1.2rem',
            margin: '10px',
            border: 'none',
            cursor: 'pointer',
            borderRadius: '5px',
            boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
            fontFamily: 'Roboto',
          }}
          onClick={handleUsernameSubmit}
        >
          Submit
        </button>
      </div>
    )}
    


    {/* Button to start the game */}
    {usernameEntered && (<button
      style={{
        backgroundColor: '#2ecc71',
        color: '#fff',
        padding: '10px 20px',
        fontSize: '1.2rem',
        margin: '10px',
        border: 'none',
        cursor: 'pointer',
        borderRadius: '5px',
        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
        fontFamily: 'Roboto',
      }}
      onClick={() => socket.emit('start_game')}
    >
      Start Game
    </button>
    )}

    {/* Button to reset the scores */}
    {usernameEntered && (<button
      style={{
        backgroundColor: '#e74c3c',
        color: '#fff',
        padding: '10px 20px',
        fontSize: '0.8rem',
        margin: '10px',
        border: 'none',
        cursor: 'pointer',
        borderRadius: '5px',
        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
      }}
      onClick={() => socket.emit('reset_game')}
    >
      Reset Scores
    </button>
    )}

    {/* Display the consecutive wins */}
    {usernameEntered && (
      <div
        style={{
          display: 'flex',
          flexDirection: 'row',
          justifyContent: 'center',
          alignItems: 'center',  // Align text in the center vertically
          margin: '10px',  // Increase margin for better spacing
          padding: '15px',  // Add padding for space inside the box
          border: '2px solid #3498db',  // Border color
          borderRadius: '8px',  // Rounded corners
          backgroundColor: '#f1f1f1',  // Background color
        }}
      >
        <p
          style={{
            fontFamily: 'Roboto',
            fontSize: '1.2rem',
            color: '#2f4f4f',
            margin: '0',  // Remove default margin for the paragraph
          }}
        >
          Consecutive Wins: {consecutiveWins}
        </p>
      </div>
    )}

    {/* Display the scores */}
    {usernameEntered && 
    (<div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'center', margin: '20px' }}>
          <div style={scoreBoxStyle}>
            <p style={scoreLabelStyle}>{username}</p>
            <h2 style={scoreValueStyle}>{playerScore}</h2>
          </div>

          <div style={{ width: '20px' }}></div> {/* Adjust the space between score boxes */}

          <div style={scoreBoxStyle}>
            <p style={scoreLabelStyle}>CPU</p>
            <h2 style={scoreValueStyle}>{computerScore}</h2>
          </div>
    </div>)}
    
    {/* Display the top 5 scores*/}
    {usernameEntered && (<div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'center', margin: '20px', width: '25%'}}>
      <table style={{ borderCollapse: 'collapse', width: '100%' }}>
        <thead>
          <tr>
            <th style={tableCellStyle}>Player</th>
            <th style={tableCellStyle}>Score</th>
          </tr>
        </thead>
        <tbody>
          {topScores.map((item) => (
            <tr key={item.username}>
              <td style={tableCellStyle}>{item.username}</td>
              <td style={tableCellStyle}>{item.score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>)}
      
  </div>

  );
};

export default App;
