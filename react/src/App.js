import React from 'react';
import { Link } from "react-router-dom";


function App() {
  
  return (<div className='App-main' style={ {backgroundColor: "#87CEFA"} }>
            <div className='intro-video'>
              <h4>hello world
                <Link to="/page1">페이지이동버튼</Link>
              </h4>
            </div>
            <div className='content-nav'>
              <h4>nav 컴포넌트?들어갈 위치</h4>
            </div>
            <div className='content-intro'>
              <h4>holy moly intro</h4>
            </div>
            <div className='content-FAQ'>
              <h4>FAQ</h4>
            </div>
            <div className='content-contectus'>
              <h4>contect us</h4>
            </div>
          </div>
  );
}

export default App;
    