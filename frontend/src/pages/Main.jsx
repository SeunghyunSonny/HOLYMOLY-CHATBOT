import React, { useEffect, useState } from "react";
import axios from "axios";
import { useSpeechRecognition } from "react-speech-kit";
import { getSpeech } from "../components/getSpeech";
import Nav from "../components/Nav";
import Footer from "../components/Footer";
import styled from "styled-components";
import chat_moly from "../images/chat_moly.png";

const Body_div = styled.div`
	display: flex;
	flex-direction: row;
	justify-content: center; /* 수평 축 가운데 정렬 */
	align-items: center; /* 수직 축 가운데 정렬 */
`;

const Section_div = styled.div({
	width: "40%",
	flexDirection: "column",
	padding: "5px",
	margin: "5px",
	minHeight: "0" /* new */,
	display: "flex",
});

const ChatBox = styled.div`
	display: flex;
	flex-direction: column;
	height: 500px; /* 적절한 높이 설정 */
	border: 1px solid #ccc;
	padding: 10px;
	overflow-y: auto; /* 스크롤 가능하도록 설정 */
`;
const Chat = styled.div`
	align-self: ${(props) =>
		props.sender.includes("user") ? "flex-end" : "flex-start"};
	background-color: ${(props) =>
		props.sender.includes("user") ? "#daf8cb" : "#f1f0f0"};
	max-width: 60%;
	margin-bottom: 10px;
	padding: 5px;
	border-radius: 10px;
`;

const Inputarea = styled.div`
display: flex;
  margin-top: auto; /* 하단에 고정 */
  width: 100%
  padding: 10px
}`;

const InputField = styled.div`
	flex-grow: 1;
	margin-right: 10px;
`;

const SendButton = styled.div`
	width: 100px;
	text-align: center;
`;
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
				"https://3.35.153.170:8000/chat",
				{
					value: value,
				}
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
			<Body_div>
				<Section_div>
					<img src={chat_moly} />
				</Section_div>
				<Section_div>
					<div>
						<h2>moly님과의 대화창</h2>

						<ChatBox>
							{messages.map((message, index) => (
								<Chat
									key={index}
									sender={`message ${message.sender}`}
								>
									{message.text}
								</Chat>
							))}
						</ChatBox>

						{listening && <div>듣는중...</div>}

						<Inputarea>
							<InputField>
								<input
									className="input-field"
									value={value}
									onChange={(e) => setValue(e.target.value)}
									type="text"
									placeholder="채팅을입력하세요"
									style={{
										width: "100%",
										height: "100%",
										boxSizing: "border-box",
										border: "1px solid #ccc",
										padding: "10px",
									}}
								/>
							</InputField>
							<SendButton>
								<button onClick={startListeningInKorean}>
									말하기
								</button>
							</SendButton>
							<SendButton>
								<button onClick={stopListening}>보내기</button>
							</SendButton>
						</Inputarea>
					</div>
					<div></div>
				</Section_div>
			</Body_div>
			<Footer />
		</>
	);
}

export default Main;
