//
//  ChatView.swift
//  Docker4All
//
//  Created by Heliodoro Tejedor Navarro on 2/6/22.
//

import SwiftUI

struct ChatView: View {
    var messages: [ChatMessage]
    var body: some View {
        ScrollView {
            ScrollViewReader { proxy in
                LazyVGrid(columns: [.init(.flexible())]) {
                    ForEach(messages) { message in
                        ChatMessageView(message: message, userOwned: true)
                    }
                }
                .padding()
                .onChange(of: messages) { newValue in
                    if let last = newValue.last {
                        withAnimation {
                            proxy.scrollTo(last.id, anchor: .bottom)
                        }
                    }
                }
            }
        }
//        .onChange(of: viewModel.messages, perform: { value in scrollView.scrollTo(viewModel.messages.last!.id, anchor:.bottom)

    }
}

struct ChatView_Previews: PreviewProvider {
    static var previews: some View {
        ChatView(messages: [])
    }
}
