import * as React from "react";
import PropTypes from "prop-types";
import Box from "@mui/material/Box";
import Footer from "../components/Footer";
import Nav from "../components/Nav";

function Item(props) {
	const { sx, ...other } = props;
	return (
		<Box
			sx={{
				p: 1,
				m: 1,
				bgcolor: (theme) =>
					theme.palette.mode === "dark" ? "#101010" : "grey.100",
				color: (theme) =>
					theme.palette.mode === "dark" ? "grey.300" : "grey.800",
				border: "1px solid",
				borderColor: (theme) =>
					theme.palette.mode === "dark" ? "grey.800" : "grey.300",
				borderRadius: 2,
				fontSize: "0.875rem",
				fontWeight: "700",
				...sx,
			}}
			{...other}
		/>
	);
}

Item.propTypes = {
	/**
	 * The system prop that allows defining system overrides as well as additional CSS styles.
	 */
	sx: PropTypes.oneOfType([
		PropTypes.arrayOf(
			PropTypes.oneOfType([
				PropTypes.func,
				PropTypes.object,
				PropTypes.bool,
			])
		),
		PropTypes.func,
		PropTypes.object,
	]),
};

export default function FlexDirection() {
	return (
		<>
			<Nav />
			<div style={{ width: "100%", align: "center" }}>
				<Box
					sx={{
						display: "flex",
						flexDirection: "row",
						p: 1,
						m: 1,
						bgcolor: "background.paper",
						borderRadius: 1,
						align: "center",
						margin: "auto",
					}}
				>
					<Item width={500} height={500}>
						Item 1
					</Item>
					<Item width={500} height={500}>
						Item 2
					</Item>
				</Box>
			</div>
			<Footer />
		</>
	);
}