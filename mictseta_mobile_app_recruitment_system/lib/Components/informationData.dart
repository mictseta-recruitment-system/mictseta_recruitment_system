import 'package:flutter/material.dart';

class Informationdata extends StatelessWidget {
  const Informationdata(
      {super.key, required this.title, required this.description});
  final String title;
  final String description;
  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(title,
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        Divider(),
        Text(
          description,
          style: TextStyle(fontSize: 16),
        ),
      ],
    );
  }
}
