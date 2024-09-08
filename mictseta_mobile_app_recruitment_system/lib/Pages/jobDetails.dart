import 'package:flutter/material.dart';
import 'package:mictseta_mobile_app_recruitment_system/Components/Buttons.dart';
import 'package:http/http.dart ' as http;
import 'dart:convert';

class JobdetailsPage extends StatefulWidget {
  final dynamic jobDetails;
  final String token;
  const JobdetailsPage({super.key, required this.jobDetails,required this.token});

  @override
  State<JobdetailsPage> createState() => _JobdetailsPageState();
}

class _JobdetailsPageState extends State<JobdetailsPage> {
  Future<void> _applyJob(int id) async {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => Center(child: CircularProgressIndicator()),
    );

    var url = 'http://10.0.2.2:8000/rest_api/jobs/apply/$id/';

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode({}),
      );

      Navigator.pop(context);

      if (response.statusCode == 200) {
        print('Application submitted successfully');
      } else if (response.statusCode == 302) {
        var redirectUrl = response.headers['location'];
        print('Redirected to: $redirectUrl');
      } else {
        print('Failed to apply: ${response.statusCode}');
      }
    } catch (e) {
      Navigator.pop(context);
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
                  child: Image.asset('assets/image.png',
                      height: 200, width: 200, fit: BoxFit.cover)),
              SizedBox(height: 10),
              Text('Title',
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20)),
              Text(widget.jobDetails['title'],
                  style: TextStyle(fontWeight: FontWeight.w300)),
              SizedBox(height: 5),
              Text('Description:',
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20)),
              SizedBox(height: 5),
              Text(widget.jobDetails['description'],
                  style: TextStyle(fontWeight: FontWeight.w300)),
              SizedBox(height: 5),
              Text('Requirements:',
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20)),
              SizedBox(height: 5),
              Text(
                  '- Java\n- JavaScripts\n- Python\n- Ruby\n- HTML\n- PhP\n- CSS'),
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
        ));
  }
}
