import React from 'react';
import { useEffect, useState } from 'react';
//import PhotoList from './PhotoList';

export default function Footer(){
    const [sample, setSample] = useState(null);

  useEffect(()=> {
  
    fetch("https://url")
    .then((response) => response.json())
    .then(data => setSample(data))
    .catch(error => console.log('error'.error))  
  }, [])
  return (
    <div className='sample'>
      <h1>Sample입니다</h1>
      <div>{sample}</div>
    </div>
    );
}