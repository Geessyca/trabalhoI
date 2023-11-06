import { createContext, useContext, useEffect, useState } from "react";
import { api } from "../lib/api";
import { useAlerta } from './alert';

const AuthContext = createContext({
    signed: false,
    user: null,
    loading: false,
    Login: ({}) => Promise.resolve(),
    Logout: () => {}
});


export const AuthProvider = ({ children }) => {
  const { popupSuccess, popupErro } = useAlerta(); 
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadStorageData() {
      const storageUser = localStorage.getItem("@Auth:access_email");
      const storageToken = localStorage.getItem("@Auth:access_token");

      if (storageUser && storageToken) {
        setUser(storageUser);
      }
      setLoading(false);
    }
    loadStorageData();
  }, []);

  const Login = async ({ email, password }) => {
    try {
      const res = await api.post("/login", {
        email: email,
        senha: password,
      });
      localStorage.setItem("@Auth:access_token", res.data.token);
      localStorage.setItem("@Auth:access_email", res.data.email);
      window.location.reload()
    } catch (error) {
      if (error.response) {
          if(error.response.status == 500){
              popupErro("Servidor fora do ar")
          }
          else{
              popupErro(error.response.data.erro)
          }
        } 
    }
  };

  const Logout = () => {
    localStorage.clear();
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{ signed: !!user, user, loading, Login, Logout }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};