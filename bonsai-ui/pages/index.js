// pages/index.js
import { useRouter } from 'next/router';
import React, { useState } from 'react';
import axios from 'axios';

const Home = () => {
  const router = useRouter();
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };
  const fetchData = async (user) => {
    try {
      // Define your API endpoint and parameters
      const apiUrl = 'http://127.0.0.1:5000/github';
      const params = {
        user_input: user_input,
      };

      // Convert the parameters into a query string
      const queryString = Object.keys(params)
        .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
        .join('&');

      // Combine the API endpoint and the query string
      const urlWithParams = `${apiUrl}?${queryString}`;

      // Send the GET request
      const response = await fetch(urlWithParams);

      // Handle the response
      if (response.ok) {
        const data = await response.json();
        console.log('Data:', data);
      } else {
        console.error('Error:', response.status);
      }
    } catch (error) {
      console.error('Error:', error);
    }
      };

  const handleSearch = async() => {
    // Implement your search functionality here
    const result = `Searching for: ${inputValue}`;
    try{
      const response = await axios.get(`http://127.0.0.1:5000/github?user_input=${JSON.stringify(inputValue)}`)
      console.log('Server response:', response.data);
      router.push(`/result?result=${response.data}`);
    }  
    catch (error) {
      console.error('Error submitting response:', error);
    }    
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-black via-orange-500 to-black">
      {/* Black bar on top with categories */}
      <div className="bg-black text-white p-4 w-full text-center fixed top-0 z-10">
        <div className="flex justify-center items-center">
          <span className="mr-4 cursor-pointer text-lg font-semibold border-r border-gray-600 pr-4">Projects</span>
          <span className="mr-4 cursor-pointer text-lg font-semibold border-r border-gray-600 pr-4">Trending</span>
          <span className="cursor-pointer text-lg font-semibold">Open Jobs</span>
        </div>
        <div className="flex items-center">
          <span className="text-4xl font-bold mr-4 text-gray-300">BONSAI</span>
        </div>
      </div>

      {/* Main content */}
      <div className="text-center mt-16">
        <h1 className="text-8xl font-bold mb-12 text-gray font-bold">
          Bonsai
        </h1>
        <div className="flex flex-col items-center">
          <input
            type="text"
            className="border p-3 rounded-md text-lightGray bg-black w-96 mb-2 border-black shadow-md font-semibold"
            placeholder="Write your product idea"
            value={inputValue}
            onChange={handleInputChange}
          />
          <button
            className="bg-black text-white py-3 px-4 rounded-md w-96"
            onClick={handleSearch}
          >
            SEARCH FOR PROJECTS
          </button>
        </div>
      </div>
    </div>
  );
};

export default Home;