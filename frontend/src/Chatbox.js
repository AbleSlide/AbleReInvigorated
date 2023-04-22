import React, { useRef, useState } from "react";
import QandA from './QandA.js';
import { FiSend } from 'react-icons/fi';
import "./Chatbox.css";

function Chatbox(args) {
    const questionRef = useRef();
    const [chat, setChat] = useState([]);
    function setQuestion(e) {
        questionRef.current.value = e.currentTarge