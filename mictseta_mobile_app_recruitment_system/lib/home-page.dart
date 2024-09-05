// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables

import 'package:flutter/material.dart';

import 'Components/JobDisplayer.dart';
import 'jobDetails.dart';
class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Available Vacancies',
                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20)),
            SizedBox(height: 10),
            GestureDetector(
              onTap: () {
                Navigator.push(context,
                    MaterialPageRoute(builder: (context) => JobdetailsPage()));
              },
              child: Expanded(
                child: JobdisplayerPage(
                  jobTitle: 'Junior Front-end Developer',
                  jobDescription: 'The job want the slender people',
                  jobDue: ' Due: ',
                  date: '20-05-2024',
                  location: 'Johanesburg',
                ),
              ),
            )
          ],
        ),
      ),
    );
  }
}
