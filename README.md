# First Mobile

A starter iOS app built with **SwiftUI** and **SwiftData**. It ships with a
simple task list (add, complete, swipe to delete, persisted on device) as a
placeholder feature to build on.

## Requirements

- macOS with **Xcode 16** or newer
- iOS 17+ (simulator or device)

## Run it

1. Open `FirstMobile.xcodeproj` in Xcode.
2. Pick an iPhone simulator in the toolbar.
3. Press **⌘R** to run, or **⌘U** to run the tests.

To run on a physical iPhone, select the **FirstMobile** target →
*Signing & Capabilities* and choose your Apple ID team. Change the bundle
identifier (`com.ramohd.FirstMobile`) if Xcode reports it's taken.

From the command line:

```sh
xcodebuild test -project FirstMobile.xcodeproj -scheme FirstMobile \
  -destination 'platform=iOS Simulator,name=iPhone 16'
```

## Project layout

```
FirstMobile/
  FirstMobileApp.swift   App entry point; sets up the SwiftData container
  Models/TaskItem.swift  SwiftData model
  Views/                 SwiftUI screens and components
  Assets.xcassets        App icon and accent color
FirstMobileTests/        Unit tests (Swift Testing)
agent/                   A Python AI agent that manages a to-do list (see agent/README.md)
```

The project uses Xcode 16 folder-synchronized groups, so any file you add to
`FirstMobile/` or `FirstMobileTests/` is picked up automatically — no need to
add it to the project by hand.

## CI

`.github/workflows/ios.yml` builds the app and runs the tests on a macOS
GitHub Actions runner for every push and pull request.
