import * as React from "react";
import Nav from "../components/Nav";
import Footer from "../components/Footer";
import "../styles/holymoly.css";
import holy from "../images/holy.png";
import moly from "../images/moly.png";
import Main from "./Main";
import Error from "./Error";
import { Link } from "react-router-dom";

export default function Intro() {
	return (
		<div className="intro">
			<Nav />
			<div className="body">
				<div className="section">
					<div className="buttondiv">
						<Link to="/error" element={Error}>
							<button className="button">Talk with Moly</button>
						</Link>
					</div>
					<div className="imgdiv">
						<img className="img" src={holy} />
					</div>
				</div>
				<div className="section">
					<div className="buttondiv">
						<Link to="/main" element={Main}>
							<button className="button">Talk with Moly</button>
						</Link>
					</div>
					<div className="imgdiv">
						<img className="img" src={moly} />
					</div>
				</div>
			</div>
			<Footer />
		</div>
	);
}
