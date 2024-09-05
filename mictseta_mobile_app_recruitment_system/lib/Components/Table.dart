import 'package:flutter/material.dart';

class Tables extends StatelessWidget {
  final String columnName;
  final String columnValue;
  const Tables(
      {super.key, required this.columnName, required this.columnValue});

  @override
  Widget build(BuildContext context) {
    return Table(
      border: TableBorder.all(),
      children: [
        TableRow(
          children: [
            TableCell(
              child: Padding(
                padding: const EdgeInsets.all(10),
                child: Text(columnName,
                    style: TextStyle(fontWeight: FontWeight.bold)),
              ),
            ),
            TableCell(
              child: Padding(
                padding: const EdgeInsets.all(10.0),
                child: Text(columnValue),
              ),
            ),
          ],
        ),
      ],
    );
  }
}
