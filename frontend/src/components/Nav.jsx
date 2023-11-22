import * as React from "react";
import Button from "@mui/material/Button";
import { AppBar, CssBaseline, IconButton, Toolbar } from "@mui/material";
import PropTypes from "prop-types";
import useScrollTrigger from "@mui/material/useScrollTrigger";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Slide from "@mui/material/Slide";
import Home from "../pages/Home";
import { useLocation, Link } from "react-router-dom";
import logo from "../images/logo.png";
import Main from "../pages/Main";
import FAQ from "../pages/FAQ";
import Intro from "../pages/Intro";
import Contactus from "../pages/Contactus";
import Login from "../pages/Login";
import { Grid } from "@mui/material";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { yellow } from "@mui/material/colors";
import LoginIcon from "@mui/icons-material/Login";

function HideOnScroll(props) {
	const { children, window } = props;
	// Note that you normally won't need to set the window ref as useScrollTrigger
	// will default to window.
	// This is only being set here because the demo is in an iframe.
	const trigger = useScrollTrigger({
		target: window ? window() : undefined,
	});

	return (
		<Slide appear={false} direction="down" in={!trigger}>
			{children}
		</Slide>
	);
}

HideOnScroll.propTypes = {
	children: PropTypes.element.isRequired,
	/**
	 * Injected by the documentation to work in an iframe.
	 * You won't need it on your project.
	 */
	window: PropTypes.func,
};

export default function HideAppBar(props) {
	const location = useLocation();

	const activeStyle = {
		backgroundColor: "#ff9100",
		color: "white",
	};

	const getStyle = (path) => {
		return location.pathname === path ? activeStyle : {};
	};

	const theme = createTheme({
		palette: {
			primary: yellow,
		},
	});

	return (
		<React.Fragment>
			<ThemeProvider theme={theme}>
				<CssBaseline />
				<HideOnScroll {...props}>
					<AppBar
						position="relative"
						style={{ background: "#FFFFFF" }}
					>
						<Toolbar>
							<Button
								component={Link}
								to="/"
								element={Home}
								sx={{ mr: "5px" }}
							>
								<img
									src={logo}
									width={80}
									height={80}
									alt="logo"
								/>
							</Button>
							<Grid
								container
								spacing={2.0}
								justifyContent="center"
								align="center"
							>
								<Grid item>
									<Button
										variant="contained"
										style={getStyle("/main")}
									>
										<Link
											href="#"
											variant="body2"
											to="/main"
											element={Main}
											style={{
												textDecoration: "none",
												color: "black",
											}}
										>
											{"Holymoly"}
										</Link>
									</Button>
								</Grid>
								<Grid item>
									<Button
										variant="contained"
										style={getStyle("/faq")}
									>
										<Link
											href="#"
											variant="body2"
											to="/faq"
											element={FAQ}
											style={{
												textDecoration: "none",
												color: "black",
											}}
										>
											{"FAQ"}
										</Link>
									</Button>
								</Grid>
								<Grid item>
									<Button
										variant="contained"
										style={getStyle("/contactus")}
									>
										<Link
											href="#"
											variant="body2"
											to="/contactus"
											element={Contactus}
											style={{
												textDecoration: "none",
												color: "black",
											}}
										>
											{"Contact us"}
										</Link>
									</Button>
								</Grid>
								<Grid item>
									<Button
										variant="contained"
										style={getStyle("/intro")}
									>
										<Link
											href="#"
											variant="body2"
											to="/intro"
											element={Intro}
											style={{
												textDecoration: "none",
												color: "black",
											}}
										>
											{"Intro"}
										</Link>
									</Button>
								</Grid>
							</Grid>
							<IconButton
								component={Link}
								to="/login"
								element={Login}
							>
								<LoginIcon />
							</IconButton>
						</Toolbar>
					</AppBar>
				</HideOnScroll>
				<Toolbar />
				<Container>
					<Box sx={{ my: 2 }}>
						{[...new Array(12)].map(() => "").join("\n")}
					</Box>
				</Container>
			</ThemeProvider>
		</React.Fragment>
	);
}
