//
//  EditContactView.swift
//  Docker4All
//
//  Created by Heliodoro Tejedor Navarro on 2/8/22.
//

import SwiftUI

struct EditContactView: View {
    @State var username: String = ""
    var close: (String?) -> Void
    
    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Personal data")) {
                    TextField("Username", text: $username)
                }
            }
            .navigationTitle("Edit Contact")
            .toolbar {
                ToolbarItemGroup(placement: .confirmationAction) {
                    Button {
                        close(username)
                    } label: {
                        Text("Save")
                    }
                }
                ToolbarItemGroup(placement: .cancellationAction) {
                    Button {
                        close(nil)
                    } label: {
                        Text("Cancel")
                    }
                }
            }
        }
    }
}

struct EditContactView_Previews: PreviewProvider {
    static var previews: some View {
        EditContactView() { value in
        }
    }
}
