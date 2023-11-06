import { useAuth } from "../context/auth";
import "../style.css";
import Configuracoes from "../componentes/configuracoes";
import Sensores from "../componentes/sensores";
import Atuadores from "../componentes/atuadores";
export const Home = () => {
  const { Logout } = useAuth();

  const handleLogout = () => {
    Logout();
  };

  return (
    <div className="home">
      
      <seticon className="left">
          <Configuracoes/>
            <h2 style={{marginTop: '35px'}} >Dados dos sensores</h2>
            <Sensores/>
        </seticon>
        <section className="right">
          
      <button onClick={handleLogout} className="sair">Logout</button>
           <Atuadores/>
        </section>
    </div>
  );
};