import 'package:flutter/material.dart';

class Buttons extends StatelessWidget {
  final String child;
  final Function() onTap;
  final Color backgroundColor;
  final Color foregroundColor;
  const Buttons({super.key, required this.child, required this.onTap, required this.backgroundColor, required this.foregroundColor});

  @override
  Widget build(BuildContext context) {
    return OutlinedButton(
      onPressed:onTap,
      style: ButtonStyle(
        minimumSize: WidgetStatePropertyAll(
          Size(double.infinity, 55),
        ),
        foregroundColor: WidgetStatePropertyAll(foregroundColor),
        backgroundColor: WidgetStatePropertyAll(backgroundColor),
        shape: WidgetStatePropertyAll(
            RoundedRectangleBorder(borderRadius: BorderRadius.circular(5))),
        side: WidgetStateProperty.resolveWith<BorderSide>(
          (Set<WidgetState> states) {
            return BorderSide(
              color: const Color.fromARGB(255, 14, 74, 165),
              width: 1.0,
            );
          },
        ),
      ),
      child: Text(
        child,
      ),
    );
  }
}
