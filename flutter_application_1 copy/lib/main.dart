import 'package:flutter/material.dart';
import 'dart:async';
import 'package:http/http.dart' as http;
import 'dart:convert';


Future<Map<String, dynamic>> fetchWarnings() async {
  final response = await http.get(Uri.parse('http://192.168.1.87:5001/process-eeg'));
  if (response.statusCode == 200) {
    return jsonDecode(response.body);
  } else {
    throw Exception('Failed to load warning data');
  }
}

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
            colors: [
              Color(0xFFB3DFF8),
              Color(0xFFEBF7FC)
            ], // Light blue gradient
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
                  SizedBox(height: 30), // Padding from the top
                  Text(
                    "Welcome To",
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.w400,
                      color: Colors.black87,
                    ),
                  ),
                  SizedBox(height: 10),
                  Text(
                    "Mind Your Drive",
                    style: TextStyle(
                      fontSize: 32,
                      fontWeight: FontWeight.bold,
                      color: Colors.black87,
                    ),
                  ),
                  SizedBox(height: 20),
                  Padding(
                    padding: EdgeInsets.symmetric(
                      horizontal: 40.0,
                      vertical: 50.0,
                    ),
                    child: Text(
                      "Drive with confidence knowing we’ve got your back",
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w400,
                        color: Colors.black87,
                      ),
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
                  boxShadow: const [
                    BoxShadow(
                      color: Colors.black12,
                      blurRadius: 10,
                      offset: Offset(0, 5),
                    ),
                  ],
                ),
                child: Column(
                  mainAxisAlignment:
                      MainAxisAlignment.center, // Center vertically
                  crossAxisAlignment:
                      CrossAxisAlignment.center, // Center horizontally
                  children: [
                    Image.asset(
                      'assets/brain.png',
                      height: 100,
                      width: 100,
                      color: Colors.grey[700],
                    ),
                    const SizedBox(height: 20),
                    const Text(
                      "Please gently put your device across your forehead and click continue when ready",
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        fontSize: 14,
                        color: Colors.black87,
                      ),
                    ),
                    const SizedBox(height: 20),
                    ElevatedButton(
                      onPressed: () {
                        // Navigate to the new page
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => InstructionsPage(),
                          ),
                        );
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor:
                            const Color(0xFFB3DFF8), // Light blue color
                        padding: const EdgeInsets.symmetric(
                            horizontal: 30, vertical: 10),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(20),
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
                            builder: (context) => DrivesOverviewScreen()),
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

class DrivesOverviewScreen extends StatefulWidget {
  @override
  _DrivesOverviewScreenState createState() => _DrivesOverviewScreenState();
}

class _DrivesOverviewScreenState extends State<DrivesOverviewScreen> {
  late Future<Map<String, dynamic>> _warningData;

  @override
  void initState() {
    super.initState();
    // Fetch the warning data when the screen is initialized
    _warningData = fetchWarnings();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Your Drives"),
        actions: [
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: () {
              setState(() {
                _warningData = fetchWarnings();
              });
            },
          ),
        ],
      ),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _warningData,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else if (snapshot.hasData) {
            final data = snapshot.data!;
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    "Theta/Beta Ratio: ${data['theta_beta_ratio'].toStringAsFixed(2)}",
                    style: TextStyle(fontSize: 18),
                  ),
                  Text(
                    "Alpha/Theta Ratio: ${data['alpha_theta_ratio'].toStringAsFixed(2)}",
                    style: TextStyle(fontSize: 18),
                  ),
                  Text(
                    "Warning Level: ${data['warning'] == 2 ? 'Severe' : data['warning'] == 1 ? 'Mild' : 'None'}",
                    style: TextStyle(
                      fontSize: 20,
                      color: data['warning'] == 2
                          ? Colors.red
                          : data['warning'] == 1
                              ? Colors.orange
                              : Colors.green,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            );
          } else {
            return Center(child: Text('No data available'));
          }
        },
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

class _DriveScreenState extends State<DriveScreen>
    with SingleTickerProviderStateMixin {
  int _countdown = 5;
  bool _showCountdown = true;
  bool _showWarning = false;
  late AnimationController _controller;
  late Animation<double> _brainSlideAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: Duration(milliseconds: 500),
      vsync: this,
    );
    _brainSlideAnimation =
        Tween<double>(begin: 0, end: 200).animate(_controller);

    // Start the countdown
    Timer.periodic(Duration(seconds: 1), (Timer timer) {
      setState(() {
        if (_countdown > 0) {
          _countdown--;
        } else {
          timer.cancel();
          _showCountdown = false; // Hide the countdown
          _controller.forward(); // Start the brain animation
          Future.delayed(Duration(seconds: 5), () {
            setState(() {
              _showWarning = true; // Show the warning after 5 seconds
            });
          });
        }
      });
    });
  }

  @override
  void dispose() {
    _controller.dispose();
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
                  if (_showCountdown)
                    Text(
                      "Starting in $_countdown",
                      style:
                          TextStyle(fontSize: 36, fontWeight: FontWeight.bold),
                    ),
                  if (!_showCountdown && !_showWarning)
                    AnimatedBuilder(
                      animation: _controller,
                      builder: (context, child) {
                        return Transform.translate(
                          offset: Offset(0, _brainSlideAnimation.value),
                          child: CircleAvatar(
                            radius: 100,
                            backgroundColor: Colors.green[300],
                            child: Image.asset(
                              'assets/brain.png',
                              height: 100,
                              width: 100,
                              color: Colors.grey[700],
                            ),
                          ),
                        );
                      },
                    ),
                ],
              ),
            ),
          ),
          if (_showWarning)
            Positioned(
              top: 30, // Adjusted position to move warning box higher
              left: 20,
              right: 20,
              child: _buildWarningBox(
                key: ValueKey("WarningBox"),
                title: "Warning!",
                message: "Significant drowsiness; please safely pull over.",
                description:
                    "A loud alarm will play periodically until dismissed.",
                headerColor: Color(0xFFFFE4E4), // Pastel Red for the header
                hasDismissButton: true,
              ),
            ),
        ],
      ),
    );
  }

  // Your existing _buildWarningBox method
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
      key: key,
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
