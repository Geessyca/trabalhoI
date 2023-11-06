import { createContext, useContext, useEffect, useState } from "react";
import Alert from '@mui/material/Alert';
import Stack from '@mui/material/Stack';

const AlertaContext = createContext();

export const AlertaProvider = ({ children }) => {
  const [open, setOpen] = useState(false);
  const [alertProps, setAlertProps] = useState({});

  function closeAlert() {
    setOpen(false);
  }

  function popupSuccess(message) {
    setAlertProps({ message, severity: 'success' });
    setOpen(true);
  }

  function popupErro(message) {
    setAlertProps({ message, severity: 'error' });
    setOpen(true);
  }
  useEffect(()=>{
    setTimeout(() => {
      setOpen(false);
    }, 60000);
  },[alertProps])
  return (
    <AlertaContext.Provider
      value={{ popupErro, popupSuccess }}
    >
      {children}
      {open && (
        <Stack sx={{ width: '30%', position: 'fixed', bottom: 16, right: 16, zIndex: 9999 }}>
          <Alert onClose={closeAlert}  severity={alertProps.severity}>
            {alertProps.message}
          </Alert>
        </Stack>
      )}
    </AlertaContext.Provider>
  );
};

export const useAlerta = () => {
  const context = useContext(AlertaContext);
  if (!context) {
    throw new Error("useAlerta must be used within a AlertaProvider");
  }
  return context;
};
