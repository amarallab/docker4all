import React, { Component } from "react";
import {
    Container
} from "@material-ui/core";
import "./ChatPreview.css";
import { ChatMessage } from "./ChatMessage";
import { ChatMessageView } from "./ChatMessageView";
import { io, Socket } from "socket.io-client";

interface InternalChatMessage {
    id: string 
    date: string 
    username: string
    text: string 
}

export interface ChatPreviewProps { }
export interface ChatPreviewState { 
    messages: ChatMessage[];
}

interface ServerToClientEvents {
    prev_messages: (messages: InternalChatMessage[]) => void;
    new_messages: (messages: InternalChatMessage[]) => void;
}
  
interface ClientToServerEvents {
    get_messages: () => void;
    message: (id: string, date: string, username: string, text: string) => void;
}

export class ChatPreview extends Component<ChatPreviewProps, ChatPreviewState> {

    private socket: Socket<ServerToClientEvents, ClientToServerEvents> = io("/chat");

    constructor(props: ChatPreviewProps) {
        super(props);
        this.state = {
            messages: [
            ]
        };
    }

    componentDidMount() {
        this.socket.on("connect", () => {
            this.socket.emit("get_messages");
        });

        this.socket.on("prev_messages", (messages) => {
            this.setState({
                messages: messages.map((value, index) => {
                    return { id: value.id, date: new Date(value.date), username: value.username, text: value.text }
                }).slice(0, 5)
            });
        });
    
        this.socket.on("new_messages", (messages) => {
            this.setState({
                messages: [...this.state.messages, ...messages.map((value, index) => {
                    return { id: value.id, date: new Date(value.date), username: value.username, text: value.text }
                })].sort((a, b) => b.date.valueOf() - a.date.valueOf()).slice(0, 5)
            });
        });    

        this.socket.connect();
    }

    render() {
        return (
            <Container maxWidth="xs">
                {this.state.messages.map( (value, index) => {
                    return <ChatMessageView key={value.id} message={value} />
                })}
            </Container>
        )
    }
}