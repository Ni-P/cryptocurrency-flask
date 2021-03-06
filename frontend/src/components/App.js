import React, {useEffect, useState} from 'react';
import {Link} from 'react-router-dom';
import logo from '../assets/logo.png'
import {API_BASE_URL} from "../config";

function App() {

    const [walletInfo, setWalletInfo] = useState({});

    useEffect(() => {
        fetch(`${API_BASE_URL}/wallet/info`)
            .then(response => response.json())
            .then(json => setWalletInfo(json));
    }, []);

    let {address, balance} = walletInfo;

    return (
        <div className="App">
            <img src={logo} alt="application-logo" className="logo"/>
            <h3>Welcome to pychain</h3>
            <br/>
            <Link to="/blockchain">Blockchain</Link>
            <Link to="/conduct-transaction">Transaction</Link>
            <Link to="/transaction-pool">Transaction Pool</Link>
            <br/>
            <div>Address: {address}</div>
            <div>Balance: {balance}</div>
        </div>
    );
}

export default App;
