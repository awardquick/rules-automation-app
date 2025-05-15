import RuleEditor from "./pages/RuleEditor";
import { RuleProvider } from "./context/RuleContext";
import "./App.css";

function App() {
  return (
    <RuleProvider>
      <RuleEditor />
    </RuleProvider>
  );
}

export default App;
