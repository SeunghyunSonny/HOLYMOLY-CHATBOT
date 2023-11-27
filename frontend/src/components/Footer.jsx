import React from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import { Link } from "react-router-dom";

function Copyright() {
	return (
		<Typography variant="body2" color="text.secondary" align="center">
			{"Copyright © "}
			<Link color="inherit" href="https://mui.com/">
				made by JJ
			</Link>{" "}
			{new Date().getFullYear()}
			{"."}
		</Typography>
	);
}

export default function Footer() {
	return (
		<Box sx={{ bgcolor: "background.paper", p: 6 }} component="footer">
			<Typography variant="h6" align="center" gutterBottom>
				H & M
			</Typography>
			<Typography
				variant="subtitle1"
				align="center"
				color="text.secondary"
				component="p"
			>
				Thank you for visiting the Holy-Moly website!
			</Typography>
			<Copyright />
		</Box>
	);
}
