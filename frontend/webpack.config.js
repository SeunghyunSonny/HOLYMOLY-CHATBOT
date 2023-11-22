module.exports = {
	// 다른 설정들...

	module: {
		rules: [
			{
				test: /\.js$/, // .js 파일에 대한 정규 표현식
				exclude: /node_modules/, // node_modules 폴더는 제외
				use: {
					loader: "babel-loader",
					options: {
						presets: ["@babel/preset-env"],
					},
				},
			},
			// 다른 로더 설정들...
		],
	},
};
