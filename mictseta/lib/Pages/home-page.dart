import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import '../Components/JobDisplayer.dart';
import 'jobDetails.dart';

class HomePage extends StatefulWidget {
  // final String? token;
  const HomePage({super.key  });

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  late Future<List<dynamic>> _futureJobs;

  @override
  void initState() {
    super.initState();
    _futureJobs = _fetchJobs();
  }

  Future<List<dynamic>> _fetchJobs() async {
    final url = 'http://127.0.0.1:8000/rest_api/jobs/';
    try {
      final response = await http.get(Uri.parse(url));

      if (response.statusCode == 200) {
        var data = json.decode(response.body);
        return data;
      } else {
        throw Exception('Failed to load jobs: ${response.statusCode}');
      }
    } catch (e) {
      print(e.toString());
      throw Exception('Failed to fetch jobs: ${e.toString()}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<dynamic>>(
      future: _futureJobs,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return Center(child: CircularProgressIndicator());
        } else if (snapshot.hasError) {
          return Center(child: Text('Error: ${snapshot.error}'));
        } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
          return Center(child: Text('No Jobs Available yet'));
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
                  
                  shrinkWrap: true,
                  physics: NeverScrollableScrollPhysics(),
                  itemCount: jobs.length,
                  itemBuilder: (context, index) {
                    var job = jobs[index];
                    String date = job['end_date'];
                    return Padding(
                      padding: const EdgeInsets.only(bottom:8.0),
                      child: GestureDetector(
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => JobdetailsPage(
                                jobDetails: job, token: '',
                              ),
                            ),
                          );
                        },
                        child: JobdisplayerPage(
                          jobTitle: job['title'],
                          jobDescription: job['description'],
                          jobDue: date.substring(0, 10),
                          // date: job['start_date'],
                          location: job['location'],
                        ),
                      ),
                    );
                  },
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}
