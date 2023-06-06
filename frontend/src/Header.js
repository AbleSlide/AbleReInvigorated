import React from "react";
import './Header.css';
import { BsGithub } from 'react-icons/bs';

function Header() {
	return (
		<div className = "header">
            <div className = "logo">
                <a href="/">
                    <img src="/logo512.png" alt="Logo" style={{
                        width: "50px", height:"50px"
                    }}/>
                </a>
            </div>
            <div className = "github"