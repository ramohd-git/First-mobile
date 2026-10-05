import SwiftData
import SwiftUI

struct ContentView: View {
    @Environment(\.modelContext) private var modelContext
    @Query(sort: \TaskItem.createdAt, order: .reverse) private var tasks: [TaskItem]
    @State private var newTitle = ""

    var body: some View {
        NavigationStack {
            List {
                Section {
                    HStack {
                        TextField("New task", text: $newTitle)
                            .onSubmit(addTask)
                            .submitLabel(.done)
                        Button("Add", systemImage: "plus.circle.fill", action: addTask)
                            .labelStyle(.iconOnly)
                            .disabled(TaskItem.normalizedTitle(newTitle) == nil)
                    }
                }

                Section {
                    if tasks.isEmpty {
                        ContentUnavailableView(
                            "No tasks yet",
                            systemImage: "checklist",
                            description: Text("Add your first task above.")
                        )
                    } else {
                        ForEach(tasks) { task in
                            TaskRow(task: task)
                        }
                        .onDelete(perform: deleteTasks)
                    }
                }
            }
            .navigationTitle("First Mobile")
            .toolbar {
                if !tasks.isEmpty {
                    EditButton()
                }
            }
        }
    }

    private func addTask() {
        guard let title = TaskItem.normalizedTitle(newTitle) else { return }
        withAnimation {
            modelContext.insert(TaskItem(title: title))
        }
        newTitle = ""
    }

    private func deleteTasks(at offsets: IndexSet) {
        withAnimation {
            for index in offsets {
                modelContext.delete(tasks[index])
            }
        }
    }
}

#Preview {
    ContentView()
        .modelContainer(for: TaskItem.self, inMemory: true)
}
