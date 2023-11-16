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
import { useNavigate } from "react-router-dom";
import Home from "../pages/Home";

export default function Nav() {
	return (
		<>
			<CssBaseline />
			<AppBar position="relative">
				<Toolbar>
					<HomeIcon />
					<Typography variant="h6" marginLeft="10px">
						H & M
					</Typography>
				</Toolbar>
			</AppBar>
		</>
	);
}
