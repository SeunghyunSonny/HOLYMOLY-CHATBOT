import React, { useEffect, useState } from "react";
import axios from "axios";
import { useSpeechRecognition } from "react-speech-kit";
import { getSpeech } from "../components/getSpeech";
import Nav from "../components/Nav";
import Footer from "../components/Footer";

function Main() {
	//
	useEffect(() => {
		window.speechSynthesis.getVoices();
	}, []);

	const [value, setValue] = useState("");
	const [messages, setMessages] = useState([]);

	const startListeningInKorean = () => listen({ lang: "ko-KR" });

	const { listen, listening, stop } = useSpeechRecognition({
		onResult: (result) => {
			setValue(result);
		},
	});
	const stopListening = () => {
		if (value) {
			handleResponse(value);
			addMessage(value, "user");
		}
		stop();
	};

	const sendValueToServer = async (value) => {
		try {
			const response = await axios.post(
				"https://your-server.com/api/endpoint",
				{ value: value }
			);
			return response.data;
		} catch (error) {
			console.error("서버로 데이터를 보내는데 실패했습니다:", error);
			return null;
		}
	};

	async function handleResponse(value) {
		const serverResponse = await sendValueToServer(value);
		if (serverResponse) {
			getSpeech(serverResponse);
			addMessage(serverResponse, "server");
		}
	}

	const addMessage = (text, sender) => {
		setMessages((prevMessages) => [...prevMessages, { text, sender }]);
	};

	return (
		<>
			<Nav />
			<div>
				<h2>holy와 대화하기</h2>
				<div>{value}</div>
				<p>마이크감지: {listening ? "작동 o " : "작동 x "}</p>
				<button onClick={startListeningInKorean}>말하기</button>
				<button onClick={stopListening}>중지</button>
				{listening && <div>듣는중...</div>}

				<div className="chat-box">
					{messages.map((message, index) => (
						<div
							key={index}
							className={`message ${message.sender}`}
						>
							{message.text}
						</div>
					))}
				</div>
			</div>
			<Footer />
		</>
	);
}

export default Main;
