import 'package:flutter/material.dart';
import 'dart:async';
import 'package:socket_io_client/socket_io_client.dart' as IO;

void main() {
  runApp(MindYourDriveApp());
}

class MindYourDriveApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: MindYourDriveScreen(),
    );
  }
}

class MindYourDriveScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xFFB3DFF8), Color(0xFFEBF7FC)],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: SafeArea(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              const Column(
                children: [
                  SizedBox(height: 30),
                  Text(
                    "Welcome To",
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.w400, color: Colors.black87),
                  ),
                  SizedBox(height: 10),
                  Text(
                    "Mind Your Drive",
                    style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: Colors.black87),
                  ),
                  SizedBox(height: 20),
                  Padding(
                    padding: EdgeInsets.symmetric(horizontal: 40.0, vertical: 50.0),
                    child: Text(
                      "Drive with confidence knowing we’ve got your back",
                      textAlign: TextAlign.center,
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.w400, color: Colors.black87),
                    ),
                  ),
                ],
              ),
              Container(
                margin: const EdgeInsets.symmetric(horizontal: 20),
                padding: const EdgeInsets.all(30),
                height: 400,
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(20),
                  boxShadow: const [BoxShadow(color: Colors.black12, blurRadius: 10, offset: Offset(0, 5))],
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Image.asset('assets/brain.png', height: 100, width: 100, color: Colors.grey[700]),
                    const SizedBox(height: 20),
                    const Text(
                      "Please gently put your device across your forehead and click continue when ready",
                      textAlign: TextAlign.center,
                      style: TextStyle(fontSize: 14, color: Colors.black87),
                    ),
                    const SizedBox(height: 20),
                    ElevatedButton(
                      onPressed: () {
                        Navigator.push(context, MaterialPageRoute(builder: (context) => InstructionsPage()));
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFFB3DFF8),
                        padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 10),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
                      ),
                      child: const Text(
                        "Continue",
                        style: TextStyle(fontSize: 16, color: Colors.white, fontWeight: FontWeight.bold),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// instructions

class InstructionsPage extends StatefulWidget {
  @override
  _InstructionsPageState createState() => _InstructionsPageState();
}

class _InstructionsPageState extends State<InstructionsPage> {
  bool _showFirstWarning = true;

  void _toggleWarning() {
    setState(() {
      _showFirstWarning = !_showFirstWarning;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0.0,
        leading: IconButton(
          icon: Icon(Icons.arrow_back),
          onPressed: () {
            Navigator.pop(context); // Navigate back to the previous screen
          },
        ),
      ),
      body: GestureDetector(
        onTap: _toggleWarning,
        child: Container(
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              colors: [Color(0xFFEBF7FC), Color(0xFFB3DFF8)], // Soft gradient
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
            ),
          ),
          child: SafeArea(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Instructions Box
                  Container(
                    padding: const EdgeInsets.all(16.0),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(16.0),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black12,
                          blurRadius: 8.0,
                          offset: Offset(0, 2),
                        ),
                      ],
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Center(
                          child: const Text(
                            "Instructions",
                            style: TextStyle(
                              fontSize: 20,
                              fontWeight: FontWeight.bold,
                              color: Colors.black87,
                            ),
                          ),
                        ),
                        const SizedBox(height: 8),
                        const Text(
                          "Mind Your Drive helps keep drivers safe.\n\n"
                          "Our fatigue-measuring headband analyzes brain activity in real-time.\n\n"
                          "Increased fatigue may trigger one of two alarms:\n",
                          textAlign: TextAlign.left,
                          style: TextStyle(
                            fontSize: 18,
                            color: Colors.black87,
                            height: 1.5,
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 24),
                  // Expanded Warning Box with Animation
                  Expanded(
                    child: AnimatedSwitcher(
                      duration: const Duration(milliseconds: 500),
                      child: _showFirstWarning
                          ? _buildWarningBox(
                              key: const ValueKey("FirstWarning"),
                              title: "Alert.",
                              message:
                                  "Fatigue levels rising; consider taking a break.",
                              description:
                                  "A short chime will play.\n No action required.",
                              headerColor:
                                  const Color(0xFFFFF9CC), // Pastel Yellow
                              hasDismissButton: false,
                              actionLabel:
                                  "No Action Required", // Label for yellow warning
                            )
                          : _buildWarningBox(
                              key: const ValueKey("SecondWarning"),
                              title: "Warning!",
                              message:
                                  "Significant drowsiness; please safely pull over.",
                              description:
                                  "A loud alarm will play periodically until dismissed.",
                              headerColor:
                                  const Color(0xFFFFE4E4), // Pastel Red
                              hasDismissButton: true,
                            ),
                    ),
                  ),
                  const SizedBox(height: 16),
                  Center(
                    child: const Text(
                      "Tap to see the two warnings",
                      style: TextStyle(
                        fontSize: 14,
                        color: Colors.black54,
                        fontStyle: FontStyle.italic,
                      ),
                    ),
                  ),
                  const SizedBox(height: 16),
                  Center(
                    child: ElevatedButton(
                      onPressed: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) =>
                                NextPage(), // Replace with your next page
                          ),
                        );
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFFD6B8B8),
                        padding: const EdgeInsets.symmetric(
                            horizontal: 40, vertical: 15),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(30),
                        ),
                      ),
                      child: const Text(
                        "Continue",
                        style: TextStyle(
                          fontSize: 16,
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: 20),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  // Helper method to build warning box with an optional Dismiss button or label
  Widget _buildWarningBox({
    required Key key,
    required String title,
    required String message,
    required String description,
    required Color headerColor,
    required bool hasDismissButton,
    String? actionLabel,
  }) {
    return Container(
      key: key, // Use the provided key for AnimatedSwitcher
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16.0),
        boxShadow: [
          BoxShadow(
            color: Colors.black12,
            blurRadius: 8.0,
            offset: Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header directly touching the top of the box
          Container(
            width: double.infinity,
            padding: const EdgeInsets.symmetric(vertical: 10.0),
            decoration: BoxDecoration(
              color: headerColor,
              borderRadius: const BorderRadius.only(
                topLeft: Radius.circular(16.0),
                topRight: Radius.circular(16.0),
              ),
            ),
            child: Text(
              title,
              textAlign: TextAlign.center,
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: Colors.black87,
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(20.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Text(
                  message,
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    fontSize: 20,
                    color: Colors.black87,
                    height: 1.4,
                  ),
                ),
                const SizedBox(height: 20),
                Text(
                  description,
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    fontSize: 16,
                    color: Colors.black54,
                    height: 1.4,
                  ),
                ),
                const SizedBox(height: 20), // Increased space before the button
                if (actionLabel != null)
                  Container(
                    padding: const EdgeInsets.symmetric(
                        vertical: 8.0, horizontal: 10.0),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(20.0),
                      border: Border.all(color: Colors.black12),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black12,
                          blurRadius: 2.0,
                          offset: Offset(0, 2),
                        ),
                      ],
                    ),
                    child: Text(
                      actionLabel,
                      style: const TextStyle(
                        color: Colors.black54,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ),
                if (hasDismissButton)
                  ElevatedButton.icon(
                    onPressed: () {
                      // Handle Dismiss Alarm action
                    },
                    icon: const Icon(
                      Icons.notifications_off,
                      color: Colors.black54,
                    ),
                    label: const Text(
                      "Dismiss Alarm",
                      style: TextStyle(
                        color: Colors.black54,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.white,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(20.0),
                      ),
                      elevation: 2,
                      side: const BorderSide(color: Colors.black12),
                    ),
                  ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class NextPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0.0,
      ),
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [
              Color(0xFFE3F2FD),
              Color(0xFFBBDEFB)
            ], // Gradient background
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: SafeArea(
          child: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Container(
                  padding: const EdgeInsets.all(100.0),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(16.0),
                    boxShadow: [
                      BoxShadow(
                        color: const Color.fromRGBO(0, 0, 0, 0.122),
                        blurRadius: 8.0,
                        offset: Offset(0, 2),
                      ),
                    ],
                  ),
                  child: Column(
                    children: [
                      const Text(
                        "You're All Set",
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: Colors.black87,
                        ),
                      ),
                      const SizedBox(height: 8),
                      const Text(
                        "Happy driving!",
                        style: TextStyle(
                          fontSize: 18,
                          color: Colors.black54,
                        ),
                      ),
                      const SizedBox(height: 20),
                      CircleAvatar(
                        radius: 40,
                        backgroundColor: Colors.grey[200],
                        child: Image.asset(
                          'assets/brain.png',
                          height: 100,
                          width: 100,
                          color: const Color.fromARGB(255, 255, 150, 150),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 40),
                ElevatedButton(
                  onPressed: () {
                    {
                      // Navigate to the menu screen
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                            builder: (context) => CountdownScreen()),
                      );
                    }
                    ;
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(
                        horizontal: 40, vertical: 15),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(30),
                    ),
                    side: BorderSide(
                        color: const Color.fromARGB(0, 96, 125, 139)),
                    elevation: 4,
                  ),
                  child: const Text(
                    "Start Driving",
                    style: TextStyle(
                      fontSize: 16,
                      color: Color.fromARGB(255, 134, 215, 255),
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class CountdownScreen extends StatefulWidget {
  @override
  _CountdownScreenState createState() => _CountdownScreenState();
}

class _CountdownScreenState extends State<CountdownScreen> {
  int _countdown = 5;

  @override
  void initState() {
    super.initState();
    // Start the countdown
    Timer.periodic(Duration(seconds: 1), (Timer timer) {
      setState(() {
        if (_countdown > 0) {
          _countdown--;
        } else {
          timer.cancel();
          // Navigate to the Drive Screen
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(builder: (context) => DriveScreen()),
          );
        }
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Text(
          "Starting in $_countdown",
          style: TextStyle(fontSize: 36),
        ),
      ),
    );
  }
}

class DriveScreen extends StatefulWidget {
  @override
  _DriveScreenState createState() => _DriveScreenState();
}

class _DriveScreenState extends State<DriveScreen> {
  int _warning = 0; // Initial warning level
  late IO.Socket socket;

  @override
  void initState() {
    super.initState();
    _connectToSocket();
  }

  void _connectToSocket() {
    socket = IO.io('http://127.0.0.1:5000', <String, dynamic>{
      'transports': ['websocket'],
      'autoConnect': true,
    });

    socket.on('connect', (_) {
      print('Connected to the server');
    });

    socket.on('update_warning', (data) {
      print('Received data: $data'); // Debug print
      setState(() {
        _warning = data['warning'] ?? 0; // Update warning state with data from server
      });
    });

    socket.on('disconnect', (_) {
      print('Disconnected from the server');
    });
  }

  @override
  void dispose() {
    socket.dispose(); // Clean up the socket connection
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0.0,
        leading: IconButton(
          icon: Icon(Icons.arrow_back, color: Colors.black),
          onPressed: () {
            Navigator.pop(context); // Navigate back to the previous screen
          },
        ),
      ),
      body: Stack(
        children: [
          Container(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [Color(0xFFE3F2FD), Color(0xFFBBDEFB)],
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
              ),
            ),
            child: Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  if (_warning == 0)
                    Text("No Warnings", style: TextStyle(fontSize: 24, color: Colors.black54)),
                ],
              ),
            ),
          ),
          if (_warning == 1)
            _buildWarningBox(
              key: ValueKey("FirstWarning"),
              title: "Alert!",
              message: "Fatigue levels rising; consider taking a break.",
              description: "A short chime will play. No action required.",
              headerColor: Color(0xFFFFF9CC),
              hasDismissButton: false,
            ),
          if (_warning == 2)
            _buildWarningBox(
              key: ValueKey("SecondWarning"),
              title: "Warning!",
              message: "Significant drowsiness; please safely pull over.",
              description: "A loud alarm will play periodically until dismissed.",
              headerColor: Color(0xFFFFE4E4),
              hasDismissButton: true,
            ),
        ],
      ),
    );
  }

  Widget _buildWarningBox({
    required Key key,
    required String title,
    required String message,
    required String description,
    required Color headerColor,
    required bool hasDismissButton,
  }) {
    return Positioned(
      top: 30,
      left: 20,
      right: 20,
      child: Container(
        key: key,
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16.0),
          boxShadow: [BoxShadow(color: Colors.black12, blurRadius: 8.0, offset: Offset(0, 2))],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              width: double.infinity,
              padding: const EdgeInsets.symmetric(vertical: 10.0),
              decoration: BoxDecoration(
                color: headerColor,
                borderRadius: const BorderRadius.only(
                  topLeft: Radius.circular(16.0),
                  topRight: Radius.circular(16.0),
                ),
              ),
              child: Text(
                title,
                textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.black87),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  Text(
                    message,
                    textAlign: TextAlign.center,
                    style: const TextStyle(fontSize: 20, color: Colors.black87, height: 1.4),
                  ),
                  const SizedBox(height: 20),
                  Text(
                    description,
                    textAlign: TextAlign.center,
                    style: const TextStyle(fontSize: 16, color: Colors.black54, height: 1.4),
                  ),
                  const SizedBox(height: 20),
                  if (hasDismissButton)
                    ElevatedButton.icon(
                      onPressed: () {
                        // Handle Dismiss Alarm action
                      },
                      icon: const Icon(Icons.notifications_off, color: Colors.black54),
                      label: const Text(
                        "Dismiss Alarm",
                        style: TextStyle(color: Colors.black54, fontWeight: FontWeight.w500),
                      ),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.white,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20.0)),
                        elevation: 2,
                        side: const BorderSide(color: Colors.black12),
                      ),
                    ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}