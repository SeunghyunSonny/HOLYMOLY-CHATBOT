import React from 'react';
import Header from './component/Header';
import Footer from './component/Footer';
//import Daylists from './component/Daylists';
import {BrowserRouter, Route, Routes} from "react-router-dom";


function App() {
  
  return (
    <BrowserRouter>
      <div className ="App">
        <Header/>
        
        <Routes>
          <Route exact path="/day" element={<Footer/>}/>
        </Routes>
       </div>
    </BrowserRouter>
  );
}

export default App;
    