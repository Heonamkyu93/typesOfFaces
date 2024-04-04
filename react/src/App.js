import './App.css';
import { BrowserRouter,Routes,Route } from 'react-router-dom';
import Layout from './common/layout/Layout';
import Upimg from './component/upimg/Upimg';
function App() {
  return (
  <>
    <BrowserRouter>
    <Routes>
    <Route path="/" element={<Layout/>}>
    <Route index element={<Upimg/>} />



    </Route>

    
    </Routes>
    </BrowserRouter>
  </>
    );
}

export default App;
