import React, { useState, useEffect } from 'react';
import { Button } from './Button.js';
import { NavHashLink as Link } from 'react-router-hash-link';

function NavBar() {
    const [click, setClick] = useState(false);
    const [button, setButton] = useState(true);

    const handleClick = () => setClick(!click);
    const closeMobileMenu = () => setClick(false);

    const showButton = () => {
        if (window.innerWidth <= 960) {
            setButton(false);
        } else {
            setButton(true);
            setClick(false)
        }
    };

    useEffect(() => {
        showButton();
      }, []);
    

    return (
        <>
            <nav className="nav-bar">
                <div className="navbar-container">
                    <div className="menu-icon" onClick={handleClick}>
                        <i className={click ? 'fas fa-times' : 'fas fa-bars'} />
                    </div>
                    <ul className={click ? 'nav-menu active' : 'nav-menu'}>
                        <li>
                            <Link target='_blank' className='nav-links-mobile' onClick={closeMobileMenu} >
                                -
                            </Link>
                        </li>
                    </ul>
                    {button && <Button className='btns' buttonStyle='btn-outline' buttonSize='btn-large' targetURL='_blank'>
                        Bobs
                    </Button>}
                </div>    
            </nav>
        </>
    );
}
export default NavBar;