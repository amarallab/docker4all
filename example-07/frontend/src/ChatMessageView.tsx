import React, { Component } from "react";
import { ChatMessage } from "./ChatMessage";
import "./ChatMessageView.css";

export interface ChatMessageProps {
    message: ChatMessage
}

export interface ChatMessageState { }

export class ChatMessageView extends Component<ChatMessageProps, ChatMessageState> {

    constructor(props: ChatMessageProps) {
        super(props);
        this.state = {
        };
    }

    render() {
        return (
            <div className="message">
                <div className="date">{this.props.message.date.toLocaleTimeString()}</div>
                <div className="bubble">
                    <div className="text">
                        {this.props.message.text}
                    </div>
                </div>
                <div className="user">{this.props.message.username}</div>
            </div>
        )
    }
}