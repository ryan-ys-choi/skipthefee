import { useState } from "react";

function App() {
  const [restaurant, setRestaurant] = useState("");
  const [city, setCity] = useState("");
  const [results, setResults] = useState([]);
  const [source, setSource] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const search = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await fetch(
        `http://localhost:8000/search?restaurant=${restaurant}&city=${city}`
      );
      const data = await response.json();
      setResults(data.results);
      setSource(data.source);
    } catch (err) {
      setError("Something went wrong. Is the server running?");
    }

  };

  return (
    <div style={{ maxWidth: "600px", margin: "40px auto", fontFamily: "sans-serif", padding: "0 20px" }}>
      <h1>SkipTheFee</h1>
      <p style={{ color: "gray" }}>Compare food delivery prices across DoorDash, Uber Eats & Grubhub</p>

      <div style={{ display: "flex", gap: "10px", marginTop: "20px" }}>
        <input
          placeholder="Restaurant name"
          value={restaurant}
          onChange={(e) => setRestaurant(e.target.value)}
          style={{ flex: 1, padding: "10px", fontSize: "16px", borderRadius: "8px", border: "1px solid #ddd" }}
        />
        <input
          placeholder="City"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          style={{ flex: 1, padding: "10px", fontSize: "16px", borderRadius: "8px", border: "1px solid #ddd" }}
        />
        <button
          onClick={search}
          style={{ padding: "10px 20px", fontSize: "16px", backgroundColor: "#00b894", color: "white", border: "none", borderRadius: "8px", cursor: "pointer" }}
        >
          Search
        </button>
      </div>

      {loading && <p>Searching...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {results.length > 0 && (
        <div style={{ marginTop: "30px" }}>
          <h2>{results[0].restaurant} — {results[0].city}</h2>
          {source === "ai" && <p style={{ color: "#6c5ce7" }}>Prices estimated by AI — not real time data</p>}
          {source === "database" && <p style={{ color: "#00b894" }}>Real prices from our database</p>}     
          {results.map((r, i) => (
            <div key={i} style={{
              padding: "16px",
              marginBottom: "12px",
              borderRadius: "10px",
              border: i === 0 ? "2px solid #00b894" : "1px solid #ddd",
              backgroundColor: i === 0 ? "#f0fff8" : "white"
            }}>
              {i === 0 && <span style={{ color: "#00b894", fontWeight: "bold" }}>✅ CHEAPEST</span>}
              {r.estimated && <span style={{ color: "#6c5ce7", fontWeight: "bold", marginLeft: "10px" }}>AI Estimated</span>}
              <h3 style={{ margin: "4px 0", textTransform: "capitalize" }}>{r.platform}</h3>
              <p style={{ margin: "4px 0", color: "gray" }}>{r.item_name}</p>
              <p>Item: ${r.item_price} + Delivery: ${r.delivery_fee} + Fees: ${r.service_fee}</p>
              <p style={{ fontWeight: "bold", fontSize: "18px" }}>Total: ${r.total}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
