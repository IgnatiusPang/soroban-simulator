# Mobile App Conversion Tasks

This document outlines the tasks required to convert the Soroban Simulator from a Python desktop application to a mobile application that runs on iOS and Android devices.

The recommended approach is to rewrite the application using **Flutter with the Dart programming language**. This will provide the best performance, a consistent UI across platforms, and access to a modern, well-supported mobile development ecosystem.

## Phase 1: Project Setup

1.  **Set up Flutter Development Environment**:
    *   Install the Flutter SDK.
    *   Set up an editor (VS Code or Android Studio).
    *   Install the Flutter and Dart plugins.
    *   Configure platform-specific tools (Xcode for iOS, Android SDK for Android).

2.  **Create a New Flutter Project**:
    *   Create a new Flutter project for the Soroban Simulator.
    *   Set up the project structure, including folders for UI, logic, and assets.

## Phase 2: UI Development

1.  **Design the Mobile UI**:
    *   Adapt the existing desktop UI for mobile screens (both phones and tablets).
    *   Create a responsive layout that works in both portrait and landscape modes.

2.  **Create the Soroban Widget**:
    *   Develop a custom Flutter widget to represent the soroban.
    *   The widget should be able to display the rods, beads, and frame.
    *   Beads should be interactive (movable via touch).

3.  **Build the Main Screen**:
    *   Create the main application screen, including the soroban widget, the input field for calculations, and the display for the current number and steps.
    *   Implement the layout for both phone and tablet screen sizes.

## Phase 3: Business Logic Implementation

1.  **Rewrite Calculation Logic in Dart**:
    *   Translate the existing Python calculation logic for addition, subtraction, and multiplication into Dart.
    *   The existing Python code in `soroban_simulator/soroban/` will serve as a reference.
    *   Ensure the logic for bead movements and step-by-step calculations is accurately ported.

2.  **Implement the Parser**:
    *   Rewrite the expression parser from `soroban_simulator/soroban/parser.py` in Dart to handle mathematical expressions.

## Phase 4: State Management

1.  **Choose a State Management Solution**:
    *   Select a state management library for Flutter (e.g., Provider, BLoC, Riverpod).
    *   Provider or Riverpod are good starting points for this project's complexity.

2.  **Implement State Management**:
    *   Manage the application's state, including:
        *   The current calculation.
        *   The list of calculation steps.
        *   The position of each bead on the soroban.
        *   The current number displayed.

## Phase 5: Testing

1.  **Write Unit Tests**:
    *   Write unit tests for the calculation logic and parser in Dart.
    *   Ensure the results match the Python implementation.

2.  **Write Widget Tests**:
    *   Write widget tests for the Soroban widget and other UI components.
    *   Verify that the UI updates correctly based on the application's state.

3.  **Write Integration Tests**:
    *   Write integration tests to test the full application flow, from entering a calculation to seeing the result.

## Phase 6: Platform-Specific Adjustments

1.  **iOS Adjustments**:
    *   Ensure the app follows Apple's Human Interface Guidelines.
    *   Test the app on different iPhone and iPad models.

2.  **Android Adjustments**:
    *   Ensure the app follows Google's Material Design guidelines.
    *   Test the app on a variety of Android phones and tablets.

## Phase 7: Deployment

1.  **Prepare for Release**:
    *   Create app icons and splash screens.
    *   Configure the app's bundle ID and version number.

2.  **Deploy to Google Play Store**:
    *   Create a Google Play Developer account.
    *   Build a release version of the app for Android.
    *   Upload the app to the Google Play Store.

3.  **Deploy to Apple App Store**:
    *   Enroll in the Apple Developer Program.
    *   Build a release version of the app for iOS.
    *   Submit the app to the App Store for review.
