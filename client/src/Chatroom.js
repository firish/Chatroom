import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Chatroom.css';

function Chatroom() {
    const [selectedUser, setSelectedUser] = useState(null);
    const [messages, setMessages] = useState([]);
    const [users, setUsers] = useState([]);  
    const [loggedInUserName, setLoggedInUserName] = useState(localStorage.getItem('activeUserName'));
    const [loggedInUserId, setLoggedInUserId] = useState(localStorage.getItem('activeUserId'));
    const [inputMessage, setInputMessage] = useState("");
    
    const navigate = useNavigate();

    useEffect(() => {
        const loggedInUserEmail = localStorage.getItem('activeUserEmail'); 
    
        fetch(`http://localhost:5000/get_users?current_user_email=${loggedInUserEmail}`)
        .then(res => res.json())
        .then(data => {
            setUsers(data); // Directly use the returned array of user objects with id and name
        });
    }, []);

    const handleUserClick = (user) => {
        setSelectedUser({
            id: user.id,
            name: user.name
        });
    
        const loggedInUserId = localStorage.getItem('activeUserId');
        fetch(`http://localhost:5000/get_messages?sender_id=${loggedInUserId}&receiver_id=${user.id}`)
        .then(res => res.json())
        .then(data => {
            if (data && data.length) {
                setMessages(data); 
            } else {
                setMessages([]);
            }
        });
    };
    

    const handleLogout = () => {
        localStorage.removeItem('activeUserEmail');
        setLoggedInUserId("");
        setLoggedInUserName("");
        navigate('/login');
    };

    const handleSendMessage = () => {
        if (inputMessage.trim()) {
            const loggedInUserId = localStorage.getItem('activeUserId');
            
            // Call API to save the message
            fetch(`http://localhost:5000/save_message`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    content: inputMessage,
                    sender_id: loggedInUserId,
                    receiver_id: selectedUser.id,
                }),
            })
            .then((res) => res.json())
            .then((data) => {
                // Optionally update the messages array with the new message
                console.log('message saved ::: ', inputMessage, loggedInUserId, selectedUser);
                setMessages([...messages, { content: inputMessage, senderId: loggedInUserId }]);
                setInputMessage('');  // Clear the input after sending
            });
        }
    };    

    return (
        <div className="chatroom">
            <div className="sidebar">
                <p className="logged-in-user">Logged in as: <span className='log-in-name'>{loggedInUserName}</span></p>
                <button className="logout-btn" onClick={handleLogout}>Logout</button>
                <div className="user-list">
                    {users.map(user => (
                        <div 
                            key={user.id} 
                            className="user" 
                            onClick={() => handleUserClick(user)}
                        >
                            {user.name}
                        </div>
                    ))}
                </div>
            </div>

            <div className="chat-screen">
                {selectedUser ? (
                    <>
                        <div className="chat-header">
                            {selectedUser.name}
                        </div>
                        <div className="messages">
                            {messages.length ? (
                                messages.map((msg, index) => (
                                    <div key={index} className={`message ${msg.senderId === loggedInUserId ?  'user-message': 'sender-message'}`}>
                                        {msg.content}
                                        <div className="vote-buttons">
                                            <button>&uarr;</button>
                                            <button>&darr;</button>
                                        </div>
                                    </div>
                                ))
                            ) : (
                                <div className="no-messages">No messages yet</div>
                            )}
                        </div>
                        <div className="chat-input">
                            <input 
                                type="text" 
                                placeholder="Type your message..." 
                                value={inputMessage} 
                                onChange={(e) => setInputMessage(e.target.value)}
                            />
                            <button onClick={handleSendMessage}>Send</button>
                        </div>
                    </>
                ) : (
                    <div className="prompt">Select a user to start chatting</div>
                )}
            </div>
        </div>
    );
}

export default Chatroom;
