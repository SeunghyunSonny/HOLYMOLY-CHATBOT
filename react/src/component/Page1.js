import React from 'react';
import Header from './Header';
import Footer from './Footer';

export default function Page1(){
    return (
        <div className="page1">
            <div>
                <Header/>
            </div>
            <div>
                    <h4>page1입니다</h4>
            </div>
            <div><Footer/></div>
        </div>
    );
}