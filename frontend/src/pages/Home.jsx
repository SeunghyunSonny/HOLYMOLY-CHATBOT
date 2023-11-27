import * as React from "react";
import { Typography, Container } from "@mui/material";
import main_moly from "../images/main_moly.png";
import Nav from "../components/Nav";
import Footer from "../components/Footer";
function Home() {
	return (
		<>
			<Nav />
			<main>
				<div>
					<Container align="center">
						<img
							src={main_moly}
							width={860}
							height={673}
							alt="moly"
						/>
					</Container>
					<Container
						maxWidth="free"
						style={{
							background: "#ffdf00",
						}}
					>
						<Typography
							variant="h4"
							align="left"
							style={{ color: "white" }}
							marginLeft={50}
							gutterBottom
						>
							INTRODUCTION
						</Typography>
						<Typography
							variant="h6"
							align="left"
							style={{ color: "white" }}
							marginTop="20px"
							marginLeft={50}
							paragraph
						>
							HOLY와 MOLY는 여러분의 첫번째 VOICE AI 친구입니다.{" "}
							<br />
							지친 일상에서 벗어나 여러분의 진짜 AI친구와
							대화해보세요!
						</Typography>
					</Container>
				</div>
			</main>
			<Footer />
		</>
	);
}

export default Home;
