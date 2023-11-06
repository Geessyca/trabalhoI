import * as React from 'react';
import { useEffect, useState } from "react";
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { useAlerta } from '../context/alert';
import { api } from "../lib/api";


export default function Sensores() {
  const { popupErro } = useAlerta(); 
  const [sensorData, setSensorData] = useState([]);
  const [carregamento, setCarregamento] = useState(false)
  const fetchData = async () => {
    try {
        const sens = await api.get("/get/sens");
        setSensorData(sens.data);
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
    }, 60000); 
    return () => clearInterval(interval);
  }, []);



  return (
    <>
      {carregamento?
      <h2>Atualizando os dados...</h2>:
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 500 }} >
          <TableBody>        
            
           {sensorData.map((row) => (
              <TableRow key={`${row.Id}+${row.Data}`}>
                <TableCell>{row.Data}<span className='nomes'>Data </span></TableCell>
                <TableCell>{row.Norte}<span className='nomes'>Norte </span></TableCell>
                <TableCell>{row.Sul}<span className='nomes'> Sul</span></TableCell>
                <TableCell>{row.Leste}<span className='nomes'> Leste</span></TableCell>
                <TableCell>{row.Oeste}<span className='nomes'>Oeste </span></TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      }
    </>
  );
}
