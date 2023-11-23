import * as React from "react";
import Nav from "../components/Nav";
import Footer from "../components/Footer";

export default function Intro() {
	return (
		<div>
			<Nav />
			<div className="body">
				<div className="section">
					<button>Talk with Holy</button>
				</div>
				<div className="section">
					<button>Talk with Moly</button>
				</div>
			</div>
			<Footer />
		</div>
	);
}
