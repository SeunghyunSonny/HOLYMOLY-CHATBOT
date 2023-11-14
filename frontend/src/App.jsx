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
import useStyles from "./styles/styles";

function App() {
	const { classes } = useStyles();

	return (
		<>
			<CssBaseline />
			<AppBar position="relative">
				<Toolbar>
					<HomeIcon />
					<Typography variant="h6">HomeIcon</Typography>
				</Toolbar>
			</AppBar>
			<main>
				<div className={classes.container}>
					<Container maxWidth="sm" style={{ marginTop: "100px" }}>
						<Typography
							variant="h2"
							align="center"
							color="textPrimary"
							gutterBottom
						>
							H & M
						</Typography>
						<Typography
							variant="h5"
							align="h5"
							color="textSecondary"
							marginTop="20px"
							paragraph
						>
							Lorem ipsum dolor sit amet, consectetur adipisicing
							elit. Alias, hic. Fugiat quam dicta necessitatibus
							quas eius quibusdam perferendis odio dolorem
							officia, aliquid deleniti doloribus. Voluptates
							quibusdam veritatis est iure facilis?
						</Typography>
					</Container>
				</div>
				<div>
					<Grid
						container
						spacing={0.5}
						justifyContent="center"
						align="center"
					>
						<Grid item>
							<Button variant="contained" color="primary">
								Get Start
							</Button>
						</Grid>
						<Grid item>
							<Button variant="contained" color="primary">
								Secondary Action
							</Button>
						</Grid>
						<Grid item>
							<Button variant="contained" color="primary">
								Last Action
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
							Lorem ipsum dolor sit amet, consectetur adipisicing
							elit. Quaerat error porro quisquam repudiandae nemo,
							nostrum iusto! Sed incidunt quae a inventore, hic
							facilis cum harum qui, optio reiciendis, quasi
							delectus!
						</Typography>
					</Container>
				</div>
			</main>
		</>
	);
}

export default App;
