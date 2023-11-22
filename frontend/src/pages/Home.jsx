import * as React from "react";
import Button from "@mui/material/Button";
import {
	Typography,
	AppBar,
	Card,
	CardActions,
	CardContent,
	CardMedia,
	CssBaseline,
	Grid,
	Toolbar,
	Container,
} from "@mui/material";
import HomeIcon from "@mui/icons-material/Home";
import ButtonGroup from "@mui/material/Button";
import useStyles from "../styles/styles";
import { Link } from "react-router-dom";
import Login from "./Login";
import Main from "./Main";
import FAQ from "./FAQ";
import Contactus from "./Contactus";
import moly from "/Users/jj/Documents/GitHub/HOLYMOLY-CHATBOT/frontend/src/images/moly.png";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { yellow } from "@mui/material/colors";
import Nav from "../components/Nav";
function Home() {
	const { classes } = useStyles();
	const theme = createTheme({
		palette: {
			primary: yellow,
		},
	});

	return (
		<>
			<Nav />
			<main>
				<ThemeProvider theme={theme}>
					<div align="center">
						<img src={moly} width={860} height={660} />
					</div>
					<div className={classes.container}>
						<Container
							maxWidth="free"
							style={{
								background: "#e3b217",
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
								HOLY와 MOLY는 여러분의 첫번째 VOICE AI
								친구입니다. <br />
								지친 일상에서 벗어나 여러분의 진짜 AI친구와
								대화해보세요!
							</Typography>
						</Container>
					</div>
					<div>
						<Grid
							container
							spacing={2.0}
							justifyContent="center"
							align="center"
						>
							<Grid item>
								<Button variant="contained">
									<Link
										href="#"
										variant="body2"
										to="/main"
										element={Main}
									>
										{"HolyMoly"}
									</Link>
								</Button>
							</Grid>
							<Grid item>
								<Button variant="contained">
									<Link
										href="#"
										variant="body2"
										to="/faq"
										element={FAQ}
									>
										{"FAQ"}
									</Link>
								</Button>
							</Grid>
							<Grid item>
								<Button variant="contained" color="primary">
									<Link
										href="#"
										variant="body2"
										to="/contactus"
										element={Contactus}
									>
										{"Contact us"}
									</Link>
								</Button>
							</Grid>
						</Grid>
					</div>
					<div className={classes.container}>
						<Container>
							<Typography
								variant="h2"
								align="center"
								color="textPrimary"
								gutterBottom
							>
								Lorem ipsum dolor sit amet, consectetur
								adipisicing elit. Quaerat error porro quisquam
								repudiandae nemo, nostrum iusto! Sed incidunt
								quae a inventore, hic facilis cum harum qui,
								optio reiciendis, quasi delectus!
							</Typography>
						</Container>
					</div>
					<div>
						<Link to="/Login" element={Login}>
							LOGIN
						</Link>
					</div>
					<div>
						<Link
							href="#"
							variant="body2"
							to="/main"
							element={Main}
						>
							{"login"}
						</Link>
					</div>
				</ThemeProvider>
			</main>
		</>
	);
}

export default Home;
