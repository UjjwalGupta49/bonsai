import React, { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import axios from 'axios'
import { AiOutlineLoading } from 'react-icons/ai'

const Result = () => {
  const router = useRouter()
  const result = router.query.result
  const [github, setGithub] = useState('')
  const [producthunt, setProducthunt] = useState('')
  const [summary, setSummary] = useState('')
  const [gitloading, setGitLoading] = useState(true)
  const [productloading, setProductLoading] = useState(true)
  const [selectedProjects, setSelectedProjects] = useState([])
  const [showModal, setShowModal] = useState(false)
  const [randomRepos, setRandomRepos] = useState([])

  // Function to handle navigation back to the index page
  const handleGoBack = () => {
    router.push('/')
  }

  const getGithubData = async (result) => {
    try {
      const response = await axios.get(
        `https://bonsai-server.onrender.com/github?user_input=${JSON.stringify(result)}`,
      )
      console.log(response.data)
      localStorage.setItem('github', JSON.stringify(response.data))
      return response.data
    } catch (error) {
      console.error('Error fetching GitHub data:', error)
    }
  }

  const getProductData = async () => {
    try {
      const response = await axios.get(`https://bonsai-server.onrender.com/producthunt`)
      console.log(response.data)
      localStorage.setItem('producthunt', JSON.stringify(response.data))
      return response.data
    } catch (error) {
      console.error('Error fetching ProductHunt data:', error)
    }
  }

  const getSummary = async () => {
    try {
      const response = await axios.get(`https://bonsai-server.onrender.com/summary`)
      console.log(response.data)
      localStorage.setItem('producthunt', JSON.stringify(response.data))
      return response.data
    } catch (error) {
      console.error('Error fetching Summary data:', error)
    }
  }


  useEffect(() => {
    const fetchData = async () => {
      setGitLoading(true)
      setProductLoading(true)
      const githubData = await getGithubData(result)
      setGithub(githubData)
      setGitLoading(false)

      const productData = await getProductData()
      setProducthunt(productData)
      setProductLoading(false)

      const summaryData = await getSummary()
      setSummary(summaryData)
    }

    fetchData()
  }, []) // there was result written here

  useEffect(() => {
    if (selectedProjects.length > 2) {
      setShowModal(true) // Show the modal
    } else {
      setShowModal(false) // Hide the modal
    }
  }, [selectedProjects.length])

  // Function to close the modal
  const handleCloseModal = () => {
    setShowModal(false)
  }

  // Function to handle selecting/deselecting projects
  // Function to handle selecting/deselecting projects
  const handleProjectSelect = (projectName) => {
    let newSelectedProjects

    if (selectedProjects.includes(projectName)) {
      // Deselect project
      newSelectedProjects = selectedProjects.filter(
        (project) => project !== projectName,
      )
    } else {
      // Select project
      newSelectedProjects = [...selectedProjects, projectName]
    }

    // Set the new list of selected projects
    setSelectedProjects(newSelectedProjects)
  }
  const getRandomRepos = (repos, count) => {
    // Shuffle array using the Fisher-Yates (Durstenfeld) shuffle algorithm
    for (let i = repos.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1))
      ;[repos[i], repos[j]] = [repos[j], repos[i]]
    }
    // Get first 'count' repos
    return repos.slice(0, count)
  }

  // UseEffect for handling modal visibility
  useEffect(() => {
    if (selectedProjects.length === 3) {
      setShowModal(true)
      setRandomRepos(getRandomRepos([...github], 5))
    } else {
      setShowModal(false)
    }
  }, [selectedProjects, github])

  const Modal = ({ onClose, randomRepos }) => (
    <div className="fixed inset-0 z-50">
      <div
        className="absolute inset-0 bg-black bg-opacity-50"
        onClick={onClose}
      />
      <div className="relative bg-white p-6 rounded-lg shadow-lg m-4 md:m-8 max-h-full overflow-auto">
        <h3 className="text-2xl font-bold mb-4 text-center">
          Random GitHub Repositories
        </h3>
        <ul className="space-y-4">
          {randomRepos.map((repo, index) => (
            <li key={index} className="bg-gray-100 p-4 rounded-md">
              <a
                href={repo.Link}
                target="_blank"
                rel="noopener noreferrer"
                className="text-lg font-semibold text-blue-600 hover:underline"
              >
                {repo['Project Name']}
              </a>
              <p className="text-sm text-gray-700 mt-2">{repo.Description}</p>
              <p className="text-xs text-gray-500 mt-1">
                ⭐ Stars: {repo.star} 🛠️ Issues: {repo.Issue}
              </p>
            </li>
          ))}
        </ul>
        <button
          onClick={onClose}
          className="mt-6 w-full bg-red-500 text-white font-semibold py-2 px-4 rounded hover:bg-red-700 transition duration-300"
        >
          Close
        </button>
      </div>
    </div>
  )

  const renderModal = () => (
    <Modal onClose={handleCloseModal} randomRepos={randomRepos}>
      <p>You have selected {selectedProjects.length} projects.</p>
    </Modal>
  )

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
          <img
            src="/static/images/cloud.png"
            alt="Image 1"
            className="w-8 h-8 rounded-full"
          />
        </div>

        {/* Text content */}
        <div className="flex flex-col ml-0 md:ml-4">
          <div className="flex justify-between mb-2">
            <p className="text-xl md:text-2xl font-bold">Summary</p>
            {/* Top right text */}
            <div className="ml-auto">
              <img
                src="/static/images/bulb.png"
                alt="Image 2"
                className="w-6 h-6 rounded-full mt-0.4"
              />
            </div>
            <p className="text-md md:text-lg font-bold">llama2</p>
          </div>
          <p className="text-md md:text-lg">
            {summary}
          </p>
        </div>
      </div>

      {/* Scrollable container for three boxes */}
      <div className="flex flex-col md:flex-row w-full mt-8 px-2 md:px-4 space-y-4 md:space-y-0 md:space-x-4">
        {/* Projects */}
        <div className="flex flex-col items-center md:w-1/3">
          {/* Image above "Projects" heading */}
          <div className="mb-4">
            <img
              src="/static/images/GitHub logo.svg"
              alt="Project Image"
              width={170}
              height={170}
            />
          </div>
          <h2 className="text-2xl md:text-3xl font-bold text-left mb-4">
            Projects
          </h2>
          <div className="w-72 md:w-96 bg-white rounded-md p-4">
            {/* Iterating over the first 5 GitHub projects */}
            {gitloading ? (
              <div className="flex items-center justify-center h-96">
                <AiOutlineLoading className="animate-spin text-3xl text-purple-500" />
              </div>
            ) : (
              Array.isArray(github) &&
              github
                .sort((a, b) => b.star - a.star)
                .slice(0, 10)
                .map((project, index) => (
                  <div key={index} className="mb-4 last:mb-0">
                    {/* Add tick marking system */}
                    <input
                      type="checkbox"
                      id={`project-${index}`}
                      checked={selectedProjects.includes(
                        project['Project Name'],
                      )}
                      onChange={() =>
                        handleProjectSelect(project['Project Name'])
                      }
                      className="mr-2"
                    />
                    <a
                      href={project.Link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-lg text-gray-700 font-semibold hover:text-blue-600 cursor-pointer"
                    >
                      {project['Project Name'].length > 50
                        ? `${project['Project Name'].substring(0, 50)}...`
                        : project['Project Name']}
                    </a>
                    <p className="text-sm text-gray-700">
                      {project.Description}
                    </p>
                    <p className="text-xs text-gray-500">
                      ⭐ Stars: {project.star}
                    </p>
                  </div>
                ))
            )}
          </div>
        </div>

        {/* Startups */}
        <div className="flex flex-col items-center md:w-1/3">
          {/* Image above "Startups" heading */}
          <div className="mb-4">
            <img
              src="/static/images/g10.svg"
              alt="Startup Image"
              width={170}
              height={170}
            />
          </div>
          <h2 className="text-2xl md:text-3xl font-bold text-center mb-4">
            Startups
          </h2>
          <div className="w-72 md:w-96 bg-white rounded-md p-4">
            {/* Iterating over the product hunt data */}
            {productloading ? (
              <div className="flex items-center justify-center h-96">
                <AiOutlineLoading className="animate-spin text-3xl text-purple-500" />
              </div>
            ) : (
              Array.isArray(producthunt) &&
              producthunt.slice(0, 8).map((product, index) => (
                <div key={index} className="mb-4 last:mb-0">
                  <a
                    href={product.Website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-lg text-gray-700 font-semibold hover:text-producthunt-orange"
                  >
                    {product.Name}
                  </a>
                  <p className="text-sm text-gray-700">{product.Description}</p>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Work Opportunities */}
        <div className="flex flex-col items-center md:w-1/3">
          {/* Image above "Work Opportunities" heading */}
          <div className="mb-4">
            <img
              src="/static/images/issues.svg"
              alt="Work Opportunities Image"
              width={170}
              height={170}
            />
          </div>
          <h2 className="text-2xl md:text-3xl font-bold text-center mb-7">
            Work Opportunities
          </h2>
          <div className="w-72 md:w-96 bg-white rounded-md p-4 overflow-auto">
            {/* Sorting and iterating over GitHub projects based on the number of issues */}
            {gitloading ? (
              <div className="flex items-center justify-center h-96">
                <AiOutlineLoading className="animate-spin text-3xl text-purple-500" />
              </div>
            ) : (
              Array.isArray(github) &&
              [...github]
                .sort((a, b) => b.Issue - a.Issue)
                .slice(0, 10)
                .map((project, index) => (
                  <div key={index} className="mb-4 last:mb-0">
                    <a
                      href={project.Link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-lg text-gray-700 font-semibold hover:text-blue-600"
                    >
                      {project['Project Name']}
                    </a>
                    <p className="text-sm text-gray-700">
                      {project.Description}
                    </p>
                    <p className="text-xs text-gray-500">
                      🛠️ Issues: {project.Issue}
                    </p>
                  </div>
                ))
            )}
          </div>
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
      {/* Conditional rendering of the Modal */}
      {showModal && renderModal()}
    </div>
  )
}

export default Result
