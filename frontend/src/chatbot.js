import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./App.css";

function Chatbot() {
  const [jobs, setJobs] = useState([]);
  const [messages, setMessages] = useState([
    { text: "Hi! I can help you with job interviews.\nType 'show jobs' to see available positions.", sender: "bot" }
  ]);
  const [input, setInput] = useState("");
  const [name, setName] = useState("");
  const [selectedJob, setSelectedJob] = useState(null);
  const chatEndRef = useRef(null);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/jobs")
      .then(res => setJobs(res.data))
      .catch(err => console.log(err));
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = () => {
    if (!input) return;

    const userMsg = { text: input, sender: "user" };
    setMessages(prev => [...prev, userMsg]);
    const lowerInput = input.toLowerCase();

    // Show jobs
    if (lowerInput.includes("show jobs") || lowerInput.includes("available jobs")) {
      if (jobs.length === 0) {
        setMessages(prev => [...prev, { text: "No jobs available.", sender: "bot" }]);
      } else {
        const jobList = jobs.map(j => `${j.id}. ${j.title} (Timeslots: ${j.timeslots.join(", ")})`).join("\n");
        setMessages(prev => [...prev, { text: `Available Jobs:\n${jobList}`, sender: "bot" }]);
      }
      setInput("");
      return;
    }

    // Select job
    if (!selectedJob) {
      const jobId = parseInt(input);
      const job = jobs.find(j => j.id === jobId);
      if (job) {
        setSelectedJob(job);
        setMessages(prev => [...prev, { text: `Selected job: ${job.title}. Available timeslots: ${job.timeslots.join(", ")}`, sender: "bot" }]);
      } else {
        setMessages(prev => [...prev, { text: "Please type a valid Job ID.", sender: "bot" }]);
      }
      setInput("");
      return;
    }

    // Select timeslot
    if (selectedJob) {
      if (selectedJob.timeslots.includes(input)) {
        axios.post("http://127.0.0.1:8000/schedule", {
          job_id: selectedJob.id,
          candidate_name: name || "John Doe",
          timeslot: input
        }).then(res => {
          setMessages(prev => [...prev, { text: res.data.message, sender: "bot" }]);
<<<<<<< HEAD
          setSelectedJob(null); // ✅ Reset only when successful
        }).catch(err => {
          if (err.response && err.response.data && err.response.data.detail) {
            setMessages(prev => [...prev, { text: err.response.data.detail, sender: "bot" }]);
            // ❌ Do not reset selectedJob → user can try another slot directly
          } else {
            setMessages(prev => [...prev, { text: "Error scheduling interview.", sender: "bot" }]);
          }
=======
          setSelectedJob(null);
        }).catch(err => {
          setMessages(prev => [...prev, { text: "Error scheduling interview.", sender: "bot" }]);
>>>>>>> ea46fc23ccbad6d64fff55771f15da52a696783b
        });
      } else {
        setMessages(prev => [...prev, { text: "Invalid timeslot. Please choose a valid timeslot.", sender: "bot" }]);
      }
      setInput("");
      return;
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">Chatbot</div>
      <div className="chat-messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.sender}`}>
            <b>{msg.sender}:</b> {msg.text}
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>

      <div className="input-area">
        <input
          type="text"
          placeholder="Type message..."
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => { if (e.key === "Enter") sendMessage(); }}
        />
        <button onClick={sendMessage}>Send</button>
        <input
          type="text"
          name="name"
          placeholder="Enter your name"
          value={name}
          onChange={e => setName(e.target.value)}
        />
      </div>
    </div>
  );
}

export default Chatbot;
