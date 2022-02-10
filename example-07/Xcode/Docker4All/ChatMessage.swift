//
//  ChatMessage.swift
//  Docker4All
//
//  Created by Heliodoro Tejedor Navarro on 2/7/22.
//

import Foundation

struct ChatMessage: Codable, Identifiable, Equatable, Comparable {
    var id: UUID
    var date: Date
    var username: String
    var text: String
    
    static func <(lhs: Self, rhs: Self) -> Bool {
        lhs.date < rhs.date
    }
}

extension ChatMessage {
   static let preview = ChatMessage(id: UUID(), date: Date(), username: "user1", text: "Text")
}
