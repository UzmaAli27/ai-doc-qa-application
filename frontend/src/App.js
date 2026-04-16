import React, { useState, useRef, useEffect } from "react";

function App() {
  const [files, setFiles] = useState([]);
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef(null);

  // Auto scroll to bottom
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleFileChange = (e) => {
    setFiles(e.target.files);
  };

  // Upload PDFs
  const uploadFiles = async () => {
    try {
      const formData = new FormData();

      for (let i = 0; i < files.length; i++) {
        formData.append("files", files[i]);
      }

      await fetch("http://localhost:8000/upload-pdfs", {
        method: "POST",
        body: formData,
      });

      alert("PDFs uploaded successfully!");
    } catch (err) {
      console.error(err);
      alert("Upload failed");
    }
  };

  // Ask question
  const askQuestion = async () => {
    if (!question.trim()) return;

    const userMessage = {
      type: "user",
      text: question,
    };

    setMessages((prev) => [...prev, userMessage]);
    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      const data = await response.json();

      const aiMessage = {
        type: "ai",
        text: data.answer,
        context: data.previous_context,
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (err) {
      console.error(err);

      setMessages((prev) => [
        ...prev,
        {
          type: "ai",
          text: "Error: Unable to fetch response",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // Enter key send
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      askQuestion();
    }
  };

  return (
    <div style={styles.container}>

      {/* LEFT PANEL */}
      <div style={styles.leftPanel}>
        <h2>📄 Documents</h2>

        <input type="file" multiple onChange={handleFileChange} />

        <button style={styles.button} onClick={uploadFiles}>
          Upload PDFs
        </button>
      </div>

      {/* RIGHT PANEL */}
      <div style={styles.rightPanel}>
        <h2>💬 AI Chat</h2>

        {/* CHAT AREA */}
        <div style={styles.chatBox}>
          {messages.map((msg, index) => (
            <div
              key={index}
              style={
                msg.type === "user"
                  ? styles.userMessage
                  : styles.aiMessage
              }
            >
              {msg.text}

              {/* optional context */}
              {msg.context && (
                <div style={styles.context}>
                  <small>Context: {msg.context}</small>
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div style={styles.aiMessage}>
              🤖 Thinking...
            </div>
          )}

          <div ref={chatEndRef} />
        </div>

        {/* INPUT AREA */}
        <div style={styles.inputBox}>
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Ask something about your documents..."
            style={styles.input}
          />

          <button style={styles.button} onClick={askQuestion}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

/* ---------------- STYLES ---------------- */

const styles = {
  container: {
    display: "flex",
    height: "100vh",
    fontFamily: "Arial",
    background: "#f4f4f4",
  },

  /* LEFT */
  leftPanel: {
    width: "25%",
    background: "#ffffff",
    padding: "20px",
    borderRight: "1px solid #ddd",
  },

  /* RIGHT */
  rightPanel: {
    width: "75%",
    display: "flex",
    flexDirection: "column",
    padding: "20px",
  },

  chatBox: {
    flex: 1,
    overflowY: "auto",
    padding: "10px",
    background: "#fafafa",
    borderRadius: "10px",
    marginBottom: "10px",
  },

  inputBox: {
    display: "flex",
    gap: "10px",
  },

  input: {
    flex: 1,
    padding: "12px",
    borderRadius: "8px",
    border: "1px solid #ccc",
  },

  button: {
    padding: "10px 15px",
    background: "#007bff",
    color: "white",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
  },

  /* CHAT BUBBLES */
  userMessage: {
    background: "#007bff",
    color: "white",
    padding: "10px",
    borderRadius: "10px",
    marginBottom: "10px",
    alignSelf: "flex-end",
    maxWidth: "70%",
    marginLeft: "auto",
  },

  aiMessage: {
    background: "#e5e5ea",
    color: "black",
    padding: "10px",
    borderRadius: "10px",
    marginBottom: "10px",
    maxWidth: "70%",
  },

  context: {
    marginTop: "5px",
    fontSize: "12px",
    opacity: 0.7,
  },
};

export default App;