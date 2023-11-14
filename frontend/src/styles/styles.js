import { makeStyles } from "tss-react/mui";

const useStyles = makeStyles()((theme) => {
	return {
		container: {
			backgroundColor: theme.palette.background.paper,
			padding: theme.spacing(8, 0, 6),
		},
	};
});

export default useStyles;
