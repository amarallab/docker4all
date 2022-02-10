//
//  ChatService.swift
//  Docker4All
//
//  Created by Heliodoro Tejedor Navarro on 2/6/22.
//

import Combine
import Foundation
import SocketIO

class ChatService: ObservableObject {

    enum ConnectStatus {
        case disconnected
        case connecting
        case connected
    }
    
    @Published private(set) var messages: [ChatMessage] = []
    @Published private(set) var status: ConnectStatus = .disconnected
    
    private let manager = SocketManager(socketURL: URL(string: "ws://heltenachat.com")!, config: [.compress, .forceWebsockets(true)])
    private let dateFormatter = ISO8601DateFormatter()
    private var socket: SocketIOClient?
    private var cancellables: Set<AnyCancellable> = []
    
    init() {
        dateFormatter.timeZone = .current
        $status
            .filter { $0 == .connected }
            .sink { _ in
                self.socket?.emit("get_messages")
            }
            .store(in: &cancellables)
    }
    
    public func connect() {
        guard status == .disconnected else { return }
        
        status = .connecting
        let socket = manager.socket(forNamespace: "/chat")
        socket.on(clientEvent: .connect) { data, ack in
            self.status = .connected
        }
        
        socket.on(clientEvent: .disconnect) { data, ack in
            self.status = .disconnected
        }

        socket.on(clientEvent: .error) { data, ack in
            self.disconnect()
        }
        
        socket.on("prev_messages") { [weak self] data, ack in
            self?.messages = []
            self?.addNewMessages(data)
        }

        socket.on("new_messages") { [weak self] data, ack in
            self?.addNewMessages(data)
        }

        socket.connect()
        self.socket = socket
    }
    
    private func addNewMessages(_ data: [Any]) {
        guard let messageList = data.first as? [Any] else { return }
        var currentMessages = self.messages
        for current in messageList {
            guard
                let currentData = current as? [String: Any],
                let idString = currentData["id"] as? String,
                let id = UUID(uuidString: idString),
                let dateString = currentData["date"] as? String,
                let date = dateFormatter.date(from: dateString),
                let username = currentData["username"] as? String,
                let text = currentData["text"] as? String
            else {
                continue
            }
            let newMessage = ChatMessage(id: id, date: date, username: username, text: text)
            currentMessages.append(newMessage)
        }
        self.messages = currentMessages.sorted()
    }
    
    public func send(username: String, text: String) {
        socket?.emit("message", UUID().uuidString, dateFormatter.string(from: Date()), username, text)
    }
    
    public func disconnect() {
        self.socket?.disconnect()
        self.socket = nil
        self.status = .disconnected
    }

}

extension ChatService: Cancellable {
    func cancel() {
        disconnect()
    }
}
