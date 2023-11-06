import * as React from 'react';
import { useEffect, useState } from "react";
import { useAlerta } from '../context/alert';
import { api } from "../lib/api";

import painel from '../assets/painel.png';

export default function Atuadores() {
  const { popupErro } = useAlerta(); 
  const [atuadoresData, setAtuadoresData] = useState([]);
  const [carregamento, setCarregamento] = useState(false);
  const [classeImagem, setClasseImagem] = useState('');
  const [posicao, setPosicao] = useState('Oi');

  const rotacionarImagem = (dado) => {
    let classe = '';
    if (dado === 1) {
      classe = 'inclinar-direita';
    } else if (dado === 2) {
      classe = 'inclinar-esquerda';
    } else if (dado === 3) {
      classe = 'inclinar-cima';
    } else if (dado === 4) {
      classe = 'inclinar-baixo';
    }

    setClasseImagem(classe);
  };

  const fetchData = async () => {
    try {
        const conf = await api.get("/get/atua");
        setAtuadoresData(conf.data);
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
    setCarregamento(false)
    };
  useEffect(() => {
    fetchData();
    const interval = setInterval(() => {
      setCarregamento(true)
      fetchData();
    }, 70000); 
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    atualizar();
  }, [atuadoresData]);

  function atualizar(){
    const dados = [atuadoresData.sensor1, atuadoresData.sensor2, atuadoresData.angulo]
    let sentido="Centro"
    if (dados[0] && dados[2] == 20){
        sentido="Norte"
        rotacionarImagem(4)
    }
    else if  (dados[0] && dados[2] == -20){
        sentido="Sul"
        rotacionarImagem(3)
    }
    else if  (dados[1] && dados[2] == 20){
        sentido="Leste"
        rotacionarImagem(2)
    }
    else if  (dados[1] && dados[2] == -20){
        sentido="Oeste"
        rotacionarImagem(1)
    } else{
      rotacionarImagem(0)
    }
    
    setPosicao(`${sentido}`) 
  }



  return (
    <>
      {carregamento?
      <h2>Atualizando os dados...</h2>:
        <>
         <h3>Posição atual: {posicao}</h3>
        <img id="imagem"  className={classeImagem} src={painel} style={{width:'200px', marginTop:'30px'}} alt="Imagem"/>
        </>
      }
      
    </>
  );
}
