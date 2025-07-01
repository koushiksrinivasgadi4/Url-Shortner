# Flutter URL Shortener Project

This project is a Flutter application that provides a user-friendly interface for shortening URLs. It connects to a backend service to handle URL shortening requests and displays the results to the user.

## Project Structure

- **lib/**: Contains the main application code.
  - **main.dart**: Entry point of the Flutter application.
  - **screens/**: Contains the different screens of the application.
    - **home_screen.dart**: Home screen layout and logic.
  - **widgets/**: Contains reusable widgets.
    - **custom_button.dart**: Custom button widget.
  - **models/**: Contains data models.
    - **url_model.dart**: Data structure for a URL.
  - **services/**: Contains services for API calls.
    - **api_service.dart**: Handles API interactions for URL shortening.

## Getting Started

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd flutter_frontend
   ```

3. Install the dependencies:
   ```
   flutter pub get
   ```

4. Run the application:
   ```
   flutter run
   ```

## Features

- Shorten URLs easily with a simple interface.
- View original and shortened URLs.
- Reusable components for better maintainability.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.