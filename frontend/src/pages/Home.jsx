import * as React from "react";
import { Typography, Container } from "@mui/material";
import useStyles from "../styles/styles";
import moly from "/Users/jj/Documents/GitHub/HOLYMOLY-CHATBOT/frontend/src/images/moly.png";
import Nav from "../components/Nav";
import Footer from "../components/Footer";
function Home() {
	const { classes } = useStyles();

	return (
		<>
			<Nav />
			<main>
				<div className={classes.container}>
					<Container align="center">
						<img src={moly} width={860} height={673} alt="moly" />
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
