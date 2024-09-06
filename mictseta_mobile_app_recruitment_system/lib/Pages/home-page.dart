// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables

import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import '../Components/JobDisplayer.dart';
import 'jobDetails.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  String url = 'http://127.0.0.1:8000/rest_api/jobs/';

  Future<List<dynamic>> _futureJobs() async {
    var res = await http.get(Uri.parse(url));
    if (res.statusCode == 200) {
      var data = json.decode(res.body);
      return data;
    } else {
      throw Exception('Failed to fetch jobs');
    }
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
        future: _futureJobs(),
        builder: (index, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (!snapshot.hasData) {
            return Center(child: Text('No Jobs Available yet'));
          } else if (snapshot.hasError) {
            return Center(child: Text(snapshot.error.toString()));
          }
          List<dynamic> jobs = snapshot.data!;
          return SingleChildScrollView(
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Available Vacancies',
                      style:
                          TextStyle(fontWeight: FontWeight.bold, fontSize: 20)),
                  SizedBox(height: 10),
                  ListView.builder(
                      itemCount: jobs.length,
                      itemBuilder: (context, index) {
                        var job = jobs[index];
                        return Expanded(
                          child: JobdisplayerPage(
                            onTap: () {
                              Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                      builder: (context) => JobdetailsPage(jobDetails: jobs[index],)));
                            },
                            jobTitle: job['title'],
                            jobDescription: job['description'],
                            jobDue: job['end_date'],
                            date: job['start_date'],
                            location: job['location'],
                          ),
                        );
                      })
                ],
              ),
            ),
          );
        });
  }
}
