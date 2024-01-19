// pages/result.js
import React from 'react';
import { useRouter } from 'next/router';

const Result = () => {
  const router = useRouter();
  const result = router.query.result;

  // Function to handle navigation back to the index page
  const handleGoBack = () => {
    router.push('/');
  };

  return (
    <div className="flex flex-col items-center justify-start min-h-screen bg-gradient-to-b from-orange-500 to-purple-800 text-white">
      <h1 className="text-5xl font-bold mt-3 border-b pb-4">
        {result.replace('Searching for: ', '')}
      </h1>

      {/* Summary white block */}
      <div className="bg-white text-black p-8 mt-8 max-w-3xl rounded-md overflow-hidden mx-4 relative flex items-start">
        {/* Left side images */}
        <div className="flex-shrink-0">
          {/* Add your image source here */}
          <img src="bx-cloud.svg.png" alt="Image 1" className="w-8 h-8 rounded-full" />
        </div>

        {/* Text content */}
        <div className="flex flex-col ml-4">
          <div className="flex justify-between mb-2">
            <p className="text-2xl font-bold">Summary</p>
            {/* Top right text */}
            <div className="ml-auto">
              <img src="bulb.png" alt="Image 2" className="w-6 h-6 rounded-full mt-0.4" />
            </div>
            <p className="text-lg font-bold">llama2</p>
          </div>
          <p className="text-lg">
            This is a summary of the result. You can add your summary text here. This is a summary of the result. You can add your summary text here. This is a summary of the result. You can add your summary text here.
          </p>
        </div>
      </div>

      {/* Scrollable container for three boxes */}
      <div className="flex w-full mt-8 px-4 overflow-y-auto max-h-96">
        {/* Projects */}
        <div className="flex flex-col items-center">
          <h2 className="text-3xl font-bold text-left mb-4">Projects</h2>
          <div className="w-96 h-96 bg-white rounded-md ml-10"></div> {/* Larger white box */}
        </div>

        {/* Startups */}
        <div className="flex flex-col items-center mx-auto">
          <h2 className="text-3xl font-bold text-center mb-4">Startups</h2>
          <div className="w-96 h-96 bg-white rounded-md"></div> {/* Larger white box */}
        </div>

        {/* Open Work */}
        <div className="flex flex-col items-center">
          <h2 className="text-3xl font-bold text-right mb-4">Open Work</h2>
          <div className="w-96 h-96 bg-white rounded-md mr-10"></div> {/* Larger white box */}
        </div>
      </div>

      {/* Back button at the bottom right */}
      <button
        className="fixed bottom-8 right-8 bg-gray-800 p-3 rounded-full"
        onClick={handleGoBack}
      >
      
        <svg
          xmlns="previous.png"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          className="w-6 h-6 text-white"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            d="M15 19l-7-7 7-7"
          />
        </svg>
      </button>
    </div>
  );
};

export default Result;
