import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

import 'package:mictseta/Components/Buttons.dart';

class JobdetailsPage extends StatefulWidget {
  final dynamic jobDetails;
  final String token;
  const JobdetailsPage(
      {super.key, required this.jobDetails, required this.token});

  @override
  State<JobdetailsPage> createState() => _JobdetailsPageState();
}

class _JobdetailsPageState extends State<JobdetailsPage> {
  String? token; // Make it nullable to handle null cases
  final storage = FlutterSecureStorage();

  @override
  void initState() {
    super.initState();
    _retrieveToken();
  }

  Future<void> _retrieveToken() async {
    String? tkn = await storage.read(key: 'auth_token');
    if (tkn != null) {
      setState(() {
        token = tkn;
      });
    } else {
      print('No token found');
    }
  }

  Future<void> _applyJob(int id) async {
    if (token == null) {
      print('Token is missing. Please log in.');
      return;
    }

    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => Center(child: CircularProgressIndicator()),
    );

    var url = 'http://127.0.0.1:8000/rest_api/jobs/apply/$id/';
    print('Here is token: $token');
    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Token $token',
        },
        body: jsonEncode({}),
      );

      Navigator.pop(context); // Close the dialog once response is received

      if (response.statusCode == 201) {
        print('Application submitted successfully');
      } else if (response.statusCode == 302) {
        var redirectUrl = response.headers['location'];
        print('Redirected to: $redirectUrl');
      } else {
        print('Failed to apply: ${response.body}');
      }
    } catch (e) {
      Navigator.pop(context); // Close the dialog on error
      print('Error: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.blue[100],
      appBar: AppBar(
        title: Text(widget.jobDetails['title']),
        centerTitle: true,
        foregroundColor: Colors.white,
        backgroundColor: Colors.blue[900],
      ),
      body: Padding(
        padding: const EdgeInsets.all(8.0),
        child: SingleChildScrollView(
          child:
              Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Center(
              child: Image.asset(
                'assets/image.png',
                height: 200,
                width: 200,
                fit: BoxFit.cover,
              ),
            ),
            SizedBox(height: 10),
            Text(
              'Title',
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20),
            ),
            Text(
              widget.jobDetails['title'],
              style: TextStyle(fontWeight: FontWeight.w300),
            ),
            SizedBox(height: 5),
//             ReadMoreText(
//   'Flutter is Google’s mobile UI open source framework to build high-quality native (super fast) interfaces for iOS and Android apps with the unified codebase.',
//   trimMode: TrimMode.Line,
//   trimLines: 2,
//   colorClickableText: Colors.pink,
//   trimCollapsedText: 'Show more',
//   trimExpandedText: 'Show less',
//   moreStyle: TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
// );
            Text(
              'Description:',
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20),
            ),
            SizedBox(height: 5),
            Text(
              widget.jobDetails['description'],
              style: TextStyle(fontWeight: FontWeight.w300),
            ),
            SizedBox(height: 5),
            Text(
              'Requirements:',
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20),
            ),
            SizedBox(height: 10),
            Buttons(
              onTap: () {
                _applyJob(widget.jobDetails['id']);
              },
              backgroundColor: Colors.white,
              foregroundColor: const Color.fromARGB(255, 13, 74, 167),
              child: 'Apply Now',
            )
          ]),
        ),
      ),
    );
  }
}
