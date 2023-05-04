import React, { useRef, useState } from "react";
import QandA from './QandA.js';
import { FiSend } from 'react-icons/fi';
import "./Chatbox.css";

function Chatbox(args) {
    const questionRef = useRef();
    const [chat, setChat] = useState([]);
    function setQuestion(e) {
        questionRef.current.value = e.currentTarget.id;
    }
    function handleQuestionEnter(e) {
        if (e.key === 'Enter') {
          askQuestion();
        }
    }
    function askQuestion() {
        // Ask question
        let text = questionRef.current.value;
        questionRef.current.value = "";
        setChat(oldArray => [["Question", text, []], ...oldArray]);
        const requestOptions = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question: text })
        };
        fetch(args.endpoint + '/ask', requestOptions)
          .then(response => response.json())
       