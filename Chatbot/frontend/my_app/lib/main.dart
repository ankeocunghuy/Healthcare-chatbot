import 'package:flutter/material.dart';
import 'homepage.dart';


// The main entry point of the Flutter app
void main() {
 runApp(const MyApp());
}


// Root widget of the app, extends StatelessWidget because it doesn't hold any state
class MyApp extends StatelessWidget {
 const MyApp({Key? key}) : super(key: key);


 // Build method for MyApp, which returns a MaterialApp widget
 @override
 Widget build(BuildContext context) {
   return MaterialApp(
     debugShowCheckedModeBanner: false,  // Disable the debug banner in the app
     home: const MainScreen(),  // Set the MainScreen as the home widget of the app
   );
 }
}


// A stateful widget to represent the main screen of the app
class MainScreen extends StatefulWidget {
 const MainScreen({Key? key}) : super(key: key);


 // Creates the mutable state for the MainScreen
 @override
 _MainScreenState createState() => _MainScreenState();
}


// The state class associated with MainScreen, handling its mutable state
class _MainScreenState extends State<MainScreen> {
 bool _showHomePage = false; // To track if the HomePage is visible or not


 // Build method to construct the widget tree for MainScreen
 @override
 Widget build(BuildContext context) {
   return Scaffold(
     body: Stack(  // Using a Stack to layer widgets on top of each other
       children: [
         Center(
           // Centered text displaying a welcome message on the main screen
           child: Text(
             'Welcome to the Main Screen!',
             style: TextStyle(fontSize: 24),  // Style for the welcome message
           ),
         ),
         // Conditionally show the HomePage when _showHomePage is true
         if (_showHomePage)
           const Positioned.fill(
             child: HomePage(),  // HomePage widget fills the screen when visible
           ),
        
         // Top bar similar to the design in the third image
         Positioned(
           top: 0,
           left: 0,
           right: 0,
           child: Container(
             padding: const EdgeInsets.symmetric(vertical: 12.0, horizontal: 16.0),
             decoration: const BoxDecoration(
               color: Color(0xFFF1E2C0), // Match the background color
             ),
             child: Row(
               mainAxisAlignment: MainAxisAlignment.spaceBetween,
               children: [
                 Row(
                   children: const [
                     // Removed the arrow back icon from here
                     SizedBox(width: 8.0),
                     Text(
                       "Nurse Ed Bot",
                       style: TextStyle(
                         fontSize: 24.0,
                         fontWeight: FontWeight.bold,
                         color: Colors.black,
                       ),
                     ),
                   ],
                 ),
                 Row(
                   children: [
                     const Icon(Icons.wifi, size: 28.0, color: Colors.teal), // Wifi icon
                     const SizedBox(width: 8.0),
                     const Icon(Icons.language, size: 28.0, color: Colors.teal), // Globe icon
                     const SizedBox(width: 8.0),
                     const Icon(Icons.person, size: 28.0, color: Colors.teal), // Person icon
                     const SizedBox(width: 8.0),
                     const Icon(Icons.settings, size: 28.0, color: Colors.teal), // Settings icon
                     const SizedBox(width: 8.0),
                     const Icon(Icons.local_hospital, size: 28.0, color: Colors.red), // Emergency icon
                     const SizedBox(width: 8.0),


                     // Clickable Android icon wrapped in IconButton
                     IconButton(
                       icon: Icon(
                         _showHomePage ? Icons.close : Icons.android,  // Toggle icon based on _showHomePage
                         size: 28.0,
                         color: Colors.teal,
                       ),
                       onPressed: () {
                         setState(() {
                           _showHomePage = !_showHomePage;  // Toggle HomePage visibility when clicked
                         });
                       },
                     ),
                   ],
                 ),
               ],
             ),
           ),
         ),


         // Align banner to be at bottom of HomePage
         if (_showHomePage == false)
           const Align(
             alignment: Alignment.bottomCenter,
             child: Image(
               image: AssetImage('assets/art-banner.png'),
             ),
           ),
       ],
     ),
     backgroundColor: const Color(0xFFF1E2C0),
   );
 }
}



