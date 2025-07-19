import React, { useState } from "react";

export default function App() {
  const [theme, setTheme] = useState("light");
  const [devicesFile, setDevicesFile] = useState(null);
  const [connectionsFile, setConnectionsFile] = useState(null);
  const [imageURL, setImageURL] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const toggleTheme = () => {
    setTheme(theme === "light" ? "dark" : "light");
    document.documentElement.classList.toggle("dark");
  };

  const generateDiagram = async () => {
    if (!devicesFile || !connectionsFile) {
      setError("Upload both devices.csv and connections.csv");
      return;
    }

    setLoading(true);
    setError("");
    try {
      const formData = new FormData();
      formData.append("devices", devicesFile);
      formData.append("connections", connectionsFile);

      const res = await fetch("http://localhost:5000/generate-diagram", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || "Server error");
      }

      const blob = await res.blob();
      setImageURL(URL.createObjectURL(blob));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`min-h-screen p-6 ${theme === "dark" ? "bg-gray-900 text-white" : "bg-white text-black"}`}>
      <div className="flex justify-between mb-6 items-center">
        <h1 className="text-2xl font-bold">Network Diagram Generator</h1>
        <button onClick={toggleTheme} className="px-4 py-2 bg-indigo-600 text-white rounded">
          {theme === "dark" ? "Light" : "Dark"} Mode
        </button>
      </div>

      <div className="mb-4">
        <label>Upload Devices CSV:</label>
        <input type="file" accept=".csv" onChange={(e) => setDevicesFile(e.target.files[0])} />

        <label className="block mt-4">Upload Connections CSV:</label>
        <input type="file" accept=".csv" onChange={(e) => setConnectionsFile(e.target.files[0])} />

        <button onClick={generateDiagram} className="mt-4 px-4 py-2 bg-green-600 text-white rounded">
          Generate Diagram
        </button>
      </div>

      {loading && <p className="text-blue-500">Generating diagram...</p>}
      {error && <p className="text-red-500">{error}</p>}

      {imageURL && (
        <div className="mt-6">
          <img src={imageURL} alt="Network Diagram" className="rounded border" />
          <a href={imageURL} download="diagram.png" className="mt-2 block text-green-600 underline">
            Download Diagram
          </a>
        </div>
      )}
    </div>
  );
}
