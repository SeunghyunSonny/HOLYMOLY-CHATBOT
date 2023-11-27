import React from "react";
import Nav from "../components/Nav";
import Footer from "../components/Footer";

function FAQ() {
	// 게시글 목록을 나타내는 임시 데이터
	const posts = [
		{
			id: 1,
			title: "첫 번째 게시글",
			author: "홍길동",
			date: "2023-01-01",
		},
		{
			id: 2,
			title: "두 번째 게시글",
			author: "김철수",
			date: "2023-01-02",
		},
		// 추가 게시글...
	];

	return (
		<div>
			<Nav />
			<h1>자유게시판</h1>
			<table>
				<thead>
					<tr>
						<th>번호</th>
						<th>제목</th>
						<th>작성자</th>
						<th>작성일</th>
					</tr>
				</thead>
				<tbody>
					{posts.map((post) => (
						<tr key={post.id}>
							<td>{post.id}</td>
							<td>{post.title}</td>
							<td>{post.author}</td>
							<td>{post.date}</td>
						</tr>
					))}
				</tbody>
			</table>
			<Footer />
		</div>
	);
}

export default FAQ;
