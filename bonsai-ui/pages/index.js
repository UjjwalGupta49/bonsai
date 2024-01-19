// pages/index.js
import { useRouter } from 'next/router';
import React, { useState } from 'react';

const Home = () => {
  const router = useRouter();
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleSearch = () => {
    // Implement your search functionality here
    const result = `Searching for: ${inputValue}`;

    // Redirect to result page with query parameter
    router.push(`/result?result=${result}`);
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
