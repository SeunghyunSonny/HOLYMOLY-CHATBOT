import React, { useState } from "react";
import axios from "axios";
import Nav from "../components/Nav";

const Chatbot = () => {
	const [input, setInput] = useState("");
	const [responses, setResponses] = useState([]);

	const handleInputChange = (e) => {
		setInput(e.target.value);
	};

	const handleSubmit = async () => {
		if (!input.trim()) return;

		try {
			// axios를 사용하여 서버에 요청을 보냅니다.
			const response = await axios.post("http://localhost:8000/chat/", {
				message: input,
			});

			// 챗봇의 응답을 상태에 추가
			setResponses([
				...responses,
				{ query: input, response: response.data },
			]);
			setInput(""); // 입력 필드 초기화
		} catch (error) {
			console.error("Error sending message:", error);
		}
	};

	return (
		<div>
			<Nav />
			<div>
				{responses.map((res, index) => (
					<div key={index}>
						<p>User: {res.query}</p>
						<p>Bot: {res.response}</p>
					</div>
				))}
			</div>
			<input type="text" value={input} onChange={handleInputChange} />
			<button onClick={handleSubmit}>Send</button>
		</div>
	);
};

export default Chatbot;
