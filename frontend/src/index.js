import React from "react";
import ReactDOM from "react-dom/client";
import Routing from "./Routing";
import Nav from "./components/Nav";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
	<React.StrictMode>
		<Nav />
		<Routing />
	</React.StrictMode>
);
