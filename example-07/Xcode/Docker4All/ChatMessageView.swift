//
//  ChatMessageView.swift
//  Docker4All
//
//  Created by Heliodoro Tejedor Navarro on 2/7/22.
//

import SwiftUI

struct ChatMessageView: View {
    var message: ChatMessage
    var userOwned: Bool
    
    var time: String {
        let dateFormatter = DateFormatter()
        dateFormatter.timeStyle = .short
        dateFormatter.dateStyle = .none
        return dateFormatter.string(from: message.date)
    }
    
    var body: some View {
        HStack {
            if userOwned {
                Spacer()
            }
            VStack(alignment: userOwned ? .trailing : .leading) {
                Text(message.username)
                    .font(.caption)
                Text(message.text)
                    .multilineTextAlignment(.leading)
                    .padding(10)
                    .foregroundColor(userOwned ? Color.white : Color.white)
                    .background(userOwned ? Color.blue : Color.gray)
                    .cornerRadius(10)
                Text(verbatim: time)
                    .font(.caption2)
            }
            
            if !userOwned {
                Spacer()
            }
        }
        .padding(.vertical, 8)
    }
}

struct ChatMessageView_Previews: PreviewProvider {
    static var previews: some View {
        VStack {
            ChatMessageView(message: .preview, userOwned: true)
            ChatMessageView(message: .preview, userOwned: false)
        }
        .padding()
        .previewLayout(.fixed(width: 200, height: 250))
    }
}
