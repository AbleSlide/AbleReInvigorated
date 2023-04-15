
import React, { useRef, useState } from "react";
import ReactPlayer from 'react-player'
import "./App.css";
import Chatbox from './Chatbox.js';
import Header from './Header.js';
import { GrYoutube } from 'react-icons/gr';
import { AtomLoader } from "react-loaders-kit";
import * as Scroll from 'react-scroll';

function App() {
  const API_ENDPOINT = "/api";
  const urlInputRef = useRef();
  const playerRef = useRef();
  const [url, setUrl] = useState();
  const [progress, setProgress] = useState();
  const [transcriptLoader, showTranscriptLoader] = useState(false);
  const [chatbox, showChatbox] = useState(false);
  const [isPlaying, setPlaying] = useState(false);
  const loaderProps = {
    loading: true,
    size: 80,
    duration: 2,
    colors: ["#FF2900", "#FF5500", "#FFE600"],
  };
  let link = "None";

  function CheckServerStatus() {
    setProgress("Checking server status...");
    fetch(API_ENDPOINT + "/ping")
    .then((response) => {
      if (!response.ok) {
        setProgress("Server is offline. Please try again later.");
        throw new Error(response.status);
      }
      else {
        return response.json();
      }