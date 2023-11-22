import * as React from "react";
import Nav from "../components/Nav";
import holymoly from "../images/holymoly.png";
import Footer from "../components/Footer";

export default function Intro() {
	return (
		<div>
			<Nav />
			<div align="center">
				<img src={holymoly} width={1000} height={600} alt="holymoly" />
			</div>
			<Footer />
		</div>
	);
}
