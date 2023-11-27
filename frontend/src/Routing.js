import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Main from "./pages/Main";
import FAQ from "./pages/FAQ";
import Contactus from "./pages/Contactus";
import Holymoly from "./pages/Holymoly";
import Error from "./pages/Error";
function Routing() {
	return (
		<div className="App">
			<BrowserRouter>
				<Routes>
					<Route path="/" element={<Home />}></Route>
					<Route path="/login" element={<Login />}></Route>
					<Route path="/main" element={<Main />}></Route>
					<Route path="/faq" element={<FAQ />}></Route>
					<Route path="/contactus" element={<Contactus />}></Route>
					<Route path="/holymoly" element={<Holymoly />}></Route>
					<Route path="/error" element={<Error />}></Route>
				</Routes>
			</BrowserRouter>
		</div>
	);
}

export default Routing;
