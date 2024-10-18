import 'package:flutter/material.dart';

class Iconstate extends StatelessWidget {
  final IconData icon;
  const Iconstate({super.key, required this.icon});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 200,
      width: 200,
      decoration: BoxDecoration(
          color: Colors.blue, borderRadius: BorderRadius.circular(100)),
      child: Icon(
        icon,
        color: Colors.white,
        size: 150,
      ),
    );
  }
}
