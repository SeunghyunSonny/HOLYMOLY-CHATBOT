import * as React from "react";
import Button from "@mui/material/Button";
import { AppBar, CssBaseline, Toolbar } from "@mui/material";
import PropTypes from "prop-types";
import useScrollTrigger from "@mui/material/useScrollTrigger";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Slide from "@mui/material/Slide";
import Home from "../pages/Home";
import { Link } from "react-router-dom";
import logo from "../images/logo.png";

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
	return (
		<React.Fragment>
			<CssBaseline />
			<HideOnScroll {...props}>
				<AppBar position="relative" style={{ background: "#FFFFFF" }}>
					<Toolbar>
						<Button
							component={Link}
							to="/"
							element={Home}
							sx={{ mr: "5px" }}
						>
							<img src={logo} width={80} height={80} />
						</Button>
					</Toolbar>
				</AppBar>
			</HideOnScroll>
			<Toolbar />
			<Container>
				<Box sx={{ my: 2 }}>
					{[...new Array(12)].map(() => "").join("\n")}
				</Box>
			</Container>
		</React.Fragment>
	);
}
