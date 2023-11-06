import React, { useState, useEffect } from 'react';
import "../style.css";
import { api } from "../lib/api";
import { useAlerta } from '../context/alert';

const Configuracoes = () => {
    const { popupSuccess, popupErro } = useAlerta(); 
    const [openConf, setOpenConf] = useState(false);

    const toggleConfig = () => {
        if (openConf == false) {
        setOpenConf(true)
        } else {
        setOpenConf(false)
        }
    }
    const handleClick = (e) => {
        e.stopPropagation(); 
    };
    const [configuracoes, setConfiguracoes] = useState({});
    const [valorMin, setValorMin] = useState(0);
    const [sensoresAtivos, setSensoresAtivos] = useState({
        sensorNorte: false,
        sensorSul: false,
        sensorLeste: false,
        sensorOeste: false
    });
    const [atuadoresAtivos, setAtuadoresAtivos] = useState({
        horizontal: false,
        vertical: false
    });

    useEffect(() => {
        const fetchData = async () => {
        try {
            const conf = await api.get("/get/conf");
            setConfiguracoes(conf.data);
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

        fetchData();
    }, []);

    useEffect(() => {
        if (configuracoes.valorMin) {
        setValorMin(configuracoes.valorMin);
        setSensoresAtivos({
            sensorNorte: configuracoes.sensorNorte === 1,
            sensorSul: configuracoes.sensorSul === 1,
            sensorLeste: configuracoes.sensorLeste === 1,
            sensorOeste: configuracoes.sensorOeste === 1
        });
        setAtuadoresAtivos({
            horizontal: configuracoes.atuaHoriz === 1,
            vertical: configuracoes.atuaVert === 1
        });
        }
    }, [configuracoes]);

    const handleButton = async () =>{
        const data={
            "atuaHoriz": atuadoresAtivos.horizontal,
            "atuaVert": atuadoresAtivos.vertical,
            "sensorLeste": sensoresAtivos.sensorLeste,
            "sensorNorte": sensoresAtivos.sensorNorte,
            "sensorOeste": sensoresAtivos.sensorOeste,
            "sensorSul": sensoresAtivos.sensorSul,
            "valorMin": valorMin
        }
        try {
            const res = await api.post("/post/conf", data);
            popupSuccess("Dados salvo com sucesso")
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
          setOpenConf(false)
    }

    const handleValorMinChange = (event) => {        
        setValorMin(parseFloat(parseFloat(event.target.value).toFixed(1)))
    };

    const handleSensorChange = (event) => {
        const { name, checked } = event.target;
        setSensoresAtivos({ ...sensoresAtivos, [name]: checked });
    };

    const handleAtuadorChange = (event) => {
        const { name, checked } = event.target;
        setAtuadoresAtivos({ ...atuadoresAtivos, [name]: checked });
    };

    

    return (
    <div className="config-div" onClick={toggleConfig}>
        <h2 className>Configurações</h2>
        <div id="config-content"  style={{display: openConf?'block':'none'}} onClick={handleClick} >
            <label>Valor Min.</label>
            <input type="number" id="numeroCampo" value={valorMin} onChange={handleValorMinChange}   />
            <br /><br />

            <h3>Sensores ativos:</h3>
            <input type="checkbox" name="sensorNorte" id="sensorN" checked={sensoresAtivos.sensorNorte} onChange={handleSensorChange} />
            <label for="sensorN">Sensor Norte</label>
            <input type="checkbox" name="sensorSul" id="sensorS" checked={sensoresAtivos.sensorSul} onChange={handleSensorChange} />
            <label for="sensorS">Sensor Sul</label>
            <input type="checkbox" name="sensorLeste" id="sensorL" checked={sensoresAtivos.sensorLeste} onChange={handleSensorChange} />
            <label for="sensorL">Sensor Leste</label>
            <input type="checkbox" name="sensorOeste" id="sensorO" checked={sensoresAtivos.sensorOeste} onChange={handleSensorChange} />
            <label for="sensorO">Sensor Oeste</label>
            <br /><br />

            <h3>Atuadores ativos:</h3>
            <input type="checkbox" name="horizontal" id="horizontal" checked={atuadoresAtivos.horizontal} onChange={handleAtuadorChange} />
            <label for="horizontal">Horizontal</label>
            <input type="checkbox" name="vertical" id="vertical" checked={atuadoresAtivos.vertical} onChange={handleAtuadorChange} />
            <label for="vertical">Vertical</label>
            <br /><br />

            <button className="buttonAlterar" onClick={handleButton}>Alterar</button>
        </div>
    </div>
    );
};

export default Configuracoes;
