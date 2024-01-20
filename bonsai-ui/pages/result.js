import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';

const Result = () => {
  const router = useRouter();
  const result = router.query.result;
  const [github, setGithub] = useState('');
  const [producthunt, setProducthunt] = useState('');

  // Function to handle navigation back to the index page
  const handleGoBack = () => {
    router.push('/');
  };

  const getGithubData = async (result) => {
    try {
      const response = await axios.get(`http://127.0.0.1:5000/github?user_input=${JSON.stringify(result)}`);
      console.log(response.data);
      localStorage.setItem('github', JSON.stringify(response.data));
      return response.data;
    } catch (error) {
      console.error('Error fetching GitHub data:', error);
    }
  };

  const getProductData = async () => {
    try {
      const response = await axios.get(`http://127.0.0.1:5000/producthunt`);
      console.log(response.data);
      localStorage.setItem('producthunt', JSON.stringify(response.data));
      return response.data;
    } catch (error) {
      console.error('Error fetching ProductHunt data:', error);
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      const githubData = await getGithubData(result);
      setGithub(githubData);

      const productData = await getProductData();
      setProducthunt(productData);
    };

    fetchData();
  }, [result]);
  return (
    <div className="flex flex-col items-center justify-start min-h-screen bg-gradient-to-b from-orange-500 to-purple-800 text-white">
      <h1 className="text-3xl md:text-5xl font-bold mt-3 border-b pb-4">
        {result}
      </h1>
      
      {/* Summary white block */}
      <div className="bg-white text-black p-4 md:p-8 mt-8 max-w-full md:max-w-3xl rounded-md overflow-hidden mx-2 md:mx-4 relative flex flex-col md:flex-row items-start">
        {/* Left side images */}
        <div className="flex-shrink-0 mb-4 md:mb-0">
          {/* Add your image source here */}
          <img src="/static/images/cloud.png" alt="Image 1" className="w-8 h-8 rounded-full" />
        </div>

        {/* Text content */}
        <div className="flex flex-col ml-0 md:ml-4">
          <div className="flex justify-between mb-2">
            <p className="text-xl md:text-2xl font-bold">Summary</p>
            {/* Top right text */}
            <div className="ml-auto">
              <img src="/static/images/bulb.png" alt="Image 2" className="w-6 h-6 rounded-full mt-0.4" />
            </div>
            <p className="text-md md:text-lg font-bold">llama2</p>
          </div>
          <p className="text-md md:text-lg">
            This is a summary of the result. You can add your summary text here. This is a summary of the result. You can add your summary text here. This is a summary of the result. You can add your summary text here.
          </p>
        </div>
      </div>

      {/* Scrollable container for three boxes */}
      <div className="flex flex-col md:flex-row w-full mt-8 px-2 md:px-4 overflow-auto">
        {/* Projects */}
        <div className="flex flex-col items-center mb-8 md:mb-0">
          {/* Image above "Projects" heading */}
          <div className="mb-4">
            <img src="/static/images/GitHub logo.svg" alt="Project Image" width={170} height={170} />
          </div>
          <h2 className="text-2xl md:text-3xl font-bold text-left mb-4">Projects</h2>
          <div className="min-w-72 md:min-w-96 min-h-72 md:min-h-96 bg-white rounded-md p-4 overflow-auto">
          </div>
 {/* Larger white box */}
        </div>

        {/* Startups */}
        <div className="flex flex-col items-center mb-8 md:mb-0 md:mx-auto">
          {/* Image above "Startups" heading */}
          <div className="mb-4">
            <img src="/static/images/g10.svg" alt="Startup Image" width={170} height={170} />
          </div>
          <h2 className="text-2xl md:text-3xl font-bold text-center mb-4">Startups</h2>
          <div className="min-w-72 md:min-w-96 min-h-72 md:min-h-96 bg-white rounded-md p-4 overflow-auto"></div>
 {/* Larger white box */}
        </div>

        {/* Open Work */}
        <div className="flex flex-col items-center">
          {/* Image above "Open Work" heading */}
          <div className="mb-4">
            <img src="/static/images/issues.svg" alt="Open Work Image" width={170} height={170} />
          </div>
          <h2 className="text-2xl md:text-3xl font-bold text-right mb-4">Open Work</h2>
          <div className="w-72 md:w-96 h-72 md:h-96 bg-white rounded-md mr-0 md:mr-10" /> {/* Larger white box */}
        </div>
      </div>

      {/* Back button at the bottom right */}
      <button
        className="fixed bottom-8 right-8 bg-gray-800 p-3 rounded-full"
        onClick={handleGoBack}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
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
