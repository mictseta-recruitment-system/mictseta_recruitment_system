import 'dart:convert';


import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class Api {
 Future<void> _applyJob(BuildContext context, int id) async {
    showDialog(
        context: context,
        builder: (context) => Center(child: CircularProgressIndicator()));
    var url = 'https://10.0.2.2:8000/rest_api/jobs/apply/$id/';

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode({}),
      );

      if (response.statusCode == 200) {
        
        print('Application submitted successfully');
      } else {
        print('Failed to apply: ${response.statusCode}');
      }
    } catch (e) {
      Navigator.pop(context);
      print('Error: $e');
    }
  }

}
