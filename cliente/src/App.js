import { AuthProvider } from "./context/auth";
import { AlertaProvider } from "./context/alert";
import { Routes } from "./routes";

function App() {
  return (
    <AlertaProvider>
      <AuthProvider>
        <Routes />
      </AuthProvider>
    </AlertaProvider>
  );
}

export default App;