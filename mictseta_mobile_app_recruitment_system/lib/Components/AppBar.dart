import 'package:flutter/material.dart';

class AppbarPage extends StatelessWidget {
  final String title;
  const AppbarPage({super.key, required this.title});

  @override
  Widget build(BuildContext context) {
    return AppBar(
      backgroundColor: Colors.blue[100],
      foregroundColor: Colors.white,
      centerTitle: true,
      title: Text(title),
    );
  }
}
