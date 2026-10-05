import SwiftUI

struct TaskRow: View {
    let task: TaskItem

    var body: some View {
        Button {
            withAnimation { task.toggle() }
        } label: {
            HStack {
                Image(systemName: task.isDone ? "checkmark.circle.fill" : "circle")
                    .foregroundStyle(task.isDone ? Color.accentColor : .secondary)
                Text(task.title)
                    .strikethrough(task.isDone)
                    .foregroundStyle(task.isDone ? .secondary : .primary)
            }
        }
        .buttonStyle(.plain)
        .accessibilityAddTraits(task.isDone ? .isSelected : [])
    }
}
