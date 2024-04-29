<p align="center">
  <img src="https://raw.githubusercontent.com/Sayad-Uddin-Tahsin/GlimpseGrid/main/application/assets/Icon.ico" height=100 width=100 alt="GlimpseGrid Logo">
</p>

<p align="center"><a href="https://github.com/Sayad-Uddin-Tahsin/GlimpseGrid/actions/workflows/github-code-scanning/codeql"><img src="https://github.com/Sayad-Uddin-Tahsin/GlimpseGrid/actions/workflows/github-code-scanning/codeql/badge.svg" alt="CodeQL Badge"></a></p>

<h1 align="center">Blink Eye</h1>

GlimpseGrid is a software tool designed to display widgets on the desktop screen, making information easily accessible. It is characterized by its low-weight, highly efficient nature, consuming minimal CPU power.

## Features

- Widget-based Interface: GlimpseGrid offers a widget-based interface, allowing users to customize their desktop screen with a variety of informative widgets.
- Real-time Monitoring: Monitor system resources such as CPU usage and network activity in real-time, providing users with up-to-date information at a glance.
- Low Resource Consumption: Designed with efficiency in mind, GlimpseGrid consumes minimal CPU power and memory, ensuring smooth operation without causing system slowdowns.
- Customization Options: Customize widget appearance and behavior to suit individual preferences, enabling users to personalize their desktop experience.
- User-friendly Interface: GlimpseGrid features an intuitive and easy-to-use interface, making it accessible to users of all experience levels.

## Installation

1. Download the executable file from the [releases page](https://github.com/Sayad-Uddin-Tahsin/GlimpseGrid/releases).
2. Double-click the downloaded file to run the installer.
3. Follow the on-screen instructions to complete the installation process.

## Usage

1. After installation, the installer should launch the application by default if not, double-click the GlimpseGrid executable to launch the application.
2. Drag and drop widgets onto the desktop screen to display them.
3. Customize widget settings as desired.

## Available Widgets
| Name | Description | Preview |
| :---:         |     :---      | :---: |
| CPU Monitor   | Shows realtime CPU usage with update interval of `1` second!     | ![CPU Monitor](https://github.com/Sayad-Uddin-Tahsin/GlimpseGrid/assets/89304780/567b7425-1ad7-444c-82f4-c54894e971bb) |
| Network Monitor     | Shows realtime Network Upload (Optional) and Download Speed with update interval of `0.5` seconds!      | ![Network Monitor](https://github.com/Sayad-Uddin-Tahsin/GlimpseGrid/assets/89304780/a5be3025-4ff9-4e02-a2da-b7af4e767ef3) |

## Contributing

We welcome contributions from the community! Please refer to the [CONTRIBUTING](./CONTRIBUTING.md) file for guidelines on how to contribute to GlimpseGrid development.

### Cloning the repository

Clone this repository:

```console
git clone https://github.com/Sayad-Uddin-Tahsin/GlimpseGrid.git
```

### Required Dependencies

GlimpseGrid relies on essential dependencies to function properly. These dependencies are succinctly listed in the [requirements.txt](./application/requirements.txt) file.

In essence, GlimpseGrid primarily utilizes the following dependencies:

- **customtkinter**: Customtkinter is leveraged for the user interface, providing a tailored and seamless experience for interacting with GlimpseGrid.

- **psutil**: Psutil is utilized for process and system monitoring, enabling GlimpseGrid to read and analyze real-time data on system resource utilization.

Additionally, GlimpseGrid requires the following dependencies:

- **Pillow**: Pillow is used for image processing tasks, enhancing the functionality of GlimpseGrid's user interface.

- **pystray**: Pystray facilitates the integration of GlimpseGrid with the system tray, allowing for convenient access and control of the application.

## Bug Reporting

To report bugs or issues encountered while using GlimpseGrid, please open an issue on the [issue tracker](https://github.com/Sayad-Uddin-Tahsin/GlimpseGrid/issues).

## Security

GlimpseGrid implements security measures to ensure the safety of user data.

## License

GlimpseGrid is licensed under the [MIT License](./LICENSE)
