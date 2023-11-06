import React from 'react';
import App from './App';
import Page1 from './component/Page1';
import Request from './component/request';
import { BrowserRouter, Routes, Route } from 'react-router-dom';


export default function Routing(){
    return(
        <div className='App'>

            <BrowserRouter>
                <Routes>
                    <Route path='/' element={<App/>}/>
                    <Route path='/page1' element={<Page1/>}/>
                    <Route path='/request' element={<Request/>}/>
                </Routes>
            </BrowserRouter>
        </div>
    )
}