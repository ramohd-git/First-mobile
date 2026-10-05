import SwiftData
import SwiftUI

@main
struct FirstMobileApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: TaskItem.self)
    }
}
