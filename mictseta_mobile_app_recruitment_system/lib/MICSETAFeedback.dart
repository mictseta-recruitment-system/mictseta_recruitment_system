// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';

import 'Components/Table.dart';

class FeedBackPage extends StatefulWidget {
  const FeedBackPage({super.key});

  @override
  State<FeedBackPage> createState() => _FeedBackPageState();
}

class _FeedBackPageState extends State<FeedBackPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.blue[100],
      appBar: AppBar(
        title: Text('MICseta Feedback'),
        foregroundColor: Colors.white,
        backgroundColor: Colors.blue[900],
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(10.0),
        child: Column(
          children: [
            Tables(columnName: 'Status', columnValue: 'Rejected'),
            Tables(columnName: 'Feedback Time', columnValue: '12:30'),
            Tables(columnName: 'Feedback Date', columnValue: '23-06-2030'),
            SizedBox(
              height: 10,
            ),
            OutlinedButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              style: ButtonStyle(
                  shape: WidgetStatePropertyAll(RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(5))),
                  minimumSize: WidgetStatePropertyAll(
                    Size(double.infinity, 55),
                  ),
                  foregroundColor: WidgetStatePropertyAll(Colors.blue[900]),
                  backgroundColor: WidgetStatePropertyAll(Colors.blue[50])),
              child: Text('Back'),
            )
          ],
        ),
      ),
    );
  }
}
