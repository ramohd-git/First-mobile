import Foundation
import SwiftData
import Testing
@testable import FirstMobile

struct TaskItemTests {
    @Test func newTaskStartsNotDone() {
        let task = TaskItem(title: "Buy milk")
        #expect(task.title == "Buy milk")
        #expect(task.isDone == false)
    }

    @Test func toggleFlipsDoneState() {
        let task = TaskItem(title: "Walk dog")
        task.toggle()
        #expect(task.isDone)
        task.toggle()
        #expect(!task.isDone)
    }

    @Test(arguments: [
        ("  Hello  ", "Hello"),
        ("\nTrim me\t", "Trim me"),
        ("Plain", "Plain"),
    ])
    func normalizedTitleTrims(input: String, expected: String) {
        #expect(TaskItem.normalizedTitle(input) == expected)
    }

    @Test(arguments: ["", "   ", "\n\t"])
    func normalizedTitleRejectsBlank(input: String) {
        #expect(TaskItem.normalizedTitle(input) == nil)
    }

    @MainActor
    @Test func persistsInModelContext() throws {
        let container = try ModelContainer(
            for: TaskItem.self,
            configurations: ModelConfiguration(isStoredInMemoryOnly: true)
        )
        let context = container.mainContext
        context.insert(TaskItem(title: "Persist me"))
        try context.save()

        let fetched = try context.fetch(FetchDescriptor<TaskItem>())
        #expect(fetched.count == 1)
        #expect(fetched.first?.title == "Persist me")
    }
}
