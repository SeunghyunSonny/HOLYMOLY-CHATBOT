import React, { useState } from "react";
import Nav from "../components/Nav";
import Footer from "../components/Footer";
const FORM_ENDPOINT =
	"https://herotofu.com/b9abefe0-88e7-11ee-80e2-e1c752d14c4b"; // TODO - update to the correct endpoint

const Contactus = () => {
	const [submitted, setSubmitted] = useState(false);
	const handleSubmit = (e) => {
		e.preventDefault();

		const inputs = e.target.elements;
		const data = {};

		for (let i = 0; i < inputs.length; i++) {
			if (inputs[i].name) {
				data[inputs[i].name] = inputs[i].value;
			}
		}

		fetch(FORM_ENDPOINT, {
			method: "POST",
			headers: {
				Accept: "application/json",
				"Content-Type": "application/json",
			},
			body: JSON.stringify(data),
		})
			.then((response) => {
				if (!response.ok) {
					throw new Error("Form response was not ok");
				}

				setSubmitted(true);
			})
			.catch((err) => {
				// Submit the form manually
				e.target.submit();
			});
	};

	if (submitted) {
		return (
			<>
				<h2>Thank you!</h2>
				<div>We'll be in touch soon.</div>
			</>
		);
	}

	return (
		<>
			<Nav />
			<form action={FORM_ENDPOINT} onSubmit={handleSubmit} method="POST">
				<div>
					<input
						type="text"
						placeholder="Your name"
						name="name"
						required
					/>
				</div>
				<div>
					<input
						type="email"
						placeholder="Email"
						name="email"
						required
					/>
				</div>
				<div>
					<textarea
						placeholder="Your message"
						name="message"
						required
					/>
				</div>
				<div>
					<button type="submit"> Send a message </button>
				</div>
			</form>
			<Footer />
		</>
	);
};

export default Contactus;
