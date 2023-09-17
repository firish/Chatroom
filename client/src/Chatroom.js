import React, { useEffect, useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import './Chatroom.css';
import UserContext from './UserContext';
import Globals from './globals';

function Chatroom() {
    const { loggedInUser } = useContext(UserContext);
    console.log(loggedInUser);
    
    const [selectedUser, setSelectedUser] = useState(null);
    const [messages, setMessages] = useState([]);
    const [users, setUsers] = useState([]);  
    const [loggedInUserName, setLoggedInUserName] = useState(localStorage.getItem('activeUserName'));
    const [loggedInUserId, setLoggedInUserId] = useState(String(localStorage.getItem('activeUserId')));
    const [inputMessage, setInputMessage] = useState("");
    const [voteUpdate, setVoteUpdate] = useState(false); 


    
    const navigate = useNavigate();

    const upvoteMessage = (messageId) => {
        fetch(`http://localhost:5000/upvote_message`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: loggedInUserId,
                message_id: messageId,
            }),
        })
        .then(() => {
            if (selectedUser) {
                handleUserClick(selectedUser); // Fetch all messages for the current chat after upvoting
            }
        });
    };
    
    const downvoteMessage = (messageId) => {
        fetch(`http://localhost:5000/downvote_message`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: loggedInUserId,
                message_id: messageId,
            }),
        })
        .then(() => {
            if (selectedUser) {
                handleUserClick(selectedUser); // Fetch all messages for the current chat after downvoting
            }
        });
    };

    useEffect(() => {
        // Get the reload flag
        fetch(`http://localhost:5000/get_reload`)
        .then(res => res.json())
        .then(data => {
            if (!data.reload) {
                // If reload is false, we reload the page and immediately flip the reload flag
                fetch(`http://localhost:5000/flip_reload`, { method: 'POST' })
                .then(() => {
                    window.location.reload();
                })
                .catch(err => {
                    console.error("Error flipping reload:", err);
                });
            }
        })
        .catch(err => {
            console.error("Error fetching reload:", err);
        });
    
        const loggedInUserEmail = localStorage.getItem('activeUserEmail'); 
        setLoggedInUserName(localStorage.getItem('activeUserName'));
        
        fetch(`http://localhost:5000/get_users?current_user_email=${loggedInUserEmail}`)
        .then(res => res.json())
        .then(data => {
            setUsers(data);
        });
    }, []);


    const handleUserClick = (user) => {
        setSelectedUser({
            id: user.id,
            name: user.name
        });
    
        setLoggedInUserId(localStorage.getItem('activeUserId'));
        fetch(`http://localhost:5000/get_messages?sender_id=${loggedInUserId}&receiver_id=${user.id}`)
        .then(res => res.json())
        .then(data => {
            if (data && data.length) {
                // Fetch likes for each message and update state
                const promises = data.map(message => 
                    fetch(`http://localhost:5000/get_likes?message_id=${message.id}`)
                    .then(res => res.json())
                    .then(likeData => {
                        message.like_value = likeData.like_value;
                        return message;
                    })
                );
    
                Promise.all(promises).then(updatedMessages => {
                    setMessages(updatedMessages);
                });
    
            } else {
                setMessages([]);
            }
        });
    };
    

    

    const handleLogout = () => {
        localStorage.removeItem('activeUserEmail');
        localStorage.removeItem('activeUserName');
        localStorage.removeItem('activeUserId');
        setLoggedInUserId("");
        setLoggedInUserName("");
        
        // Flip the reload state
        fetch(`http://localhost:5000/flip_reload`, { method: 'POST' })
        .then(() => {
            navigate('/login');
        })
        .catch(err => {
            console.error("Error flipping reload on logout:", err);
            // You might still want to navigate to login even if the flip fails
            navigate('/login');
        });
    };

    const handleSendMessage = () => {
        if (inputMessage.trim()) {
            setLoggedInUserId(localStorage.getItem('activeUserId'));
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
                console.log(data)
                console.log('message saved ::: ', inputMessage, loggedInUserId, loggedInUserName, selectedUser.name);
                setMessages([...messages, { content: inputMessage, sender_id: loggedInUserId, like_value: 0 }]);
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
                                messages.map((msg, index) => {
                                    console.log('Message Sender ID:', msg.sender_id, loggedInUserId); // Add this line
                                
                                    return (
                                        <div key={index} className={`message ${String(msg.sender_id) === String(loggedInUserId) ?  'sender-message':'user-message'}`}>
                                            {msg.content}
                                            <div className="vote-buttons">
                                                <button 
                                                    className={msg.like_value > 0 ? "active-upvote" : "no-vote"}
                                                    onClick={() => upvoteMessage(msg.id)}
                                                >&uarr;</button>
                                                <span className="like-value-box">{msg.like_value}</span>
                                                <button 
                                                    className={msg.like_value < 0 ? "active-downvote" : "no-vote"}
                                                    onClick={() => downvoteMessage(msg.id)}
                                                >&darr;</button>
                        </div>
                                        </div>
                                    );
                                })
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
