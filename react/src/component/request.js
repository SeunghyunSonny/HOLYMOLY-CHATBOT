import { useState, useEffect } from 'react';
import axios from 'axios';
import Header from './Header';
import React from 'react';
import Footer from './Footer';

function Request (){
    const [posts, setPosts] = useState([]);

    useEffect(()=>{
      axios.get('https://jsonplaceholder.typicode.com/posts')
            .then(response=>setPosts(response.data))
          }
      ,[]);

    return(
      <div>
        <div><Header/></div>
        <div>{posts.length}</div>
        <div><Footer/></div>
      </div>
    )

}

export default Request;