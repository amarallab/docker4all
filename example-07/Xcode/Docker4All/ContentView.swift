//
//  ContentView.swift
//  Docker4All
//
//  Created by Heliodoro Tejedor Navarro on 2/6/22.
//

import SwiftUI

struct ContentView: View {
    @StateObject var service = ChatService()
    @State var newMessage: String = ""
    @State var editingContact: Bool = false
    @AppStorage("username") var username: String = ""

    var body: some View {
        NavigationView {
            ChatView(messages: service.messages)
                .safeAreaInset(edge: .bottom, spacing: 0) {
                    if service.status == .connected {
                        HStack {
                            Text(newMessage.isEmpty ? "M" : newMessage)
                                .foregroundColor(.clear)
                                .padding(8)
                                .frame(maxWidth: .infinity)
                                .overlay(
                                    TextEditor(text: $newMessage)
                                )
                                .clipShape(RoundedRectangle(cornerRadius: 8))
                            Button {
                                service.send(username: username, text: newMessage)
                                newMessage = ""
                            } label: {
                                Label("Send", systemImage: "paperplane.fill")
                                    .labelStyle(.iconOnly)
                            }
                            .disabled(newMessage.isEmpty || username.isEmpty)
                        }
                        .padding(.vertical, 8)
                        .padding(.horizontal)
                        .background(.thinMaterial)
                    }
                }
                .navigationTitle("Docker4All chat")
                .toolbar {
                    ToolbarItemGroup(placement: .confirmationAction) {
                        Button {
                            editingContact = true
                        } label: {
                            Label("Account", systemImage: "person.circle")
                                .labelStyle(.iconOnly)
                        }
                    }
                }
                .onAppear {
                    service.connect()
                }
                .onDisappear {
                    service.disconnect()
                }
        }
        .fullScreenCover(isPresented: $editingContact) {
            EditContactView(username: username) { newValue in
                if let newValue = newValue {
                    username = newValue
                }
                editingContact = false
            }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
