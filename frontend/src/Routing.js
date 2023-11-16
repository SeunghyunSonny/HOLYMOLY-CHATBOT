import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Main from "./pages/Main";

//import Signup from './pages/signup/Signup'

function Routing() {
	return (
		<div className="App">
			<BrowserRouter>
				<Routes>
					<Route path="/" element={<Home />}></Route>
					<Route path="/login" element={<Login />}></Route>
					<Route path="/main" element={<Main />}></Route>
				</Routes>
			</BrowserRouter>
		</div>
	);
}

export default Routing;
