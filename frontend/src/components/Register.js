// src/components/Register.js
import React, { useState } from 'react';
import axios from 'axios';


function Register(props) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
        console.log(username)
      await axios.post('http://127.0.0.1:5000/register', { username, password }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      // Redirect or show success message
      props.history.push('/login'); // assuming you're using React Router for navigation
    } catch (error) {
      // Handle error, maybe set an error state and show it to the user
      console.error('Registration failed:', error.response.data);
    }
};

  return (
    <div>
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default Register;
