import React from 'react';
import { Link } from 'react-router-dom';

const Header = () =>{
    return (
        <div className="header" style={ {backgroundColor: "#FF0000"} } >
            <nav className="wrapper">
                <div>
                    <Link className='Logo' to={'/'}>H&M</Link>
                </div>
            </nav>
            <div className="menu">
                <h4>
                    사이드바 버튼 들어갈 위치
                </h4>
            </div>
        </div>
    );
}

export default Header;