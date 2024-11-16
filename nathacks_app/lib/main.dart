import 'package:flutter/material.dart';
import 'home_screen.dart'; // Import the HomeScreen file

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Mind Your Drive',
      home: HomeScreen(), // Set HomeScreen as the home widget
    );
  }
}

