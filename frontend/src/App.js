import React, {useState} from 'react';
import Joke from './Joke';

function App() {
    const [userQuery, setUserQuery] = useState('');

    const updateUserQuery = (event) => {
        setUserQuery(event.target.value);
    };

    const searchQuery = () => {
        window.open(`https://google.com/search?q=${userQuery}`);
        setUserQuery('');
    };

    const handleKeyPress = (event) => {
        if (event.key === 'Enter') {
            searchQuery();
        }
    };

    return (
        <div className="App">
            <input type="text" value={userQuery} onChange={updateUserQuery} onKeyPress={handleKeyPress}/>
            <button onClick={searchQuery}>Search</button>
            <hr/>
            <Joke></Joke>
        </div>
    );
}

export default App;
