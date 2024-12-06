import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:markdown_viewer/markdown_viewer.dart';
import 'package:http/http.dart' as http;
import 'config.dart';

// List to store all chat messages (user and bot)
List<Map<String, String>> messages = [];

class HomePage extends StatefulWidget { 
  const HomePage({Key? key}) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

// State class for the HomePage widget
class _HomePageState extends State<HomePage> { 
  final _textController = TextEditingController();  // Controller for handling text input
  final List<Map<String, String>> _messages = messages;  // Local copy of messages list

  // Function to handle sending a message
  void _sendMessage() async {
    final text = _textController.text;  // Get text from the input field
    if (text.isEmpty) return;  // Return if text is empty

    // Add user message to the chat
    setState(() {
      _messages.add({'sender': 'user', 'text': text});
      _textController.clear();  // Clear the input field after sending
    });

    // API request to backend server, note that https can only make request to https 
    var url = Uri.parse(Config.serverUrl + '/api/send_msg');
    var response = await http.post(url, body: text);  // Send the message to the server
    var decodedResp = jsonDecode(utf8.decode(response.bodyBytes)) as Map;  // Decode the JSON response

    // Add bot response to the chat
    setState(() {
      _messages.add({'sender': 'bot', 'text': decodedResp['response_text']});
    });
  }

  // Simple function to generate a bot response (could be used if no backend server is available)
  String _generateBotResponse(String userMessage) {
    return "You said: $userMessage";  // Echoes user input
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Chatbot"),  // Title for the AppBar
      ),
      body: Column(
        children: [
          // Expanded widget to display chat messages
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(8.0),
              itemCount: _messages.length,  // Total number of messages
              itemBuilder: (context, index) {
                final message = _messages[index];  // Get message at current index
                final isUserMessage = message['sender'] == 'user';  // Check if message is from user

                // Display message, align right for user and left for bot
                return Align(
                  alignment: isUserMessage
                      ? Alignment.centerRight
                      : Alignment.centerLeft,
                  child: Container(
                    margin: const EdgeInsets.symmetric(vertical: 4.0),
                    padding: const EdgeInsets.all(12.0),
                    decoration: BoxDecoration(
                      color: isUserMessage ? Color(0xFF373B38) : Color(0xFF06B67F),  // Different colors for user and bot messages
                      borderRadius: BorderRadius.circular(8.0),
                    ),
                    child: 
                    MarkdownViewer(
                        message['text']!,
                        enableTaskList: true,
                        enableSuperscript: false,
                        enableSubscript: false,
                        enableFootnote: false,
                        enableImageSize: false,
                        enableKbd: false,
                        syntaxExtensions: const [],
                        elementBuilders: const [],
                        styleSheet: MarkdownStyle(
                            textStyle: TextStyle(
                              color: isUserMessage ? Colors.white : Colors.black,
                            ),
                          ),
                      ),
                  ),
                );
              },
            ),
          ),
          // Input field and send button at the bottom
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _textController,  // Controller for the input field
                    decoration: const InputDecoration(
                      hintText: 'Type a message',  // Placeholder hint in the input field
                      border: OutlineInputBorder(),
                    ),
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.send),  // Icon for the send button
                  onPressed: _sendMessage,  // Send the message when button is pressed
                ),
              ],
            ),
          ),
        ],
      ),
      backgroundColor: const Color(0xFFF1E2C0),
    );
  }
}
