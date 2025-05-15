import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import RuleEditor from "./pages/RuleEditor";
import Home from "./pages/Home";
import { RuleProvider } from "./context/RuleContext";
import "./App.css";

function App() {
  return (
    <Router>
      <RuleProvider>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/rules/new" element={<RuleEditor />} />
        </Routes>
      </RuleProvider>
    </Router>
  );
}

export default App;
